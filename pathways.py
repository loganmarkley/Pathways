# File: Pathways.py
# Desc: This program contains the GUI and database implementation for our
#       company matchmaking application, Pathways.
# Course: CS 2300 (Databases)
# Semester: Fall 2023
# Languages: Python
# Database Engine: SQLite
# Team Members: Logan Markley, Abigail Krimmel, Madeline Harmon

import tkinter as tk
import random

CONST_WIDTH = 500
CONST_HEIGHT = 700
CONST_BGCOLOR = '#f5e5d3'

class LandingPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        titleLabel = tk.Label(self, text="Pathways", fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 40))
        subtitleLabel = tk.Label(self, text="The expresslane to finding your dream company!", fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 12))
        signInBtn = tk.Button(self, text="Sign In", fg='Black', command=lambda: controller.show_frame(SignInPage), font=('Tahoma', 16))
        createAccBtn = tk.Button(self, text="Create Account", fg='Black', command=lambda: controller.show_frame(CreateAccPage), font=('Tahoma', 16))
        
        titleLabel.place(x=230, y=70)
        subtitleLabel.place(x=170, y=180)
        signInBtn.place(x=200, y=270)
        createAccBtn.place(x=320, y=270)


class SignInPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        goHomeBtn = tk.Button(self, text="Go Back", command=lambda: controller.show_frame(LandingPage), fg='Black', font=('Tahoma', 12))
        
        goHomeBtn.grid(padx=10, pady=10)


class CreateAccPage(tk.Frame):
    # initializes all the widgets and places them in the frame
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        goHomeBtn = tk.Button(self, text="Go Back", command=lambda: controller.show_frame(LandingPage), fg='Black', font=('Tahoma', 12))
        goHomeBtn.grid(padx=10, pady=10)
        
        self.fname_var=tk.StringVar()
        self.lname_var=tk.StringVar()
        self.email_var=tk.StringVar()
        self.passw_var=tk.StringVar()
        self.repassw_var=tk.StringVar()
        
        fname_label = tk.Label(self, text = 'First Name:', font=('Tahoma',11, 'bold'))
        fname_entry = tk.Entry(self,textvariable = self.fname_var, font=('Tahoma',11,'normal'))
        lname_label = tk.Label(self, text = 'Last Name:', font=('Tahoma',11, 'bold'))
        lname_entry = tk.Entry(self,textvariable = self.lname_var, font=('Tahoma',11,'normal'))
        email_label = tk.Label(self, text = 'Email:*', font=('Tahoma',11, 'bold'))
        email_entry = tk.Entry(self,textvariable = self.email_var, font=('Tahoma',11,'normal'))
        passw_label = tk.Label(self, text = 'Password:*', font = ('Tahoma',11,'bold'))
        passw_entry = tk.Entry(self, textvariable = self.passw_var, font = ('Tahoma',11,'normal'), show = '*')
        repassw_label = tk.Label(self, text = 'Re-enter Password:*', font = ('Tahoma',11,'bold'))
        repassw_entry = tk.Entry(self, textvariable = self.repassw_var, font = ('Tahoma',11,'normal'), show = '*')
        submit_btn=tk.Button(self, text = 'Submit', command= self.submitEntries, font = ('Tahoma',14,'normal'))
        
        fname_label.place(x=218, y=90)
        fname_entry.place(x=320, y=90)
        lname_label.place(x=220, y=120)
        lname_entry.place(x=320, y=120)
        email_label.place(x=248, y=150)
        email_entry.place(x=320, y=150)
        passw_label.place(x=216, y=180)
        passw_entry.place(x=320, y=180)
        repassw_label.place(x=147, y=210)
        repassw_entry.place(x=320, y=210)
        submit_btn.place(x=300, y=290)

    def submitEntries(self) -> None:
        print(self.fname_var.get())
        print(self.lname_var.get())
        print(self.email_var.get())
        print(self.passw_var.get())
        print(self.repassw_var.get())
        return
    
    def verifyEntries(self) -> None:
        return
    
    def addAccToDatabase(self) -> None:
        return


class Pathways(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Pathways')
        self.geometry(f"{CONST_HEIGHT}x{CONST_WIDTH}+600+100")
        self.resizable(False,False)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (LandingPage, SignInPage, CreateAccPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(background=CONST_BGCOLOR)
        
        self.show_frame(LandingPage)

    def show_frame(self, cont) -> None:
        frame = self.frames[cont]
        frame.tkraise()
        return


if __name__ == "__main__":
    app = Pathways()
    app.mainloop()