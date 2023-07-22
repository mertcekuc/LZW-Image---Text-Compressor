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
    #imgarr=np.array(img.convert('L'))
    #m,n=np.shape(imgarr)
    #zeros=np.zeros((m,n))  
    #zeros = Image.fromarray(np.uint8(zeros))
    
    r, g, b =img.split()
    
    rarray=np.array(r.convert('L'))
    garray=np.array(g.convert('L'))
    barray=np.array(b.convert('L'))
    
    return rarray, garray, barray

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

def LZwencode(array):

    dict_size = 256
    max_dict_size = 1 << 12
    dct = {i: [i] for i in range (0, dict_size)}
    
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
    dict_size = 256
    max_dict_size = 1 << 12
    dct = {i: [i] for i in range(0, dict_size)}

    output = []
    entry = []
    for row in encodedArray:
        row_output = []
        value = dct[row[0]].copy()
        row_output.extend(value)
        row.pop(0)

        for column in row:
            if column in dct:
                entry = dct[column].copy()
            elif column == dict_size:
                entry = value.copy()
                entry.append(value[0])
            else:
                raise ValueError("Invalid column value")

            row_output.extend(entry)
            if dict_size < max_dict_size:
                dct[dict_size] = value + [entry[0]]
                dict_size += 1

            value = entry.copy()

        output.append(row_output)

    return output
    
def intToBinaryString(array,codelength=12):
    
    strarray=[]
    bitstr=""
    
    for row in array:
        for index in row:
            for n in range(codelength):
                if index  & (1 << (codelength - 1 - n)):
                    bitstr+="1"
                else:
                    bitstr+="0"
                
        strarray.append(bitstr)
        bitstr=""

    return strarray

def padding(array,codelength=12):
    output=[]
    for index in array:
        extra_padding=8-(len(index) % 8)
        for i in range(extra_padding):
            index += "0"

        padded_info=  "{0:08b}".format(extra_padding)
        index= padded_info + index
        output.append(index)
    
    return output

def removePadding(array,codelength=12):
    output=[]
    for index in array:
        padded_info=index[:8]
        extra_padding=int(padded_info,2)

        index=index[8:]
        encoded_text=index[:-1*extra_padding]

        numbers=[]
        for bits in range (0,len(encoded_text),codelength):
            numbers.append(int(encoded_text[bits:bits+codelength],2))
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
    
def decompressfile(path,decompresspath):
    file=open(path,"rb")
    r,g,b=byteToInt(file)
    file.close()


    rdecode=LZWdecode(removePadding(r))
    gdecode=LZWdecode(removePadding(g))
    bdecode=LZWdecode(removePadding(b))

    rdecode = np.array(rdecode).astype(np.uint8)
    gdecode = np.array(gdecode).astype(np.uint8)
    bdecode = np.array(bdecode).astype(np.uint8)

    assert rdecode.shape == gdecode.shape == bdecode.shape

    imgg = Image.fromarray(np.dstack((rdecode, gdecode, bdecode)))
    imgg.save(decompresspath+"/colordiffdecmp.bmp")

def redImage(img):
    red, greeen, blue=splitColors(img)
    

    red = np.array(red).astype(np.uint8)
    m,n=np.shape(red)
    zeros=np.zeros((m,n))  
    zeros = Image.fromarray(np.uint8(zeros))

    imgg = Image.fromarray(np.dstack((red, zeros, zeros)))
    

    return imgg

def greenImage(img):
    red, green, blue=splitColors(img)
    

    green = np.array(green).astype(np.uint8)
    m,n=np.shape(green)
    zeros=np.zeros((m,n))  
    zeros = Image.fromarray(np.uint8(zeros))

    imgg = Image.fromarray(np.dstack((zeros, green, zeros)))
    

    return imgg

def blueImage(img):
    red, greee, blue=splitColors(img)
    

    blue = np.array(blue).astype(np.uint8)
    m,n=np.shape(blue)
    zeros=np.zeros((m,n))  
    zeros = Image.fromarray(np.uint8(zeros))

    imgg = Image.fromarray(np.dstack((zeros, zeros, blue)))
    

    return imgg

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

def compressFile(path,filepath):

    img = Image.open(path)
    rarray, garray, barray=splitColors(img)
    img.close()


    encodedR=(LZwencode(rarray))
    encodedG=(LZwencode(garray))
    encodedB=(LZwencode(barray))


    bytesR=getBytes(padding(intToBinaryString(encodedR)))
    bytesG=getBytes(padding(intToBinaryString(encodedG)))
    bytesB=getBytes(padding(intToBinaryString(encodedB)))

    compressedFile=open(filepath+"/color_compressed.bmp","wb")

    for line in range(len(bytesR)):
        compressedFile.write(bytesR[line])
        if line != (len(bytesR)-1):
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')

    compressedFile.write(b'a')
    compressedFile.write(b'z')
    compressedFile.write(b'0')
    compressedFile.write(b'/')

    for line in range(len(bytesG)):
        compressedFile.write(bytesG[line])
        if line != (len(bytesG)-1):
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')

    compressedFile.write(b'a')
    compressedFile.write(b'z')
    compressedFile.write(b'0')
    compressedFile.write(b'/')

    for line in range(len(bytesB)):
        compressedFile.write(bytesB[line])
        if line != (len(bytesB)-1):
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')
    compressedFile.close()

    entropy=calcualteEntropy(rarray) +calcualteEntropy(garray) +calcualteEntropy(barray)
    firstsize=os.path.getsize(path)
    secondsize=os.path.getsize(filepath+"/color_compressed.bmp")

    ratio= 100-(100 * (float(secondsize)/float(firstsize)))

    return ratio, firstsize ,secondsize ,entropy






