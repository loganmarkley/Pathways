# File: Pathways.py
# Desc: This program contains the GUI and database implementation for our
#       company matchmaking application, Pathways.
# Course: CS 2300 (Databases)
# Semester: Fall 2023
# Languages: Python
# Database Engine: SQLite
# Team Members: Logan Markley, Abigail Krimmel, Madeline Harmon

import tkinter as tk
from tkinter import ttk
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
        
        return
    
    def verifyEntries(self, email, passw, repassw) -> bool:
        message = tk.Label(self, text = '', font=('Tahoma',11, 'bold'), bg='red')
        
        # WIP: MUST CHECK TO SEE IF THE EMAIL EXISTS ALREADY IN THE DATABASE bc emails are unique
        if '@' not in email:
            message.config(text = "Not a valid email address!")
            self.emptyEntries(False,True, True, True)
        elif passw != repassw:
            message.config(text = "Passwords do not match!")
            self.emptyEntries(False, False, True, True)
        elif len(passw) < 8:
            message.config(text = "Passwords not long enough!")
            self.emptyEntries(False, False, True, True)
        else:
            message.config(text = "Account creation successful! Sending you to sign in...", bg='lawn green')
            self.emptyEntries(True, False, False, False)
        
        if message['bg'] == 'lawn green':
            message.place(x=140, y=340)
        else:
            message.place(x=240, y=340)
            
        self.after(2000, lambda: message.place_forget())    # small delay to allow the message to be displayed for 3s
        if message['bg'] == 'lawn green':    # if everything is verified, return True
            self.after(2000, lambda: self.controller.show_frame(SignInPage))
            return True
        else:
            return False
    
    def emptyEntries(self, allE: bool, email: bool, passw: bool, repassw: bool) -> None:    # if True, empty that entry
        if email:
            self.email_entry.delete(0, 'end')
        if passw:
            self.passw_entry.delete(0, 'end')
        if repassw: 
            self.repassw_entry.delete(0, 'end')
        if allE:
            self.fname_entry.delete(0, 'end')
            self.lname_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.passw_entry.delete(0, 'end')
            self.repassw_entry.delete(0, 'end')
        return
    
    def addAccToDatabase(first, last, emai, pas) -> None:   # WIP
        return


class ProfilePage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        #NEED TO ADD LOG OUT FUNCTIONALITY!!
        logOutBtn = tk.Button(self, text="<- Log Out", command=lambda: controller.show_frame(LandingPage), fg='Black', font=('Tahoma', 12))
        logOutBtn.grid(padx=10, pady=10)
        
        titleLabel = tk.Label(self, text="Profile Page", fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 20, 'bold', 'underline'))
        titleLabel.place(x=250, y=50)
        
        takeQuizBtn = tk.Button(self, text="Take A Preferences Quiz!", command=lambda: controller.show_frame(QuizPage), fg='Black', font=('Tahoma', 12))
        takeQuizBtn.place(x=238, y=120)


class QuizPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        backBtn = tk.Button(self, text="<- Log Out", command=lambda: controller.show_frame(LandingPage), fg='Black', font=('Tahoma', 12))
        backBtn.grid(padx=10, pady=10)
        
        statesArr = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 
                    'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 
                    'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 
                    'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 
                    'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
                    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
                    ]
        
        benefitsArr = ['Health Insurance', 'Employee Discount', 'Parental Leave', 'Home and Auto', 'Wellness Programs', 'Education',
                    'Free Snacks And Drinks', 'Gym On Site', 'Stock Options', 'Professional Development', 'Flexible Work Hours',
                    'Part Time Off', 'No Dress Code', 'Birthday And Holiday Gifts', 'Retirement Plans', 'Wellness Program',
                    'Stock Options', 'Flexible Work Hours', 'Professional Development', 'Gym On Site', 'Employee Assistance Programs'
                    ]
        
        valuesArr = [ 'Customer Obsession', 'Ownership', 'Innovation', 'Integrity', 'Inclusion', 'Collaboration', 'Customer Focus',
                    'Commitment To Excellence', 'Teamwork', 'Sustainability', 'Health', 'Customer Satisfaction', 'Inclusion',
                    'User Focus', 'Design', 'User Experience', 'Customer Focus', 'Everyday Low Prices',
                    'Sustainability', 'Creativity', 'Inspiration', 'Trust', 'Entertainment', 'Safety', 'Excellence',
                    'Public Service', 'Economic Stability'
                    ]
        
        industryArr = ['E-Commerce', 'Telecommunications', 'Social Media', 'Defense', 'Finance', 'Technology Services',
                        'Retail', 'Life Sciences', 'Entertainment', 'Software Technology', 'Electronics']
        
        fullPartTmpArr = ['Full-time', 'Part-time']
        
        self.fullPartOrTmp_var = tk.StringVar()
        self.industry_var = tk.StringVar()
        self.values_var = tk.StringVar()
        
        
        self.fullPartOrTmp_label = tk.Label(self, text='Full-time or Part-time?', font=('Tahoma',11, 'bold'))
        self.fullPartOrTmp_dropdown = tk.OptionMenu(self, self.fullPartOrTmp_var, *fullPartTmpArr)
        
        self.industry_label = tk.Label(self, text='Favorite industry?', font=('Tahoma',11, 'bold'))
        self.industry_dropdown = tk.OptionMenu(self, self.industry_var, *industryArr)
        
        self.values_label = tk.Label(self, text='The value that you align the most with?', font=('Tahoma',11, 'bold'))
        self.values_dropdown = tk.OptionMenu(self, self.values_var, *valuesArr)
        # self.location_label = tk.Label(self, text = 'Email:*', font=('Tahoma',11, 'bold'))
        # self.location_dropdown = tk.Entry(self,textvariable = self.email_var, font=('Tahoma',11,'normal'))
        # self.values_label
        # self.values_dropdown
        # self.benefits_label
        # self.benefits_dropdown
        # self.salary_label
        # self.salary_slider
        
        self.fullPartOrTmp_label.place(x=180, y=50)
        self.fullPartOrTmp_dropdown.place(x=400, y=50)
        self.industry_label.place(x=180, y=80)
        self.industry_dropdown.place(x=400, y=80)
        self.values_label.place(x=180, y=110)
        self.values_dropdown.place(x=400, y=110)


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
        for F in (LandingPage, SignInPage, CreateAccPage, ProfilePage, QuizPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(background=CONST_BGCOLOR)
        
        self.show_frame(ProfilePage)
    
    def show_frame(self, cont) -> None:
        frame = self.frames[cont]
        frame.tkraise()
        return



if __name__ == "__main__":
    app = Pathways()
    app.mainloop()