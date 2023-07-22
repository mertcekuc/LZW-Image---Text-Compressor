from PIL import Image
import numpy as np
import math
import os

def readGrayImage(path):
    img=Image.open(path)
    img_gray=img.convert('L')

    return img_gray

def PIL2np(img):
    nrow=img.size[0]
    ncol=img.size[1]

    img_arr=np.array(img.convert('L'))
    return img_arr
    
def np2PIL(im):
    print("size of arr: ",im.shape)
    img = Image.fromarray(np.uint8(im))
    
    return img

def differenceArr(array):
    
    m=len(array)
    n=len(array[0])

    intarray=[]
    
    for i in range(m):
        
        row=[]

        row.append(int(array[i][0]))
        for j in range(1, n):
            row.append((int(array[i][j])) - (int(array[i][j-1])))
            
        intarray.append(row)

    pivot = (intarray[0][0])
    diffarray =intarray.copy()
    
    for i in range(1,m):
        diffarray[i][0]=intarray[i][0]-intarray[i-1][0]

    diffarray[0][0]=diffarray[0][0]-pivot

    output=diffarray.copy()
    output.insert(0,[pivot])


    return output

def LZwencode(array):
    

    dict_size=511
    dct={i+255:[i] for i in range (-255, 256)}
    
    output=[[]]
    value=[]
    valuecol=[]
    

    rownumber=0
    for row in array:
        for column in row:
            valuecol=value.copy()
            valuecol.append(column)
            

            if valuecol in list(dct.values()):
                value=valuecol.copy()
            else:
                output[rownumber].append(list(dct.values()).index(value))
                dct[dict_size]=valuecol.copy()
                dict_size+=1
                value=[]
                value.append(column)
        
            
        if value:
            output[rownumber].append(list(dct.values()).index(value))

        if rownumber != len(array)-1:
            output.append([])
            rownumber+=1

        

        value=[]
        valuecol=[]

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

    output=[]
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
                        output.append(bitstr)
                        bitstr=""
                        byte=file.read(1)
    
        byte=ord(byte)
        bits = '{0:08b}'.format(byte)
        bitstr+=bits
        byte=file.read(1)
    
    output.append(bitstr)

    return output

def reConstructImage(diffarray):
    pivot=diffarray.pop(0)[0]
    diffarray[0][0]=diffarray[0][0] + pivot

    m=len(diffarray)
    n=len(diffarray[1])

    for i in range(1,m):
        diffarray[i][0]=diffarray[i][0]+diffarray[i-1][0]


    for i in range(m):
        for j in range(1,m):
            diffarray[i][j]=diffarray[i][j]+diffarray[i][j-1]

    return diffarray

def calcualteEntropy(imgarray):
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
    gray_image=readGrayImage(path)
    array=PIL2np(gray_image)

    calcualteEntropy(array)

    difArray=differenceArr(array)
    encoded=LZwencode(difArray)

    bitStr=intToBinaryString(encoded)
    padded=padding(bitStr)
    bytesArr=getBytes(padded)

    compressedFile=open(filepath+"/grey_diff_compressed.bmp","wb")

    for line in range(len(bytesArr)):
        compressedFile.write(bytesArr[line])
        if line != (len(bytesArr)-1):
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')
            compressedFile.write(b'\t')
            compressedFile.write(b'\n')
    compressedFile.close()

    entropy=calcualteEntropy(array)
    firstsize=os.path.getsize(path)
    secondsize=os.path.getsize(filepath+"/grey_diff_compressed.bmp")

    ratio= 100-(100 * (float(secondsize)/float(firstsize)))

    return ratio, firstsize ,secondsize ,entropy

def defcompress(path,decompresspath):
    decompressedFile=open(path,"rb")
    decompressed=byteToInt(decompressedFile)
    decompressedFile.close()


    removepadded=(removePadding(decompressed))
    decoded=(LZWdecode(removepadded))
    imgarr=reConstructImage(decoded)

    imgarr=np.array(imgarr)
    img=np2PIL(imgarr)
    img.save(decompresspath+"/greydiffdecmp.png")















