from PIL import Image
import numpy as np
import math
import os

def PIL2np(img):
    nrow=img.size[0]
    ncol=img.size[1]

    img_arr=np.array(img.convert('L'))
    return img_arr
    
def np2PIL(im):
    print("size of arr: ",im.shape)
    img = Image.fromarray(np.uint8(im))
    
    return img

def splitColors(img):
    
    r, g, b =img.split()
    
    rarray=np.array(r.convert('L'))
    garray=np.array(g.convert('L'))
    barray=np.array(b.convert('L'))
    
    return rarray, garray, barray

def differenceArr(array):
    m = len(array)
    n = len(array[0])


    array=array.astype(int)
    copyarray=[]
    for i in range(m):
        row=[]
        for j in range(n):
            value=int(array[i][j])
            row.append(value)
        copyarray.append(row)
    intarray=[]
    for i in range(m):
        row=[int(copyarray[i][0])]
        for j in range(1,n):
            row.append(int((copyarray[i][j])- (copyarray[i][j-1])))
        intarray.append(row)

    pivot=intarray[0][0]
    diff_array=[]
    for i in range(m):
        row=[]
        for j in range(n):
            value=int(intarray[i][j])
            row.append(value)
        diff_array.append(row)

    for i in range(1,m):

        diff_array[i][0]=int(int(intarray[i][0])- (int(intarray[i-1][0])))

    diff_array[0][0] -= pivot
    diff_array.insert(0,[pivot])

    return diff_array

def LZwencode(array):

    dict_size = 511
    max_dict_size = 1 << 12
    dct = {i+255: [i] for i in range (-255, 256)}
    
    output = [[]]
    value = []
    valuecol = []
    

    rownumber = 0
    for row in array:
        for column in row:
            valuecol = value.copy()
            valuecol.append(column)
            

            if valuecol in list(dct.values()):
                value = valuecol.copy()
            elif dict_size == max_dict_size:
                output[rownumber].append(list(dct.values()).index(value))
                value = []
                value.append(column)
            else:
                output[rownumber].append(list(dct.values()).index(value))
                dct[dict_size] = valuecol.copy()
                dict_size += 1
                value = []
                value.append(column)
        
            
        if value:
            output[rownumber].append(list(dct.values()).index(value))

        if rownumber != len(array) - 1:
            output.append([])
            rownumber += 1

        value = []
        valuecol = []
        

    return output
    
def LZWdecode(encodedArray):

    dict_size=511
    dct={i+255:[i] for i in range (-255, 256)}
    
    output=[]
    entry=[]
    
    for row in encodedArray:
        row_output = []
        value=dct[row[0]].copy()
        row_output.extend(value)
        row.pop(0)
        
        for column in row:
            if column in dct:
                entry=dct[column].copy()
            elif column==dict_size:
                entry=value.copy()
                entry.append(value[0])
            else:
                print("ERROR")
                return 0
            
            row_output.extend(entry)
            dct[dict_size]=value.copy()
            dct[dict_size].append(entry[0])
            dict_size+=1

            value=entry.copy()

        output.append(row_output)


    return output
    
def intToBinaryString(array, codelength=12):
    strarray = []
    for row in array:
        bitstr = ""
        for index in row:
            for n in range(codelength):
                if index & (1 << (codelength - 1 - n)):
                    bitstr += "1"
                else:
                    bitstr += "0"
        strarray.append(bitstr)
    return strarray

def padding(array, codelength=12):
    output = []
    for index in array:
        extra_padding = 8 - (len(index) % 8)
        index += "0" * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        index = padded_info + index
        output.append(index)
    return output

def removePadding(array, codelength=12):
    output = []
    for index in array:
        padded_info = index[:8]
        extra_padding = int(padded_info, 2)
        index = index[8:]
        encoded_text = index[:-extra_padding]
        numbers = []
        for bits in range(0, len(encoded_text), codelength):
            numbers.append(int(encoded_text[bits:bits+codelength], 2))
        output.append(numbers)
    return output

def byteToInt(file):

    red=[]
    green=[]
    blue=[]
    bitstr=""
    
    # Read data from file until newline character is reached
    byte=file.read(1)
    while(len(byte)>0):

        if(byte == b'\t'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'\n') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'\t') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'\n') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        red.append(bitstr)
                        bitstr=""
                        byte=file.read(1)
        

        if(byte == b'a'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'z') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'0') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'/') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        red.append(bitstr)
                        bitstr=""
                        break

    
        byte=ord(byte)
        bits = '{0:08b}'.format(byte)
        bitstr+=bits
        byte=file.read(1)

    byte=file.read(1)
    while(len(byte)>0):

        if(byte == b'\t'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'\n') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'\t') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'\n') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        green.append(bitstr)
                        bitstr=""
                        byte=file.read(1)
        
        if(byte == b'a'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'z') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'0') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'/') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        green.append(bitstr)
                        bitstr=""
                        break

    
        byte=ord(byte)
        bits = '{0:08b}'.format(byte)
        bitstr+=bits
        byte=file.read(1)    
    
    byte=file.read(1)
    while(len(byte)>0):

        if(byte == b'\t'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'\n') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'\t') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'\n') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        blue.append(bitstr)
                        bitstr=""
                        byte=file.read(1)
        
        if(byte == b'a'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'z') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'0') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'/') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        blue.append(bitstr)
                        bitstr=""
                        break

    
        byte=ord(byte)
        bits = '{0:08b}'.format(byte)
        bitstr+=bits
        byte=file.read(1)    
    
    blue.append(bitstr)

    return red, green, blue

def reversediffarray(diffarray):
    pivot=diffarray.pop(0)[0]
    diffarray[0][0]=diffarray[0][0] + pivot

    m = len(diffarray)
    n = len(diffarray[0])

    for i in range(1, m):
        diffarray[i][0] = pivot + diffarray[i][0]
        pivot = diffarray[i][0]

    for i in range(m):
        for j in range(1, n):
            diffarray[i][j] = diffarray[i][j] + diffarray[i][j-1]

    return diffarray

def getBytes(padded):
    output=[]
    for padded_bytes in padded:
        if(len(padded_bytes)%8!=0):
            print("Error on byte padding")
            exit(0)
        
        b=bytearray()

        for i in range(0,len(padded_bytes),8):
            byte=padded_bytes[i:i+8]
            b.append(int(byte,2))

        output.append(b)
    
    return output

def byteToInt(file):

    red=[]
    green=[]
    blue=[]
    bitstr=""
    
    # Read data from file until newline character is reached
    byte=file.read(1)
    while(len(byte)>0):

        if(byte == b'\t'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'\n') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'\t') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'\n') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        red.append(bitstr)
                        bitstr=""
                        byte=file.read(1)
        

        if(byte == b'a'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'z') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'0') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'/') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        red.append(bitstr)
                        bitstr=""
                        break

    
        byte=ord(byte)
        bits = '{0:08b}'.format(byte)
        bitstr+=bits
        byte=file.read(1)

    byte=file.read(1)
    while(len(byte)>0):

        if(byte == b'\t'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'\n') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'\t') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'\n') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        green.append(bitstr)
                        bitstr=""
                        byte=file.read(1)
        
        if(byte == b'a'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'z') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'0') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'/') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        green.append(bitstr)
                        bitstr=""
                        break

    
        byte=ord(byte)
        bits = '{0:08b}'.format(byte)
        bitstr+=bits
        byte=file.read(1)    
    
    byte=file.read(1)
    while(len(byte)>0):

        if(byte == b'\t'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'\n') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'\t') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'\n') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        blue.append(bitstr)
                        bitstr=""
                        byte=file.read(1)
        
        if(byte == b'a'):
            byte=ord(byte)
            bits = '{0:08b}'.format(byte)
            bitstr+=bits
            byte=file.read(1)
            if(byte == b'z') and (len(byte)>0):
                byte=ord(byte)
                bits = '{0:08b}'.format(byte)
                bitstr+=bits
                byte=file.read(1)
                if(byte == b'0') and (len(byte)>0):
                    byte=ord(byte)
                    bits = '{0:08b}'.format(byte)
                    bitstr+=bits
                    byte=file.read(1)
                    if(byte == b'/') and (len(byte)>0):
                        bitstr=bitstr[:-24]
                        blue.append(bitstr)
                        bitstr=""
                        break

    
        byte=ord(byte)
        bits = '{0:08b}'.format(byte)
        bitstr+=bits
        byte=file.read(1)    
    
    blue.append(bitstr)

    return red, green, blue

def calcualteEntropy(imgarray):
    import math
    values={}

    m=len(imgarray)
    n=len(imgarray[0])

    
    for i in range(m):
        for j in range(n):
            key=int(imgarray[i][j])
            if key in values:
                values[key]+=1
            else:
                d1={key:1}
                values.update(d1)

    sum=0
    for i in values:
        sum+=values[i]

    entropy=0

    for i in values:
        prob=values[i]/sum
        log=(math.log(prob))
        entropy= entropy + (prob*log)
    entropy*=(-1)
    

    return entropy

def compress(path,filepath):
    img=Image.open(path)
    r,g,b=splitColors(img)

    rdiff=differenceArr(r)
    gdiff=differenceArr(g)
    bdiff=differenceArr(b)

    rbytes=getBytes(padding(intToBinaryString(LZwencode(rdiff))))
    gbytes=getBytes(padding(intToBinaryString(LZwencode(gdiff))))
    bbytes=getBytes(padding(intToBinaryString(LZwencode(bdiff))))

    compressedFile=open(filepath+"/thumbs_up_difference.bmp","wb")

    for line in range(len(rbytes)):
        compressedFile.write(rbytes[line])
        if line != (len(rbytes)-1):
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')

    compressedFile.write(b'a')
    compressedFile.write(b'z')
    compressedFile.write(b'0')
    compressedFile.write(b'/')

    for line in range(len(gbytes)):
        compressedFile.write(gbytes[line])
        if line != (len(gbytes)-1):
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')

    compressedFile.write(b'a')
    compressedFile.write(b'z')
    compressedFile.write(b'0')
    compressedFile.write(b'/')

    for line in range(len(bbytes)):
        compressedFile.write(bbytes[line])
        if line != (len(bbytes)-1):
                compressedFile.write(b'\t')
                compressedFile.write(b'\n')
                compressedFile.write(b'\t')
                compressedFile.write(b'\n')
    compressedFile.close()

    entropy=calcualteEntropy(r) +calcualteEntropy(g) +calcualteEntropy(b)
    firstsize=os.path.getsize(path)
    secondsize=os.path.getsize(filepath+"/thumbs_up_difference.bmp")

    ratio= 100-(100 * (float(secondsize)/float(firstsize)))

    return ratio, firstsize ,secondsize ,entropy

def decompress(path,decompresspath):
    decompressf=open(path,"rb")
    r2, g2, b2=byteToInt(decompressf)

    r2dc=reversediffarray((LZWdecode((removePadding(((r2)))))))
    g2dc=reversediffarray((LZWdecode((removePadding(((g2)))))))
    b2dc=reversediffarray((LZWdecode((removePadding(((b2)))))))

    rdecode = np.array(r2dc).astype(np.uint8)
    gdecode = np.array(g2dc).astype(np.uint8)
    bdecode = np.array(b2dc).astype(np.uint8)

    assert rdecode.shape == gdecode.shape == bdecode.shape

    imgg = Image.fromarray(np.dstack((rdecode, gdecode, bdecode)))
    imgg.save(decompresspath+"/colordifference.bmp")


