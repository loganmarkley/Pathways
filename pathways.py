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
        
        titleLabel = tk.Label(self, text="Pathways", fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 40, 'bold', 'underline'))
        subtitleLabel = tk.Label(self, text="The expresslane to finding your dream company!", fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 12))
        signInBtn = tk.Button(self, text="Sign In", fg='Black', command=lambda: controller.show_frame(SignInPage), font=('Tahoma', 16))
        createAccBtn = tk.Button(self, text="Create Account", fg='Black', command=lambda: controller.show_frame(CreateAccPage), font=('Tahoma', 16))
        
        titleLabel.place(x=210, y=60)
        subtitleLabel.place(x=170, y=180)
        signInBtn.place(x=200, y=270)
        createAccBtn.place(x=320, y=270)


class SignInPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        goHomeBtn = tk.Button(self, text="<- Back", command=lambda: controller.show_frame(LandingPage), fg='Black', font=('Tahoma', 12))
        goHomeBtn.grid(padx=10, pady=10)
        
        titleLabel = tk.Label(self, text="Sign In", fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 20, 'bold', 'underline'))
        titleLabel.place(x=280, y=50)
        
        self.email_var=tk.StringVar()
        self.passw_var=tk.StringVar()
        
        self.email_label = tk.Label(self, text = 'Email:', font=('Tahoma',11, 'bold'))
        self.email_entry = tk.Entry(self,textvariable = self.email_var, font=('Tahoma',11,'normal'))
        self.passw_label = tk.Label(self, text = 'Password:', font = ('Tahoma',11,'bold'))
        self.passw_entry = tk.Entry(self, textvariable = self.passw_var, font = ('Tahoma',11,'normal'), show = '*')
        self.signIn_btn=tk.Button(self, text = 'Sign in', font = ('Tahoma',14,'normal'))
        
        self.email_label.place(x=250, y=190)
        self.email_entry.place(x=320, y=190)
        self.passw_label.place(x=218, y=220)
        self.passw_entry.place(x=320, y=220)
        self.signIn_btn.place(x=300, y=380)
        


class CreateAccPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        goHomeBtn = tk.Button(self, text="<- Back", command=lambda: controller.show_frame(LandingPage), fg='Black', font=('Tahoma', 12))
        goHomeBtn.grid(padx=10, pady=10)
        
        titleLabel = tk.Label(self, text="Create Account", fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 20, 'bold', 'underline'))
        titleLabel.place(x=240, y=50)
        
        self.fname_var=tk.StringVar()
        self.lname_var=tk.StringVar()
        self.email_var=tk.StringVar()
        self.passw_var=tk.StringVar()
        self.repassw_var=tk.StringVar()
        
        self.fname_label = tk.Label(self, text = 'First Name:', font=('Tahoma',11, 'bold'))
        self.fname_entry = tk.Entry(self,textvariable = self.fname_var, font=('Tahoma',11,'normal'))
        self.lname_label = tk.Label(self, text = 'Last Name:', font=('Tahoma',11, 'bold'))
        self.lname_entry = tk.Entry(self,textvariable = self.lname_var, font=('Tahoma',11,'normal'))
        self.email_label = tk.Label(self, text = 'Email:*', font=('Tahoma',11, 'bold'))
        self.email_entry = tk.Entry(self,textvariable = self.email_var, font=('Tahoma',11,'normal'))
        self.passw_label = tk.Label(self, text = 'Password:*', font = ('Tahoma',11,'bold'))
        self.passw_entry = tk.Entry(self, textvariable = self.passw_var, font = ('Tahoma',11,'normal'), show = '*')
        self.repassw_label = tk.Label(self, text = 'Re-enter Password:*', font = ('Tahoma',11,'bold'))
        self.repassw_entry = tk.Entry(self, textvariable = self.repassw_var, font = ('Tahoma',11,'normal'), show = '*')
        self.subtitle_label = tk.Label(self, text = 'fields with an asterik(*) are required', font = ('Calibri',9,'italic'), bg=CONST_BGCOLOR)
        self.submit_btn=tk.Button(self, text = 'Submit', command= self.submitEntries, font = ('Tahoma',14,'normal'))
        
        self.fname_label.place(x=218, y=150)
        self.fname_entry.place(x=320, y=150)
        self.lname_label.place(x=220, y=180)
        self.lname_entry.place(x=320, y=180)
        self.email_label.place(x=248, y=210)
        self.email_entry.place(x=320, y=210)
        self.passw_label.place(x=216, y=240)
        self.passw_entry.place(x=320, y=240)
        self.repassw_label.place(x=147, y=270)
        self.repassw_entry.place(x=320, y=270)
        self.subtitle_label.place(x=300, y=300)
        self.submit_btn.place(x=300, y=380)
    
    def submitEntries(self) -> None:
        fname = self.fname_var.get()
        lname = self.lname_var.get()
        email = self.email_var.get()
        passw = self.passw_var.get()
        repassw = self.repassw_var.get()
        
        entriesVerified = self.verifyEntries(email, passw, repassw)
        if entriesVerified:
            addAccToDatabase(fname, lname, email, passw)
        
        self.emptyEntries()
        return
    
    def verifyEntries(self, email, passw, repassw) -> bool:
        message = tk.Label(self, text = '', font=('Tahoma',11, 'bold'), bg='red')
        
        # WIP: MUST CHECK TO SEE IF THE EMAIL EXISTS ALREADY IN THE DATABASE bc emails are unique
        if '@' not in email:
            message.config(text = "Not a valid email address!")
        elif passw != repassw:
            message.config(text = "Passwords do not match!")
        elif len(passw) < 8:
            message.config(text = "Passwords not long enough!")
        else:
            message.config(text = "Account creation successful! Sending you to sign in...", bg='lawn green')
        
        if message['bg'] == 'lawn green':
            message.place(x=140, y=340)
        else:
            message.place(x=240, y=340)
            
        self.after(2000, lambda: message.place_forget())    # small delay to allow the message to be displayed for 3s
        if message['bg'] == 'lawn green':    # if everything is verified, return True
            self.after(2000, lambda: self.controller.show_frame(LandingPage))
            return True
        else:
            return False
    
    def emptyEntries(self) -> None:
        self.fname_entry.delete(0, 'end')
        self.lname_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.passw_entry.delete(0, 'end')
        self.repassw_entry.delete(0, 'end')
        return
    
    def addAccToDatabase(first, last, emai, pas) -> None:   # WIP
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