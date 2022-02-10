#FREE HOMEWORK MANAGER 2022
#Created for SST Computing+ Coursework 2022
#Developed By: Group S - Ethan Wang JQ (402), Joshua Lim ZK (407), Yeo ZW Quentin (402)
#Version: 1.0
#Open Sourced on GITHUB: https://github.com/JoshuaLimZK/FHM2022

#IMPORT TKINTER LIBRARY FOR GUI + EXTRA WIDGETS
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

#IMPORT REGEX FOR DATA VALIDATION (pls gib extra points, this gave me a headache)
import re

#IMPORT DATETIME FOR HANDING TIME
import datetime

#PYREBASE SETUP
#pyrebase is a simple third-party firebase wrapper for python
import pyrebase

#requests and json used for handing login & signup errors
import requests
import json

fbconfig = {
  "apiKey": "AIzaSyAq2OeJ1K1u2rPZG7UBw691gYlpWF-DSKo",
  "authDomain": "fhm2022-90ce4.firebaseapp.com",
  "databaseURL": "https://fhm2022-90ce4-default-rtdb.asia-southeast1.firebasedatabase.app",
  "storageBucket": "fhm2022-90ce4.appspot.com"
}

firebase = pyrebase.initialize_app(fbconfig)
auth = firebase.auth()
db = firebase.database()

#Create a window
root = Tk()
root.title("Free Homework Manager 2022")

class app:
    def __init__(self, master):
        self.master = master
        self.login()

    #Login Page
    def login(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame1 = Frame(self.master, width=300, height=300)
        self.frame1.pack()

        self.emailIn = StringVar()
        self.passwordIn = StringVar()

        self.emailLb = ttk.Label(self.frame1, text='Email:')
        self.emailEn = ttk.Entry(self.frame1, width=30, textvariable=self.emailIn)
        self.passLb = ttk.Label(self.frame1, text='Password:')
        self.passEn = ttk.Entry(self.frame1, width=30, show='*', textvariable=self.passwordIn)

        self.loginBn = ttk.Button(self.frame1, text='Login', command=self.loginCheck)
        self.regBn = ttk.Button(self.frame1, text="Register", command=self.register)

        self.emailLb.grid(row = 0, column = 0, sticky = E)
        self.passLb.grid(row = 1, column = 0, sticky = E)
        self.emailEn.grid(row = 0, column = 1, sticky = W)
        self.passEn.grid(row = 1, column = 1, sticky = W)
        self.loginBn.grid(row = 2, column = 0, sticky = E)
        self.regBn.grid(row = 2, column = 1, sticky = W)
    
    #Registration for account Page
    def register(self):
        for i in self.master.winfo_children():
            i.destroy()
        
        self.frame2 = Frame(self.master, width=300, height=300)
        self.frame2.pack()

        self.emailIn = StringVar()
        self.passwordIn = StringVar()

        self.emailLb = ttk.Label(self.frame2, text='Email:')
        self.emailEn = ttk.Entry(self.frame2, width=30, textvariable=self.emailIn)
        self.passLb = ttk.Label(self.frame2, text='Password:')
        self.passEn = ttk.Entry(self.frame2, width=30, show='*', textvariable=self.passwordIn)

        self.loginBn = ttk.Button(self.frame2, text='Register an Account', command=self.registerAcc)
        self.regBn = ttk.Button(self.frame2, text="Back to Login", command=self.login)

        self.emailLb.grid(row = 0, column = 0, sticky = E)
        self.passLb.grid(row = 1, column = 0, sticky = E)
        self.emailEn.grid(row = 0, column = 1, sticky = W)
        self.passEn.grid(row = 1, column = 1, sticky = W)
        self.loginBn.grid(row = 2, column = 0, sticky = E)
        self.regBn.grid(row = 2, column = 1, sticky = W)
    
    #Function for login validation
    def loginCheck(self):
        try:
            self.user = auth.sign_in_with_email_and_password(self.emailIn.get(), self.passwordIn.get())
            print(self.user)
            self.home()
        except requests.exceptions.HTTPError as exception:
            error_json = exception.args[1]
            error = json.loads(error_json)['error']['message']
            self.loginErrorHandling(error)

    #Function for creating new account
    def registerAcc(self):
        try:
            auth.create_user_with_email_and_password(self.emailIn.get(), self.passwordIn.get())

        except requests.exceptions.HTTPError as exception:
            error_json = exception.args[1]
            error = json.loads(error_json)['error']['message']
            self.loginErrorHandling(error)
        
        else:
            self.loginCheck(self)

    def loginErrorHandling(self, error):

        messagebox.showerror("showerror", "Error: {}".format(error))

    #Function to listen for changes in database
    def stream_handler(self, message):
        return message["data"]

    #Home Page
    def home(self):
        for i in self.master.winfo_children():
            i.destroy()
        
        self.frame3 = Frame(self.master, width=300, height=300)
        self.frame3.pack()

        self.menuFrame = Frame(self.frame3, width=100, height=300, bg='#cccccc')
        self.menuFrame.grid(row=0, column=0, sticky=N)

        self.mainFrame = Frame(self.frame3, width=200, height=300)
        self.mainFrame.grid(row=0, column=1, sticky=N)

        self.createNewBn = Button(self.menuFrame, text='Create New', command=self.createNew, highlightbackground='#cccccc')
        self.createNewBn.grid(row = 0, column = 0, sticky = EW)

        self.manageBn = Button(self.menuFrame, text='Manage Homework', command=self.manage, highlightbackground='#cccccc')
        self.manageBn.grid(row = 1, column = 0, sticky = EW)

        self.signoutBn = Button(self.menuFrame, text='Sign Out', command=self.login, highlightbackground='#cccccc')
        self.signoutBn.grid(row = 2, column = 0, sticky = EW)
        
        self.timeTableGnBn = Button(self.menuFrame, text='Generate Time Table', command=self.timeTable, highlightbackground='#cccccc')
        self.timeTableGnBn.grid(row=3, column=0, sticky=EW)

        self.data = db.child("data").child(self.user['localId']).get()

        rowCounter = 1

        nameTitle = Label(self.mainFrame, text='Name of Homework').grid(row=0, column=0, sticky=W)
        dueTitle = Label(self.mainFrame, text='Due Date').grid(row=0, column=1, sticky=W)

        for i in self.data.each():
            
            self.nameData = ttk.Label(self.mainFrame, text=i.val()["name"])
            self.dateData = ttk.Label(self.mainFrame, text=i.val()["date"])

            self.nameData.grid(row = rowCounter, column = 0, sticky = E)
            self.dateData.grid(row = rowCounter, column = 1, sticky = E)
            
            rowCounter += 1

    #Create New Homework Page
    def createNew(self):
        for i in self.master.winfo_children():
            i.destroy()

        self.frame4 = Frame(self.master, width=300, height=300)
        self.frame4.pack()
        
        self.nameVar = StringVar()
        self.timeTakenVar = StringVar()
        self.dateVar = StringVar()

        self.nameLb = ttk.Label(self.frame4, text='Name:')
        self.timeTakenLb = ttk.Label(self.frame4, text='Time Needed (Mins)')
        self.dateLb = ttk.Label(self.frame4, text='Due Date:')

        self.nameEn = ttk.Entry(self.frame4, width=30, textvariable=self.nameVar)
        self.timeTakenEn = ttk.Entry(self.frame4, width=30, textvariable=self.timeTakenVar)
        self.dateSelect = DateEntry(self.frame4, width=30, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', textvariable=self.dateVar)

        self.nameLb.grid(row = 0, column = 0, sticky = E)
        self.timeTakenLb.grid(row = 1, column = 0, sticky = E)
        self.dateLb.grid(row = 2, column = 0, sticky = E)

        self.nameEn.grid(row = 0, column = 1, sticky = W)
        self.timeTakenEn.grid(row = 1, column = 1, sticky = W)
        self.dateSelect.grid(row = 2, column = 1, sticky = W)

        self.confirmBn = ttk.Button(self.frame4, text='Confirm', command=self.confirmAdd)
        self.cancelBn = ttk.Button(self.frame4, text='Cancel', command=self.home)

        self.cancelBn.grid(row = 3, column = 0, sticky = E)
        self.confirmBn.grid(row = 3, column = 1, sticky = W)

    #Function to push new homework to database
    def confirmAdd(self):
        regexTestCase = "^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$"
        if re.match(regexTestCase, self.dateVar.get()) and self.timeTakenVar.get().isdigit():
            data = {"name": self.nameVar.get(), "timeTaken": int(self.timeTakenVar.get()), "date": self.dateVar.get()}
            db.child("data").child(self.user['localId']).push(data)
            self.home()
        else:
            messagebox.showerror("Showerror", "Please enter a valid date and time taken")
            return

    #Manage current homework page
    def manage(self):
        for i in self.master.winfo_children():
            i.destroy()

        print("bruh")

        self.frame5 = Frame(self.master, width=300, height=300)
        self.frame5.pack()

        self.data = db.child("data").child(self.user['localId']).get()

        rowCounter = 1

        nameTitle = Label(self.frame5, text='Name of Homework').grid(row=0, column=0, sticky=W)
        dueTitle = Label(self.frame5, text='Due Date').grid(row=0, column=1, sticky=W)
        try:
            for i in self.data.each():
                
                self.nameData = Label(self.frame5, text=i.val()["name"])
                self.dateData = Label(self.frame5, text=i.val()["date"])
                self.editBn = Button(self.frame5, text='Edit', command=lambda j=i: self.editData(j.key(), j.val()["name"], j.val()["timeTaken"], j.val()["date"]))
                self.deleteBn = Button(self.frame5, text='Delete', command=lambda: self.deleteData(j.key(), j.val()["name"]))

                self.nameData.grid(row = rowCounter, column = 0, sticky = E)
                self.dateData.grid(row = rowCounter, column = 1, sticky = E)
                self.editBn.grid(row = rowCounter, column = 2, sticky = EW)
                self.deleteBn.grid(row = rowCounter, column = 3, sticky = EW)
            
                rowCounter += 1
        except:
            pass
        backBn = Button(self.frame5, text='Back', command=self.home).grid(row=rowCounter, column=0, sticky=W)
        backBn.grid(row=rowCounter, column=1, sticky=W)

    #Edit Data
    def editData(self, key, name, timeTaken, date):

        for i in self.master.winfo_children():
            i.destroy()

        self.frame7 = Frame(self.master, width=300, height=300)
        self.frame7.pack()
        
        self.nameVar = StringVar()
        self.timeTakenVar = IntVar()
        self.dateVar = StringVar()

        self.nameVar.set(name)
        self.timeTakenVar.set(timeTaken)
        self.dateVar.set(date)

        self.nameLb = ttk.Label(self.frame7, text='Name:')
        self.timeTakenLb = ttk.Label(self.frame7, text='Time Needed (Mins):')
        self.dateLb = ttk.Label(self.frame7, text='Due Date:')

        self.nameEn = ttk.Entry(self.frame7, width=30, textvariable=self.nameVar)
        self.timeTakenEn = ttk.Entry(self.frame7, width=30, textvariable=self.timeTakenVar)
        self.dateSelect = DateEntry(self.frame7, width=30, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', textvariable=self.dateVar)

        self.nameLb.grid(row = 0, column = 0, sticky = E)
        self.timeTakenLb.grid(row = 1, column = 0, sticky = E)
        self.dateLb.grid(row = 2, column = 0, sticky = E)

        self.nameEn.grid(row = 0, column = 1, sticky = W)
        self.timeTakenEn.grid(row = 1, column = 1, sticky = W)
        self.dateSelect.grid(row = 2, column = 1, sticky = W)

        self.confirmBn = ttk.Button(self.frame7, text='Confirm', command=lambda: self.confirmEdit(key))
        self.cancelBn = ttk.Button(self.frame7, text='Cancel', command=lambda: self.manage())

        self.cancelBn.grid(row = 3, column = 0, sticky = E)
        self.confirmBn.grid(row = 3, column = 1, sticky = W)

    #Confirm Edit
    def confirmEdit(self, key):
        regexTestCase = "^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$"
        if re.match(regexTestCase, self.dateVar.get()) and self.timeTakenVar.get().isdigit():
            data = {"name": self.nameVar.get(), "timeTaken": int(self.timeTakenVar.get()), "date": self.dateVar.get()}
            db.child("data").child(self.user['localId']).update(data)
            self.manage()
        else:
            messagebox.showerror("Showerror", "Please enter a valid date and time taken")
            return
    
    #Delete Data
    def deleteData(self, key, name):

        print(key)
        proceed = messagebox.askokcancel("askokcancel", "Are you sure you want to delete \"{}\"".format(name))

        if proceed:
            db.child("data").child(self.user['localId']).child(key).remove()
        
        self.manage()

    #Time Table Page
    def timeTable(self):
        for i in self.master.winfo_children():
            i.destroy()

        self.frame6 = Frame(self.master, width=300, height=300)
        self.frame6.pack()

        data = db.child("data").child(self.user['localId']).get()
        sortedDataByDate = db.sort(data, "date")

        self.workTimingBn = Button(self.frame6, text='Manage Work Timing', command=self.workTiming).grid(row=0, column=0, sticky=W)

        timings = db.child("timing").child(self.user['localId']).get()
        if timings.val()["startTiming"] == "":
            startTiming = "Not Set"
        else:
            startTiming = timings.val()["startTiming"]

        if timings.val()["endTiming"] == "":
            endTiming = "Not Set"
        else:
            endTiming = timings.val()["endTiming"]

        Label(self.frame6, text='Start Time:').grid(row=1, column=0, sticky=W)
        Label(self.frame6, text='End Time:').grid(row=2, column=0, sticky=W)
        Label(self.frame6, text='Start Time: {}'.format(startTiming)).grid(row=1, column=1, sticky=W)
        Label(self.frame6, text='End Time: {}'.format(endTiming)).grid(row=2, column=1, sticky=W)


    def workTiming(self):
        for i in self.master.winfo_children():
            i.destroy()
        
        self.frame7 = Frame(self.master, width=300, height=300)
        self.frame7.pack()
        
        self.startTimingVar = StringVar()
        self.endTimingVar = StringVar()

        Label(self.frame7, text='Work Timing').grid(row=0, column=0, sticky=W)
        Entry(self.frame7, width=30, textvariable=self.startTimingVar).grid(row=1, column=1, sticky=W)
        Label(self.frame7, text='Start Timing (24H Format, HHMM):').grid(row=1, column=0, sticky=W)
        Entry(self.frame7, width=30, textvariable=self.endTimingVar).grid(row=2, column=1, sticky=W)
        Label(self.frame7, text='End Timing (24H Format, HHMM):').grid(row=2, column=0, sticky=W)
        
        Button(self.frame7, text='Confirm', command=lambda:self.confirmWorkTiming(self.startTimingVar.get(), self.endTimingVar.get())).grid(row=3, column=0, sticky=E)
        Button(self.frame7, text='Cancel', command=self.timeTable).grid(row=3, column=1, sticky=W)

    def confirmWorkTiming(self, startTiming, endTiming):
        regexTestCase = "^([01]\d|2[0-4]):?([0-5]\d)$"
        if re.match(regexTestCase, startTiming) and re.match(regexTestCase, endTiming) and startTiming < endTiming:
            db.child("timing").child(self.user['localId']).set({"startTiming": startTiming, "endTiming": endTiming})
            self.timeTable()
        else:
            messagebox.showerror("Error", "Please enter a valid time")
            self.workTiming()
        
        
app(root)
root.mainloop()