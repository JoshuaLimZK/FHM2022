#IMPORT TKINTER LIBRARY FOR GUI + EXTRA WIDGETS
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

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
        top= Toplevel(root)
        top.title("Error Encountered")
        lb = ttk.Label(top, text="Error: {}".format(error))
        lb.pack()

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
        self.createNewBn.grid(row = 0, column = 0, sticky = E)

        self.manageBn = Button(self.menuFrame, text='Manage Homework', command=self.manage, highlightbackground='#cccccc')
        self.manageBn.grid(row = 1, column = 0, sticky = E)

        self.signoutBn = Button(self.menuFrame, text='Sign Out', command=self.login, highlightbackground='#cccccc')
        self.signoutBn.grid(row = 2, column = 0, sticky = E)

        self.settingsBn = Button(self.menuFrame, text='Settings', command=self.settings, highlightbackground='#cccccc')
        self.settingsBn.grid(row = 3, column = 0, sticky = E)

        self.data = db.child("data").child(self.user['localId']).get()

        rowCounter = 0

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
        self.timeTakenVar = IntVar()
        self.dateVar = StringVar()

        self.nameLb = ttk.Label(self.frame4, text='Name:')
        self.timeTakenLb = ttk.Label(self.frame4, text='Time Needed:')
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
        data = {"name": self.nameVar.get(), "timeTaken": self.timeTakenVar.get(), "date": self.dateVar.get()}
        db.child("data").child(self.user['localId']).push(data)
        self.home()

    #Manage current homework page
    def manage(self):
        for i in self.master.winfo_children():
            i.destroy()

    #Settings Page
    def settings(self):
        for i in self.master.winfo_children():
            i.destroy()

        self.frame5 = Frame(self.master, width=300, height=300)
        self.frame5.pack()

app(root)
root.mainloop()