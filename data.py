#import model
from  tkinter import *
from tkinter import messagebox as mb 
import os
import cv2
import numpy as np
import tkinter.font as font
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def error():
    mb.showinfo('OK',"Plese Enter Name")
    
def call():
    name= entry.get()
    if(name==''):
        error()
    else:
        res = mb.askquestion('Update Data?', 'Do you want to Delete existing file and Add new?') 
        if res == 'yes' : 
            update()
        else : 
            mb.showinfo('Return', 'Returning to main application')

def capture(path):
    def face_extractor(img):
        cropped_face=None
        faces = face_classifier.detectMultiScale(img, 1.3, 5,minSize=(75,75))
        for (x,y,w,h) in faces:
            x=x-10
            y=y-10
            cropped_face = img[y:y+h+50, x:x+w+50]
        return cropped_face
    cap = cv2.VideoCapture(0)
    count = 0
    max_count=300
    try:
        while True:            
            ret, frame = cap.read()
            if face_extractor(frame) is not None:
                count += 1
                face=face_extractor(frame)
                file_name_path =path+str(count) + '.jpg'
                cv2.imwrite(file_name_path, face)
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (222,255,200), 2)
                cv2.imshow('Capturing ', face)
            if cv2.waitKey(1) == 13 or count == max_count: #13 is the Enter Key
                break
    except:
        pass
    cap.release()
    cv2.destroyAllWindows()      
    print("Collected Samples")

def create_folder(name):
    parent_dir1 = "data/"
    path1 = os.path.join(parent_dir1, name)
    try: 
        os.makedirs(path1, exist_ok = True)
        print("Directory '%s' created successfully for user " % name) 
    except OSError as error: 
        print("Directory '%s' can not be created for user " % name)
    return path1+'/'
def remove(name):
    path = "data/"+name
    try:
        os.chmod(path, 0o777)

        os.remove(path)
        print("Directory '%s' Deleted successfully for user ",name) 
    except OSError as error: 
        print("Directory '%s' Not Found for user " ,error)
    
    
def new_data():
    name= entry.get()
    if(name==''):
        error()
    else:
        path=create_folder(name)
        capture(path)
        mb.showinfo("Done","Taken Your Images.")  
    

def update():
    name=entry.get()
    if(name==''):
        error()
    else:
        remove(name)
        path=create_folder(name)
        capture(path)
        mb.showinfo("Done","Updated ur Images.")  
def delete():
    name=entry.get()
    if(name==''):
        error()
    else:
        remove(name)
        
def train():
    x=0


window = Tk()
window.geometry("500x250")
window.maxsize(600, 250)
window.minsize(300,250)
window.title("Data Collector")
main_frame = Frame(window, )
main_frame.pack( fill= BOTH ,side=  TOP)

frame = Frame(main_frame)
frame.pack( fill= BOTH ,side=  TOP)

frame2 = Frame(main_frame)
frame2.pack( fill= BOTH,side=  BOTTOM)


frame3 = Frame(main_frame)
frame3.pack( fill= BOTH,side=  BOTTOM)


label =  Label(frame,text = "ENTER USER NAME ↴",font=('calibre',15,'normal') )
label.pack(side = LEFT, expand = True,padx=5, pady=15)

entry =  Entry(frame,font=('calibre',20,'normal') )
entry.pack(side = LEFT, expand = True ,padx=5, pady=15)

b1 =  Button(frame2, text = "New Data" ,bg='#293d3d',
             fg = "#66d9ff" ,font=('calibre',15,'normal') ,command=new_data)
b1.pack(side = LEFT, expand = True,padx=5, pady=15,fill = BOTH)

b2 =  Button(frame2, text = "Update Data" ,bg='#293d3d',
             font=('calibre',15,'normal') , fg = "#3366ff" ,command=call)
b2.pack( side = LEFT, expand = True,padx=5, pady=15 ,fill = BOTH)

b3 =  Button(frame3, text = "delete Data" ,bg='#293d3d',
             font=('calibre',15,'normal') , fg = "#3366ff" ,command=delete)
b3.pack( side = LEFT, expand = True,padx=5, pady=15,fill = BOTH )

b4 =  Button(frame3, text = "Feed Data" ,bg='#293d3d', 
             fg = "#66d9ff" ,font=('calibre',15,'normal') )#,command=model.train)
b4.pack(side = LEFT, expand = True,padx=5, pady=15 ,fill = BOTH)


window.mainloop()
