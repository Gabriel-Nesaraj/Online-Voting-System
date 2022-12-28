from tkinter import *
import shutil
from PIL import ImageTk,Image
import sqlite3
from tkinter import filedialog
import tkinter.messagebox as tmsg
from subprocess import call


def register():
    call(["python", "registerGUI.py"])
def VideoSurveillance():
    call(["python", "surveillance.py"])
def viewResult():
    call(["python", "electionResult.py"])


root = Tk()
root.geometry('800x500')
root.minsize(800,500)
root.maxsize(800,500)

root.title("ONLINE VOTING SYSTEM")
root.configure(bg="#386184")


Fullname=StringVar()
father=StringVar()
var = IntVar()
c=StringVar()
d=StringVar()
var1= IntVar()
file1=""
image=Image.open("image.jpeg")
photo=ImageTk.PhotoImage(image)
photo_label=Label(image=photo,width=800,height=0,bg='white').place(x=0,y=0)
photo_label

label_0 = Label(root, text="ONLINE VOTING SYSTEM",width=50,font=("bold", 20),anchor=CENTER,bg="#386184",fg="white")
label_0.place(x=0,y=0)

Button(root, text='REGISTER NEW VOTER',width=20,height=3,bg='blue',fg='white',font=("bold", 11),command=register).place(x=50,y=340)
Button(root, text='CAST YOUR VOTE',width=20,height=3,bg='red',fg='white',font=("bold", 11),command=VideoSurveillance).place(x=300,y=340)
Button(root, text='ELECTION RESULT',width=20,height=3,bg='blue',fg='white',font=("bold", 11),command=viewResult).place(x=550,y=340)
root.mainloop()