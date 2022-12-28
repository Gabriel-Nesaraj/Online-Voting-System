from tkinter import *
import shutil
from PIL import ImageTk,Image
import sqlite3
from tkinter import filedialog
import tkinter.messagebox as tmsg
from subprocess import call
from tkcalendar import Calendar, DateEntry
from datetime import datetime

def register():
    call(["python", "registerGUI.py"])
def VideoSurveillance():
    call(["python", "surveillance.py"])

root = Tk()
root.geometry('800x500')
root.minsize(800,500)
root.maxsize(800,500)

root.title("ONLINE VOTING SYSTEM")
root.configure(bg="#386184")

seldate = StringVar()
bjpcount=StringVar()
cjpcount=StringVar()
cyclecount=StringVar()
elephantcount=StringVar()
Constituency=StringVar()

def closewin():
    root.destroy()
def getdata():
    Constituencyval = Constituency.get()
    selectdate = cal.get()
    print(Constituencyval)
    print(selectdate)

    conn = sqlite3.connect("voterDB.db")
    cur = conn.cursor()

    cur.execute("SELECT PartyName FROM electionResult"
                " where Date= '" + str(selectdate) + "' and Constituency= '"+ str(Constituencyval) +"'")
    rows = cur.fetchall()

    BJP = 0;
    CPJ = 0;
    Cycle = 0;
    Elephant = 0;

    print(rows)

    for row in rows:
        if(row[0] == "BJP"):
            BJP += 1
        elif(row[0] == "CPJ"):
            CPJ += 1
        elif (row[0] == "Cycle"):
            Cycle += 1
        elif (row[0] == "Elephant"):
            Elephant += 1

    bjpcount.set(str(BJP))
    cjpcount.set(str(CPJ))
    cyclecount.set(str(Cycle))
    elephantcount.set(str(Elephant))

    conn.close()

label_0 = Label(root, text="ONLINE VOTING SYSTEM",width=50,font=("bold", 20),anchor=CENTER,bg="#386184",fg="white")
label_0.place(x=0,y=0)

list1 = ['Section A','Section B','Section C','Section D'];

droplist=OptionMenu(root,Constituency, *list1)
droplist.config(width=16)
Constituency.set('Select Constituency')
droplist.place(x=150,y=80)

#Create a Calendar using DateEntry
cal = DateEntry(root, width= 16, background= "magenta3", foreground= "white",bd=2, textVariable = seldate, date_pattern='yyyy-MM-dd')
cal.place(x=360,y=80)

Button(root, text='Submit',width=5,height=1,bg='blue',fg='white',font=("bold", 11),command=getdata).place(x=530,y=80)
Button(root, text='Cancel',width=5,height=1,bg='blue',fg='white',font=("bold", 11),command=closewin).place(x=600,y=80)



x='BJP.png'
image=Image.open('partylogo/'+x)
image = image.resize((50,50), Image.ANTIALIAS)
photo1=ImageTk.PhotoImage(image)
photo_l1=Label(image=photo1,width=50,height=50).place(x=400,y=150)
Entry(root,width=10,textvar=bjpcount).place(x=305,y=160)

y='CPJ.png'
image=Image.open('partylogo/'+y)
image = image.resize((50,50), Image.ANTIALIAS)
photo2=ImageTk.PhotoImage(image)
photo_l2=Label(image=photo2,width=50,height=50).place(x=400,y=220)
Entry(root,width=10,textvar=cjpcount).place(x=305,y=230)

yz='Cycle.png'
image=Image.open('partylogo/'+yz)
image = image.resize((50,50), Image.ANTIALIAS)
photo3=ImageTk.PhotoImage(image)
photo_l3=Label(image=photo3,width=50,height=50).place(x=400,y=290)
Entry(root,width=10,textvar=cyclecount).place(x=305,y=300)

yzz='Elephant.png'
image=Image.open('partylogo/'+yzz)
image = image.resize((50,50), Image.ANTIALIAS)
photo4=ImageTk.PhotoImage(image)
photo_l4=Label(image=photo4,width=50,height=50).place(x=400,y=360)
Entry(root,width=10,textvar=elephantcount).place(x=305,y=370)

root.mainloop()