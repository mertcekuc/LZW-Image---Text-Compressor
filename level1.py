import os

def encode(textfile):

    dict_size = 256
    dicitonary = {chr(i): i for i in range(dict_size)}
    
    w = ""
    
    result = []

    while True:
        c= textfile.read(1)
    
        if not c:
            print("reached end of file")
            break

        if w+c in dicitonary:
            w=w+c
        
        else:
            result.append(dicitonary[w])
            dicitonary[w+c]=dict_size
            dict_size +=1
            w=c
        
    if w:
        result.append(dicitonary[w])

    return result

def decode(compressed):
    from io import StringIO

    dict_size=256
    dictionary = {i: chr(i) for i in range(dict_size)}
    
    result=StringIO()

    w=chr(compressed.pop(0))
    result.write(w)

    for k in compressed:
        if k in dictionary:
            entry=dictionary[k]
        elif k== dict_size:
            entry= w+w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        dictionary[dict_size]=w+entry[0]
        dict_size+=1

        w=entry
    
    return result.getvalue()

def intToBytes(intCompressed, codelength=12):
    import math
    bitstr=""
    total_bits=0
    
    for num in intCompressed:
        for n in range(codelength):
            if num & (1 << (codelength - 1 - n)):
                bitstr+="1"
            else:
                bitstr+="0"
            total_bits+=1
    
    return bitstr

def padBytes(encoded_bytes):

    extra_padding=8-len(encoded_bytes) % 8
    for i in range(extra_padding):
        encoded_bytes += "0"
    
    padded_info=  "{0:08b}".format(extra_padding)
    encoded_bytes= padded_info + encoded_bytes
    return encoded_bytes

def removepadding(bitstr,codelength=12):
    padded_info= bitstr[:8]
    extra_padding=int(padded_info,2)
    
    bitstr=bitstr[8:]
    encoded_text= bitstr[:-1*extra_padding]
    int_numbers=[]

    
    for bits in range(0, len(encoded_text),codelength):
        int_numbers.append(int(encoded_text[bits:bits+codelength],2))

    return int_numbers

def decompresstoInt(file):
    bitstr= ""
    
    byte=file.read(1)
    while(len(byte) > 0):
    
        byte=ord(byte)
        bits = '{0:08b}'.format(byte)
        bitstr+=bits
        byte=file.read(1)
    
    byteToIntArray=removepadding(bitstr)
    return byteToIntArray
    
def getByteArray(padded_bytes):
    if(len(padded_bytes)%8!=0):
        print("Error on byte padding")
        exit(0)
    
    b=bytearray()
    for i in range(0,len(padded_bytes),8):
        byte=padded_bytes[i:i+8]
        b.append(int(byte,2))
    
    return b

def compress(path,filepath):
    f = open(path,"r")
    compressed=encode(f)
    f.close()


    byestring=intToBytes(compressed)
    padded=padBytes(byestring)
    byteArray=getByteArray(padded)

    compressedtext=open(filepath+"/compressed_text.bin","wb")
    compressedtext.write(bytes(byteArray))
    compressedtext.close()

    firstsize=os.path.getsize(path)
    secondsize=os.path.getsize(filepath+"/compressed_text.bin")

    ratio= 100-(100 * (float(secondsize)/float(firstsize)))

    return ratio, firstsize ,secondsize

def decompress(path):

    compressedtext=open(path,"rb")
    strtext=decode(decompresstoInt(compressedtext))
    compressedtext.close()

    return strtext












