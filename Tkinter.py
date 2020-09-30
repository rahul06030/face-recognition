from tkinter import *
import tkinter.ttk as ttk
import csv
import tkinter as tk
import os
import model

#CREATE CSV FROM LIST
def Start():
    present=[]
    present=model.predict()
    attendance=[]
    allpeople= os.listdir('data/')
    for i in allpeople:
        if i in present:
            attendance.append("Present")
        else:
            attendance.append("Absent")

    csvdict=dict(zip(allpeople, attendance))

    final = {"Name":"Attendance"}
    final.update(csvdict)
    print(final)

    with open("test.csv", "w") as f:
        writer = csv.writer(f)
        for i in final:
          writer.writerow([i, final[i]])
    f.close()


#VIEW CSV
def ViewCSV():
    window=tk.Tk()
    window.title("CSV FILE")
    width = 500
    height = 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry("%dx%d+%d+%d" % (width, height, x, y))
    window.resizable(0, 0)
    TableMargin = Frame(window, width=500)
    TableMargin.pack(side=TOP)

    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("Name", "Attendance"), height=400, selectmode="extended",
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Attendance', text="Attendance", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=120)
    tree.pack()
    with open('test.csv') as f:
      reader = csv.DictReader(f, delimiter=',')
      for row in reader:
        name = row['Name']
        dt = row['Attendance']
        tree.insert("", 0, values=(name, dt))
    window.mainloop()


#SAVE & EXIT
def close(): 
    window.destroy()


window = tk.Tk()
window.title("Face Recognition Project UI")
button = tk.Button(
    text="Start",
    width=22,
    height=3,
    bg="red",
    fg="white",
    command=Start
)
button2 = tk.Button(
    text="View",
    width=22,
    height=3,
    bg="yellow",
    fg="black",
    command=ViewCSV
)
button3 = tk.Button(
    text="Save & Exit",
    width=22,
    height=3,
    bg="green",
    fg="white",
    command=close
)

label=tk.Label(
    text="Welcome to Face Recognition Attendance System",
    height=3,
)
label.pack()
button.pack(side=tk.LEFT)
button2.pack(side=tk.LEFT)
button3.pack(side=tk.LEFT)




