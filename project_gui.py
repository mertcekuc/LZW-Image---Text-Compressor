import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from level2 import compress,decompress,grayImage
from level3 import compress as l3compress , defcompress as l3decompress
from level4 import compressFile as l4compress , decompressfile as l4decompress ,greenImage ,blueImage ,redImage
from level5 import compress as l5compress , decompress as l5decompress
from level1 import compress as l1compress , decompress as l1decompress
top = Tk()

top.title("GUI")
top.geometry('800x400')

lf = tk.LabelFrame(top, text='Compression')
lf.pack(side=LEFT)

lf3=tk.LabelFrame(top, text='Text')
lf3.place(x=350,y=300)
lf2= tk.LabelFrame(top, text='Decompression')
lf2.pack(side=RIGHT)

img=PIL.Image.open("thumbs_up.bmp")
photo =PIL.ImageTk.PhotoImage(PIL.Image.open("thumbs_up.bmp"))
lbl=Label(image=photo)
lbl.pack()

def b1f():
    filename=filedialog.askopenfilename()
    filepath=filedialog.askdirectory()
    ratio, firstize, secondsize, entropy=compress(filename,filepath)
    message1=("COMPRESSED!\n Before Compression Size:" +str(firstize) +"\nAfter Compression:" +str(secondsize)+"\nRatio: "+str(ratio)+"\nEntropy:"+str(entropy)+"\n Codelength=12")
    messagebox.showinfo(title="COMPRESSED", message=message1)

def b2f():
    filename=filedialog.askopenfilename()
    decompresspath=filedialog.askdirectory()
    decompress(filename,decompresspath)
    messagebox.showinfo(title="DECOMPRESSED", message="DECOMPRESSED")


def b3f():
    filename=filedialog.askopenfilename()
    filepath=filedialog.askdirectory()
    ratio, firstize, secondsize, entropy=l3compress(filename,filepath)
    message1=("COMPRESSED!\n Before Compression Size:" +str(firstize) +"\nAfter Compression:" +str(secondsize)+"\nRatio: "+str(ratio)+"\nEntropy:"+str(entropy)+"\n Codelength=12")
    messagebox.showinfo(title="COMPRESSED", message=message1)
def b4f():
    filename=filedialog.askopenfilename()
    decompresspath=filedialog.askdirectory()
    l3decompress(filename,decompresspath)
    messagebox.showinfo(title="DECOMPRESSED", message="DECOMPRESSED")


def b5f():
    filename=filedialog.askopenfilename()
    filepath=filedialog.askdirectory()
    ratio, firstize, secondsize, entropy=l4compress(filename,filepath)
    message1=("COMPRESSED!\n Before Compression Size:" +str(firstize) +"\nAfter Compression:" +str(secondsize)+"\nRatio: "+str(ratio)+"\nEntropy:"+str(entropy)+"\n Codelength=12")
    messagebox.showinfo(title="COMPRESSED", message=message1)
def b6f():
    filename=filedialog.askopenfilename()
    decompresspath=filedialog.askdirectory()
    l4decompress(filename,decompresspath)
    messagebox.showinfo(title="DECOMPRESSED", message="DECOMPRESSED")

def b7f():
    filename=filedialog.askopenfilename()
    filepath=filedialog.askdirectory()
    ratio, firstize, secondsize, entropy=l5compress(filename,filepath)
    message1=("COMPRESSED!\n Before Compression Size:" +str(firstize) +"\nAfter Compression:" +str(secondsize)+"\nRatio: "+str(ratio)+"\nEntropy:"+str(entropy)+"\n Codelength=12")
    messagebox.showinfo(title="COMPRESSED", message=message1)
def b8f():
    filename=filedialog.askopenfilename()
    decompresspath=filedialog.askdirectory()
    l5decompress(filename,decompresspath)
    messagebox.showinfo(title="DECOMPRESSED", message="DECOMPRESSED")

def b9f():
    filename=filedialog.askopenfilename()
    filepath=filedialog.askdirectory()
    ratio,firstsize,secondsize=l1compress(filename,filepath)
    message1=("COMPRESSED!\n Before Compression Size:" +str(firstsize) +"\nAfter Compression:" +str(secondsize)+"\nRatio: "+str(ratio))
    messagebox.showinfo(title="COMPRESSED", message=message1)

def b10f():
    
    filename=filedialog.askopenfilename()
    strdec=l1decompress(filename)
    messagebox.showinfo(title="COMPRESSED", message=strdec)

def b11f(image=img,label=lbl):
    imgg=redImage(image)
    photo =PIL.ImageTk.PhotoImage(imgg)
    label.config(image=photo)
    label.image= photo


def b12f(image=img,label=lbl):
    imgg=greenImage(image)
    photo =PIL.ImageTk.PhotoImage(imgg)
    label.config(image=photo)
    label.image= photo

def b13f(image=img,label=lbl):
    imgg=blueImage(image)
    photo =PIL.ImageTk.PhotoImage(imgg)
    label.config(image=photo)
    label.image= photo

def b14f(image=img,label=lbl):
    imgg=grayImage(image)
    photo =PIL.ImageTk.PhotoImage(imgg)
    label.config(image=photo)
    label.image= photo

def b15f(image=img,label=lbl):
    photo =PIL.ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image= photo

B1=Button(lf,text="Compress Grayimage",command=b1f )
B1.pack()
B2=Button(lf2,text="Decompress Gray Image",command=b2f)
B2.pack()

B3=Button(lf,text="Compress Gray Difference Image",command=b3f)
B3.pack()

B4=Button(lf2,text="Decompress Gray Differance Image",command=b4f)
B4.pack()

B5=Button(lf,text="Compress Color Image",command=b5f)
B5.pack()

B6=Button(lf2,text="Dcompress Color Image",command=b6f)
B6.pack()

B7=Button(lf,text="Compress Color DifferenceImage",command=b7f)
B7.pack()

B8=Button(lf2,text="Dcompress Color Difference Image",command=b8f)
B8.pack()

B9=Button(lf3,text="Compress Text",command=b9f)
B9.pack()

B10=Button(lf3,text="Decompress Text",command=b10f)
B10.pack()

B11=Button(top,bg='red',text="REDt",command=b11f)
B11.place(x=300,y=225)

B12=Button(top,bg='green' ,text="GREEN",command=b12f)
B12.place(x=375,y=225)

B13=Button(top,bg='blue',text="BLUE",command=b13f)
B13.place(x=450,y=225)

B14=Button(top,bg='gray',text="GRAY",command=b14f)
B14.place(x=525,y=225)

B15=Button(top,text="ORIGINAL",command=b15f)
B15.place(x=225,y=225)
top.mainloop()
