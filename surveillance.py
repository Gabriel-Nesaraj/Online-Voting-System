import cv2
import numpy as np
import sqlite3
import face_recognition as fr
import numpy as np
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
import os
import imutils
import math
import winsound
from datetime import datetime
from subprocess import call
import tkinter.messagebox as tmsg
# from sklearn.metrics import accuracy_score

#####################################################################################################

class App:
	def __init__(self,video_source=0):
		self.appname="ONLINE VOTING SYSTEM"
		self.window=Tk()
		self.window.title(self.appname)
		self.window.geometry('1350x720')
		self.window.state("zoomed")
		self.window["bg"]='#386184'
		self.video_source=video_source
		self.vid=myvideocapture(self.video_source)
		self.label=Label(self.window,text=self.appname,font=("bold",20),bg='#386184',fg='white').pack(side=TOP,fill=BOTH)
		self.canvas=Canvas(self.window,height=700,width=700,bg='#386184')
		self.canvas.pack(side=LEFT,fill=BOTH)
		self.detectedPeople=[]
		self.images=self.load_images_from_folder("images")
		self.partyname = StringVar()
		self.Constituency = StringVar()
		self.electorid = StringVar()

		#get image names
		self.images_name=[]
		for img in self.images:
			self.images_name.append(fr.load_image_file(os.path.join("images",img)))
		
		#get their encodings
		self.encodings=[]
		for img in self.images_name:
			self.encodings.append(fr.face_encodings(img)[0])


		#get id from images
		self.known_face_names=[]
		for name in self.images:
			self.known_face_names.append((os.path.splitext(name)[0]).split('.')[1])


		self.face_locations=[]
		self.face_encodings=[]
		self.face_names=[]
		self.process_this_frame=True



		print(self.known_face_names)
		self.faceDetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
		self.recognizer = cv2.face.LBPHFaceRecognizer_create()
		# self.recognizer.read("recognizer\\training_data.yml")
		self.Id=0


		#== showing treeview

		self.tree = ttk.Treeview(self.window, column=("column1", "column2", "column3", "column4", "column5"),
								 show='headings')

		self.tree.heading("#1", text="ID")
		self.tree.column("#1", minwidth=0, width=50, stretch=NO)

		self.tree.heading("#2", text="NAME")
		self.tree.column("#2", minwidth=0, width=150, stretch=NO)

		self.tree.heading("#3", text="Elector Card No")
		self.tree.column("#3", minwidth=0, width=150, stretch=NO)

		self.tree.heading("#4", text="Constituency")
		self.tree.column("#4", minwidth=0, width=100, stretch=NO)

		self.tree.heading("#5", text="MATCHING %")
		self.tree.column("#5", minwidth=0, width=120, stretch=NO)

		ttk.Style().configure("Treeview.Heading", font=('Calibri', 13, 'bold'), foreground="red", relief="flat")

		self.tree.place(x=710, y=50)

		self.update()
		self.window.mainloop()

	def castVote(self):
		# call(["python", "electionResult.py"])
		Gender = IntVar()

		def setValueparty():
			gender = Gender.get()
			if (gender == 1):
				gen1 = 'BJP'
			if (gender == 2):
				gen1 = 'CPJ'
			if (gender == 3):
				gen1 = 'Cycle'
			if (gender == 4):
				gen1 = 'Elephant'

			self.partyname.set(gen1)
			self.savevotes()
			closewindow()

		def closewindow():
			root.destroy()

		root = Toplevel(self.window)
		root.geometry('800x500')
		root.minsize(800, 500)
		root.maxsize(800, 500)

		root.title("ONLINE VOTING")
		root.configure(bg="#386184")



		label_0 = Label(root, text="ONLINE VOTING SYSTEM", width=50, font=("bold", 20), anchor=CENTER, bg="#386184",
						fg="white")
		label_0.place(x=0, y=0)

		x = 'BJP.png'
		image = Image.open('partylogo/' + x)
		image = image.resize((50, 50), Image.ANTIALIAS)
		photo1 = ImageTk.PhotoImage(image)
		photo_l1 = Label(root,image=photo1, width=50, height=50).place(x=400, y=50)
		Radiobutton(root, text="", padx=1, variable=Gender, value="1").place(x=365, y=60)

		y = 'CPJ.png'
		image = Image.open('partylogo/' + y)
		image = image.resize((50, 50), Image.ANTIALIAS)
		photo2 = ImageTk.PhotoImage(image)
		photo_l2 = Label(root, image=photo2, width=50, height=50).place(x=400, y=120)
		Radiobutton(root, text="", padx=1, variable=Gender, value="2").place(x=365, y=130)

		yz = 'Cycle.png'
		image = Image.open('partylogo/' + yz)
		image = image.resize((50, 50), Image.ANTIALIAS)
		photo3 = ImageTk.PhotoImage(image)
		photo_l3 = Label(root,image=photo3, width=50, height=50).place(x=400, y=190)
		Radiobutton(root, text="", padx=1, variable=Gender, value="3").place(x=365, y=200)

		yzz = 'Elephant.png'
		image = Image.open('partylogo/' + yzz)
		image = image.resize((50, 50), Image.ANTIALIAS)
		photo4 = ImageTk.PhotoImage(image)
		photo_l4 = Label(root, image=photo4, width=50, height=50).place(x=400, y=260)
		Radiobutton(root, text="", padx=1, variable=Gender, value="4").place(x=365, y=270)

		Button(root, text='Submit', width=10, height=2, bg='blue', fg='white', font=("bold", 11),
			   command=setValueparty).place(x=300,y=340)
		Button(root, text='Cancel', width=10, height=2, bg='blue', fg='white', font=("bold", 11), command=closewindow).place(
			x=410,
			y=340)
		root.mainloop()


	def savevotes(self):
		consti = self.Constituency.get()
		party = self.partyname.get()
		electorid = self.electorid.get()

		today = datetime.today().strftime('%Y-%m-%d')

		if (consti != "" and party != "" and electorid != "" and today != "" ):
			conn = sqlite3.connect('voterDB.db')
			with conn:
				cursor = conn.cursor()
			# cursor.execute('CREATE TABLE IF NOT EXISTS People (Fullname TEXT,Email TEXT,Gender TEXT,country TEXT,Programming TEXT)')
			cursor.execute('INSERT INTO electionResult(Date,ElectorCardNo,PartyName,Constituency)'
						   'VALUES(?,?,?,?)',(today, electorid, party, consti))

			# cursor.execute('INSERT INTO People (Name,Gender,Father,Mother,Religion,Blood,Bodymark,Nationality,Crime) VALUES(?,?,?,?,?,?,?,?,?)',(name,gen1,father,mother,religion,bl,body,nat,crime))
			conn.commit()

		tmsg.showinfo("Success","Vote Recorded Successfully")

		self.window.destroy()

	def load_images_from_folder(self,folder):
		images=[]
		for filename in os.listdir(folder):
			images.append(filename)
		return images

	def doubleclick(self,event):
		item=self.tree.selection()
		itemid=self.tree.item(item,"values")
		ide=itemid[0]
		ide=(int(ide))
		self.viewdetail(ide)

	def viewdetail(self,a):
		conn = sqlite3.connect("voterDB.db")
		cur = conn.cursor()
		cur.execute("SELECT * FROM voter_details where Id="+str(a))
		rows = cur.fetchall()
		print(rows)
		for row in rows:
			label_n = Label(self.window, text=row[1],bg="#382273",fg='white',width=20,font=("bold", 12))
			label_n.place(x=1130,y=400)
			label_f = Label(self.window, text=row[2],bg="#382273",fg='white',width=20,font=("bold", 12))
			label_f.place(x=1130,y=430)
			label_m = Label(self.window, text=row[3],bg="#382273",fg='white',width=20,font=("bold", 12))
			label_m.place(x=1130,y=460)
			label_g = Label(self.window, text=row[4],bg="#382273",fg='white',width=20,font=("bold", 12))
			label_g.place(x=1130,y=490)
			label_r = Label(self.window, text=row[5],bg="#382273",fg='white',width=20,font=("bold", 12))
			label_r.place(x=1130,y=520)
			label_bl = Label(self.window, text=row[6],bg="#382273",fg='white',width=20,font=("bold", 12))
			label_bl.place(x=1130,y=550)
			label_b = Label(self.window, text=row[7],bg="#382273",fg='white',width=20,font=("bold", 12))
			label_b.place(x=1130,y=580)
			self.Constituency.set(row[7])
			self.electorid.set(row[4])
		conn.close()
		label_name = Label(self.window, text="Name",bg="#382273",fg='yellow',width=20,font=("bold", 12))
		label_name.place(x=930,y=400)
		label_father = Label(self.window, text="Father's Name",bg="#382273",fg='yellow',width=20,font=("bold", 12))
		label_father.place(x=930,y=430)
		label_mother = Label(self.window, text="Gender",bg="#382273",fg='yellow',width=20,font=("bold", 12))
		label_mother.place(x=930,y=460)
		label_gender = Label(self.window, text="Elector Card No",bg="#382273",fg='yellow',width=20,font=("bold", 12))
		label_gender.place(x=930,y=490)
		label_religion = Label(self.window, text="Address",bg="#382273",fg='yellow',width=20,font=("bold", 12))
		label_religion.place(x=930,y=520)
		label_bloodgroup = Label(self.window, text="Nationality",bg="#382273",fg='yellow',width=20,font=("bold", 12))
		label_bloodgroup.place(x=930,y=550)
		label_body = Label(self.window, text="Constituency",bg="#382273",fg='yellow',width=20,font=("bold", 12))
		label_body.place(x=930,y=580)

		Button(self.window, text='Cast Your Vote', width=15, font=("bold", 10), bg='brown', height=2, fg='white',
			   command=self.castVote).place(x=970, y=620)
		Button(self.window, text='Cancel', width=15, font=("bold", 10), bg='brown', height=2, fg='white',
			   command=self.destroywin).place(x=1140, y=620)

		x='user.'+str(a)+".png"
		image=Image.open('images/'+x)
		image = image.resize((180,180), Image.ANTIALIAS)
		photo=ImageTk.PhotoImage(image)
		photo_l=Label(image=photo,width=180,height=180).place(x=720,y=410).pack()

	def destroywin(self):
		self.window.destroy()

	def getProfile(self,id):
	    conn=sqlite3.connect("voterDB.db")
	    cmd="SELECT ID,ElectorName,ElectorCardNo,Constituency FROM voter_details where ID="+str(id)
	    cursor=conn.execute(cmd)
	    profile=None
	    for row in cursor:
	        profile=row
	        break
	    
	    conn.close()
	    return profile

	
	def showPercentageMatch(self,face_distance,face_match_threshold=0.6):
		if face_distance > face_match_threshold:
			range = (1.0 - face_match_threshold)
			linear_val = (1.0 - face_distance) / (range * 2.0)
			return linear_val
		else:
			range = face_match_threshold
			linear_val = 1.0 - (face_distance / (range * 2.0))
			return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))

	def update(self):
		isTrue,frame=self.vid.getframe()
		if isTrue:
			self.photo=ImageTk.PhotoImage(image=Image.fromarray(frame))
			self.canvas.create_image(0,0,image=self.photo,anchor=NW)

			#Resize the frame of video to 1/4 size for fast process
			small_frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)

			#convert the image to BGR color(openCV) to RGB color(face_recognition)
			rgb_small_frame=small_frame[:,:,::-1]

			#Only process every other frame of video to save time
			if self.process_this_frame:
				#find all the faces and face encodings in the current frame of video
				self.face_locations=fr.face_locations(rgb_small_frame)
				self.face_encodings=fr.face_encodings(rgb_small_frame,self.face_locations)
				self.face_names=[]
				for face_encoding in self.face_encodings:
					#See if the face is a match for known face(s)
					matches=fr.compare_faces(self.encodings,face_encoding)
					Id=0
					face_distances=fr.face_distance(self.encodings,face_encoding)
					best_match_index=np.argmin(face_distances)

					percent=self.showPercentageMatch(face_distances[best_match_index])
					
					#acc = accuracy_score(self.encodings[best_match_index], face_encoding)

					if matches[best_match_index]:
						Id=self.known_face_names[best_match_index]
					self.face_names.append(Id)

			# self.gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			# faces=self.faceDetect.detectMultiScale(self.gray, 1.2, 5)
			# for(x,y,w,h) in faces:
			# 	cv2.rectangle(frame,(x,y),(x+w,y+h),(225,0,0),2)
			# 	Id, confidence = self.recognizer.predict(self.gray[y:y+h,x:x+w])
			
					profile=self.getProfile(Id)
					confidence=str(round(percent*100,2))+"%"

					if profile not in self.detectedPeople and profile!=None:
						self.detectedPeople.append(profile)
						profilex=list(profile)
						profilex.append(confidence)
						profile=tuple(profilex)
						self.tree.insert("", 'end', values=profile)
						self.tree.bind("<Double-1>",self.doubleclick)
						winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

					print(profile)
			self.process_this_frame=not self.process_this_frame
			# #display the result
			# for(top,right,bottom,left),name in zip(self.face_locations,self.face_names):
			# 	top*=4
			# 	right*=4
			# 	bottom*=4
			# 	left*=4
			# 	cv2.rectangle(frame,(left,top),(right,bottom),(0,0,225),2)
			# 	cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,225),cv2.FILLED)
			# 	font=cv2.FONT_HERSHEY_DUPLEX
			# 	cv2.putText(frame,name,(left+6,bottom-6),font,1.0,(225,225,225),1)

		self.window.after(15,self.update)

#####################################################################################################
class myvideocapture:
	def __init__(self,video_source=0):
		self.vid=cv2.VideoCapture(video_source)
		if not self.vid.isOpened():
			raise ValueError("unable to open",video_source)

		self.width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

	def getframe(self):
		if self.vid.isOpened():
			ret, frame = self.vid.read()
			frame=imutils.resize(frame,height=700)
			if ret:
				return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
			else:
				return (ret, None)
		else:
			return (ret, None)

	def __del__(self):
		if self.vid.isOpened():
			self.vid.release()

if __name__=="__main__":
	App()
