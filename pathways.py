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

import sqlite3

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
        
        goHomeBtn = tk.Button(self, text="<- Back", command=lambda: self.controller.show_frame(LandingPage), fg='Black', font=('Tahoma', 12))
        goHomeBtn.grid(padx=10, pady=10)
        
        titleLabel = tk.Label(self, text="Sign In", fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 20, 'bold', 'underline'))
        titleLabel.place(x=280, y=50)
        
        self.email_var=tk.StringVar()
        self.passw_var=tk.StringVar()
        
        self.email_label = tk.Label(self, text = 'Email:', font=('Tahoma',11, 'bold'))
        self.email_entry = tk.Entry(self,textvariable = self.email_var, font=('Tahoma',11,'normal'))
        self.passw_label = tk.Label(self, text = 'Password:', font = ('Tahoma',11,'bold'))
        self.passw_entry = tk.Entry(self, textvariable = self.passw_var, font = ('Tahoma',11,'normal'), show = '*')
        self.signIn_btn=tk.Button(self, text = 'Sign in', command=lambda:self.signIntoAccount(), font = ('Tahoma',14,'normal'))
        
        self.email_label.place(x=250, y=190)
        self.email_entry.place(x=320, y=190)
        self.passw_label.place(x=218, y=220)
        self.passw_entry.place(x=320, y=220)
        self.signIn_btn.place(x=300, y=380)
    
    def signIntoAccount(self) -> None:
        message = tk.Label(self, text = '', font=('Tahoma',11, 'bold'), bg='firebrick2')
        
        if self.accountExistsInDatabase() and self.passwordIsCorrect():
            self.controller.cursor.execute('SELECT user_ID FROM User WHERE email=?;', (self.email_var.get(),))
            userIDfromDB = self.controller.cursor.fetchone()
            self.controller.currentUserId = userIDfromDB[0]
            message.config(text='Successfully signed in! Taking you to your profile page...', bg='green3')
            message.place(x=140, y=340)
            self.after(1500, lambda: message.place_forget())    # small delay to allow the message to be displayed for 1.5s
            self.after(1500, lambda: self.sendToProfilePage())
            self.after(1500, lambda: self.email_entry.delete(0,'end'))
            self.after(1500, lambda: self.passw_entry.delete(0,'end'))
        elif self.accountExistsInDatabase() is False:
            message.config(text='There is not an account associated with that email.')
            message.place(x=140, y=340)
            self.email_entry.delete(0,'end')
            self.passw_entry.delete(0,'end')
            self.after(1500, lambda: message.place_forget())    # small delay to allow the message to be displayed for 1.5s
        else:
            message.config(text='That password was not correct, please try again.')
            message.place(x=150, y=340)
            self.passw_entry.delete(0,'end')
            self.after(1500, lambda: message.place_forget())    # small delay to allow the message to be displayed for 1.5s
        
        return
    
    def accountExistsInDatabase(self) -> bool:
        self.controller.cursor.execute('SELECT user_ID FROM User WHERE email=?;', (self.email_var.get(),))
        if self.controller.cursor.fetchone() is not None:
            return True
        else:
            return False
    
    def passwordIsCorrect(self) -> bool:
        self.controller.cursor.execute('SELECT user_ID FROM User WHERE email=? AND password=?;', (self.email_var.get(), self.passw_var.get()))
        if self.controller.cursor.fetchone() is not None:
            return True
        else:
            return False
        return True
    
    def sendToProfilePage(self) -> None:
        self.controller.frames[ProfilePage].showNameText()
        
        self.controller.cursor.execute('''SELECT user_ID
                                        FROM Recommendation
                                        WHERE user_ID = ?;''', (self.controller.currentUserId,))
        userID = self.controller.cursor.fetchone()
        if userID is not None:
            self.controller.frames[ProfilePage].showResultsBtn()
        self.controller.show_frame(ProfilePage)
        return


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
            self.addAccToDatabase(fname, lname, email, passw)
        
        return
    
    def verifyEntries(self, email, passw, repassw) -> bool:
        message = tk.Label(self, text = '', font=('Tahoma',11, 'bold'), bg='firebrick2')
        
        if self.emailInUse(email):
            message.config(text = "Email address already in use!")
            self.emptyEntries(False,True, True, True)
        elif '@' not in email:
            message.config(text = "Not a valid email address!")
            self.emptyEntries(False,True, True, True)
        elif passw != repassw:
            message.config(text = "Passwords do not match!")
            self.emptyEntries(False, False, True, True)
        elif len(passw) < 8:
            message.config(text = "Passwords not long enough!")
            self.emptyEntries(False, False, True, True)
        else:
            message.config(text = "Account creation successful! Sending you to sign in...", bg='green3')
            self.after(2500, lambda: self.emptyEntries(True, False, False, False))
        
        if message['bg'] == 'green3':
            message.place(x=140, y=340)
        else:
            message.place(x=240, y=340)
            
        self.after(2500, lambda: message.place_forget())    # small delay to allow the message to be displayed for 2.5s
        if message['bg'] == 'green3':    # if everything is verified, return True
            self.after(2500, lambda: self.controller.show_frame(SignInPage))
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
    
    def emailInUse(self, email) -> bool:
        self.controller.cursor.execute('''SELECT email
                                        FROM User AS U
                                        WHERE U.email = ?;
                                        ''', (email,))
        matchingEmail = self.controller.cursor.fetchone()
        return matchingEmail is not None
    
    def addAccToDatabase(self, first, last, emai, pas) -> None:
        self.controller.cursor.execute('SELECT COUNT(user_ID) FROM User;')
        newAccountID = self.controller.cursor.fetchone()
        self.controller.cursor.execute('INSERT INTO User (user_ID, password, email, first_name, last_name) VALUES (?, ?, ?, ?, ?);', (newAccountID[0], pas, emai, first, last))
        self.controller.conn.commit()
        
        return


class ProfilePage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        #NEED TO ADD LOG OUT FUNCTIONALITY!!
        logOutBtn = tk.Button(self, text="<- Log Out", command=lambda: self.signOut(), fg='Black', font=('Tahoma', 12))
        logOutBtn.grid(padx=10, pady=10)
        
        titleLabel = tk.Label(self, text="Profile Page", fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 20, 'bold', 'underline'))
        titleLabel.place(x=250, y=50)
        
        takeQuizBtn = tk.Button(self, text="Take A Preferences Quiz!", command=lambda: self.sendToQuiz(), fg='Black', font=('Tahoma', 12))
        takeQuizBtn.place(x=238, y=120)
        
        self.nameLabel = tk.Label(self, text='', fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 13, 'italic'))
        self.nameLabel.place(x=510, y=10)
    
    def signOut(self) -> None:
        self.controller.currentUserId = -1
        self.controller.show_frame(LandingPage)
        return
    
    def sendToQuiz(self) -> None:
        self.controller.cursor.execute('''SELECT user_ID
                                        FROM Salary_Question AS S
                                        WHERE S.user_ID = ?;
                                        ''', (self.controller.currentUserId,))
        userID = self.controller.cursor.fetchone()   # returns the user's ID if they have quiz responses currently stored in the database.
        if userID is not None:  # if they have taken a quiz already...
            self.controller.cursor.execute('''DELETE
                                        FROM Salary_Question
                                        WHERE user_ID = ?;
                                        ''', (self.controller.currentUserId,))
            self.controller.cursor.execute('''DELETE
                                        FROM Benefit_Question
                                        WHERE user_ID = ?;
                                        ''', (self.controller.currentUserId,))
            self.controller.cursor.execute('''DELETE
                                        FROM Time_Question
                                        WHERE user_ID = ?;
                                        ''', (self.controller.currentUserId,))
            self.controller.cursor.execute('''DELETE
                                        FROM Industry_Question
                                        WHERE user_ID = ?;
                                        ''', (self.controller.currentUserId,))
            self.controller.cursor.execute('''DELETE
                                        FROM Value_Question
                                        WHERE user_ID = ?;
                                        ''', (self.controller.currentUserId,))
            self.controller.cursor.execute('''DELETE
                                        FROM Location_Question
                                        WHERE user_ID = ?;
                                        ''', (self.controller.currentUserId,))
            self.controller.cursor.execute('''DELETE
                                        FROM Recommendation
                                        WHERE user_ID = ?;
                                        ''', (self.controller.currentUserId,))
            self.controller.conn.commit()
        self.controller.show_frame(QuizPage)
    
    def showNameText(self) -> None:
        self.controller.cursor.execute('SELECT first_name, last_name FROM User WHERE user_ID=?;', (self.controller.currentUserId,))
        names = self.controller.cursor.fetchone()
        fname = names[0]
        lname = names[1]
        if fname is not None and lname is not None:
            nameText = f'Hello {fname} {lname}!'
            self.nameLabel.configure(text=nameText)
        elif fname is not None and lname is None:
            nameText = f'Hello {fname}!'
            self.nameLabel.configure(text=nameText)
        return
    
    def showResultsBtn(self) -> None:
        goToResultsBtn = tk.Button(self, text="See your last quiz results!", command=lambda: self.sendToResults(), fg='Black', font=('Tahoma', 12))
        goToResultsBtn.place(x=238, y=200)
        return
    
    def sendToResults(self) -> None:
        self.controller.show_frame(QuizResultsPage)
        self.controller.frames[QuizResultsPage].pullOldRecommendation()
        self.controller.frames[QuizResultsPage].displayCompanyJobs()
        return

class QuizPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        backBtn = tk.Button(self, text="<- Back", command=lambda: controller.show_frame(LandingPage), fg='Black', font=('Tahoma', 12))
        backBtn.grid(padx=10, pady=10)
        
        titleLabel = tk.Label(self, text="Preferences Quiz!", fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 20, 'bold', 'underline'))
        titleLabel.place(x=240, y=5)
        
        statesArr = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 
                    'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 
                    'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 
                    'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 
                    'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
                    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
                    ]
        
        benefitsArr = ['Birthday And Holiday Gifts', 'Education', 'Employee Assistance Programs', 'Employee Discount',
                        'Flexible Work Hours', 'Free Snacks And Drinks', 'Gym On Site', 'Health Insurance', 'Home and Auto',
                        'No Dress Code', 'Parental Leave', 'Paid Time Off', 'Professional Development',
                        'Retirement Plans', 'Stock Options', 'Wellness Programs'
                        ]
        
        valuesArr = ['Commitment To Excellence', 'Creativity', 'Customer Focus', 'Customer Obsession',
                        'Customer Satisfaction', 'Design', 'Economic Stability', 'Entertainment', 'Everyday Low Prices',
                        'Excellence', 'Health', 'Inclusion', 'Innovation', 'Inspiration', 'Integrity', 'Ownership',
                        'Public Service', 'Safety', 'Sustainability', 'Teamwork', 'Trust', 'User Experience', 'User Focus'
                        ]
        
        industryArr = ['Defense', 'E-Commerce', 'Electronics', 'Entertainment', 'Finance', 'Life Sciences', 'Retail',
                        'Social Media', 'Software Technology', 'Technology Services', 'Telecommunications'
                        ]
        
        
        fullPartTmpArr = ['Full', 'Part']
        
        # initialize the variables that hold the values from the questions here
        self.fullPartOrTmp_var = tk.StringVar()
        self.industry_var = tk.StringVar()
        self.values_var = tk.StringVar()
        self.benefits_var = tk.StringVar()
        self.location1_var = tk.StringVar()
        self.location1_var.set('*Location 1')
        self.location2_var = tk.StringVar()
        self.location3_var = tk.StringVar()
        self.salary_var = tk.IntVar()
        
        # create each of the widgets to be displayed here
        self.fullPartOrTmp_label = tk.Label(self, text='Full-time or Part-time?', font=('Tahoma',11, 'bold'))
        self.fullPartOrTmp_dropdown = tk.OptionMenu(self, self.fullPartOrTmp_var, *fullPartTmpArr)
        
        self.industry_label = tk.Label(self, text='Favorite industry?', font=('Tahoma',11, 'bold'))
        self.industry_dropdown = tk.OptionMenu(self, self.industry_var, *industryArr)
        
        self.values_label = tk.Label(self, text='The value that you align the most with?', font=('Tahoma',11, 'bold'))
        self.values_dropdown = tk.OptionMenu(self, self.values_var, *valuesArr)
        
        self.benefits_label = tk.Label(self, text='Which benefit do you value the most?', font=('Tahoma',11, 'bold'))
        self.benefits_dropdown = tk.OptionMenu(self, self.benefits_var, *benefitsArr)
        
        self.location_label = tk.Label(self, text = 'Choose up to 3 of your desired states to work in:', font=('Tahoma',11, 'bold'))
        self.location_subtitle_label = tk.Label(self, text = '*only 1 state selection is required*', font = ('Calibri',9,'italic'), bg=CONST_BGCOLOR)
        self.location1_dropdown = tk.OptionMenu(self, self.location1_var, *statesArr)
        self.location2_dropdown = tk.OptionMenu(self, self.location2_var, *statesArr)
        self.location3_dropdown = tk.OptionMenu(self, self.location3_var, *statesArr)
        
        self.salary_label = tk.Label(self, text='What is your desired starting salary?', font=('Tahoma',11, 'bold'))
        self.salary_scale = tk.Scale(
            self,
            variable=self.salary_var,
            from_=25000,
            to=125000,
            orient=tk.HORIZONTAL,
            length=650,
            tickinterval=10000,
            resolution=2500,
        )
        
        # inititally place all of the widgets here
        self.fullPartOrTmp_label.place(x=140, y=55)
        self.fullPartOrTmp_dropdown.place(x=470, y=55-2)
        self.industry_label.place(x=140, y=90)
        self.industry_dropdown.place(x=470, y=90-2)
        self.values_label.place(x=140, y=125)
        self.values_dropdown.place(x=470, y=125-2)
        self.benefits_label.place(x=140, y=160)
        self.benefits_dropdown.place(x=470, y=160-2)
        self.location_label.place(x=90, y=210)
        self.location_subtitle_label.place(x=180, y=240)
        self.location1_dropdown.place(x=470, y=210-2)
        self.location2_dropdown.place(x=470, y=240-2)
        self.location3_dropdown.place(x=470, y=270-2)
        self.salary_label.place(x=220, y=320)
        self.salary_scale.place(x=20, y=350)
        
        # initially create and place the clear quiz and submit quiz buttons
        self.clear_btn=tk.Button(self, text = 'Clear Responses', command=lambda: self.clearAllResponses(), font = ('Tahoma',14,'normal'), bg='firebrick2')
        self.clear_btn.place(x=170, y=435)
        self.submit_btn=tk.Button(self, text = 'Submit Quiz', command=lambda: self.uploadQuizResponses(), font = ('Tahoma',14,'normal'), bg='green3')
        self.submit_btn.place(x=400, y=435)
    
    def clearAllResponses(self) -> None:
        self.fullPartOrTmp_var.set('')
        self.industry_var.set('')
        self.values_var.set('')
        self.benefits_var.set('')
        self.location1_var.set('*Location 1')
        self.location2_var.set('')
        self.location3_var.set('')
        self.salary_var.set(25000)
        return
    
    def uploadQuizResponses(self) -> None:
        verified = self.verifyEntries()
        if verified:
            self.controller.cursor.execute('INSERT INTO Time_Question (user_ID, time_answer) VALUES (?, ?);', (self.controller.currentUserId, self.fullPartOrTmp_var.get()))
            self.controller.cursor.execute('INSERT INTO Industry_Question (user_ID, industry_answer) VALUES (?, ?);', (self.controller.currentUserId, self.industry_var.get()))
            self.controller.cursor.execute('INSERT INTO Value_Question (user_ID, value_answer) VALUES (?, ?);', (self.controller.currentUserId, self.values_var.get()))
            self.controller.cursor.execute('INSERT INTO Benefit_Question (user_ID, benefit_answer) VALUES (?, ?);', (self.controller.currentUserId, self.benefits_var.get()))
            self.controller.cursor.execute('INSERT INTO Location_Question (user_ID, location1, location2, location3) VALUES (?, ?, ?, ?);', (self.controller.currentUserId, self.location1_var.get(), self.location2_var.get(), self.location3_var.get()))
            self.controller.cursor.execute('INSERT INTO Salary_Question (user_ID, expected_salary) VALUES (?, ?);', (self.controller.currentUserId, self.salary_var.get()))
            self.controller.conn.commit()
            
            message = tk.Label(self, text = 'Uploading quiz results ...', font=('Tahoma',11, 'bold'), bg='green3')
            message.place(x=250, y=340)
            self.after(1500, lambda: message.place_forget())    # small delay to allow the message to be displayed for 1.5s
            self.after(1500, lambda: self.controller.show_frame(QuizResultsPage))
            self.after(1500, lambda: self.controller.frames[QuizResultsPage].updateQuizResultsPage())   # this updates the quiz results page through the controller to display the users quiz results.)
            self.after(1500, lambda: self.clearAllResponses())
        return
    
    def verifyEntries(self) -> bool:
        message = tk.Label(self, text = 'Uploading quiz results ...', font=('Tahoma',11, 'bold'), bg='firebrick2')
        if self.fullPartOrTmp_var.get() == '' or self.industry_var.get() == '' or self.values_var.get() == '' or self.benefits_var.get() == '' or self.location1_var.get() == '': 
            message.config(text='One or more required entries were not answered. Failed to upload.')
            message.place(x=120, y=340)
            self.after(1500, lambda: message.place_forget())
            return False
        elif self.location1_var.get() == self.location2_var.get() or self.location1_var.get() == self.location3_var.get() or (self.location2_var.get() != '' and self.location3_var.get() != '' and self.location2_var.get() == self.location3_var.get()):
            message.config(text='You selected locations that are duplicates, please choose different locations.')
            message.place(x=140, y=340)
            self.after(1500, lambda: message.place_forget())
            return False
        else:
            return True


class QuizResultsPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        backBtn = tk.Button(self, text="<- Back to Profile", command=lambda: self.goToProfilePage(), fg='Black', font=('Tahoma', 12))
        backBtn.grid(padx=10, pady=10)
        
        titleLabel = tk.Label(self, text="Your highest matched company is...", fg='Black', bg=CONST_BGCOLOR, font=('Tahoma', 20, 'bold', 'underline'))
        titleLabel.place(x=100, y=50)
        
        self.companyLabel = tk.Label(self, text="", fg='Black', bg=CONST_BGCOLOR, font=('Calibri', 30, 'bold'))
        self.companyLabel.place(x=70, y=200)
        
        self.jobsLabel = tk.Label(self, text="", fg='Black', bg=CONST_BGCOLOR, font=('Calibri', 14, 'italic'))
        self.jobsLabel.place(x=240, y=340)
    
    def goToProfilePage(self) -> None:
        self.controller.frames[ProfilePage].showResultsBtn()
        self.controller.show_frame(ProfilePage)
        return
    
    def displayCompanyJobs(self) -> None:
        self.controller.cursor.execute('''SELECT cname
                                        FROM Recommendation
                                        WHERE user_ID = ?;''', (self.controller.currentUserId,))
        matchedCompany = self.controller.cursor.fetchone()
        
        self.controller.cursor.execute('''SELECT job_title
                                        FROM Job_Listing
                                        WHERE cname = ?;''', (matchedCompany[0],))
        jobs = self.controller.cursor.fetchall()
        self.jobsLabel.configure(text=f"Potential Jobs:\n{jobs[0][0]}\n{jobs[1][0]}")
        return
    
    def pullOldRecommendation(self) -> None:
        self.controller.cursor.execute('''SELECT match_strength, cname
                                        FROM Recommendation
                                        WHERE user_ID = ?;''', (self.controller.currentUserId,))
        strengthAndCompany = self.controller.cursor.fetchone()
        self.companyLabel.configure(text=f"{strengthAndCompany[1]}\n with a match score of {strengthAndCompany[0]:.2f}%!")
        return
    
    def updateQuizResultsPage(self) -> None:
        self.companyLabel.configure(text="")
        self.jobsLabel.configure(text="")
        topCompany = self.createCompanyRecommendation()
        self.after(1500, lambda: self.companyLabel.configure(text=f"{topCompany[0]}\n with a match score of {topCompany[1]:.2f}%!"))
        self.after(1500, lambda: self.displayCompanyJobs())
        
        return
    
    def createCompanyRecommendation(self):
        self.controller.cursor.execute('''SELECT cname
                                        FROM Company;''')
        companies = self.controller.cursor.fetchall()
        company_scores = []
        
        self.controller.cursor.execute("""SELECT I.industry_answer
                                        FROM Industry_Question AS I
                                        WHERE I.user_ID = ?;""", (self.controller.currentUserId,))
        industry_answer = self.controller.cursor.fetchone()
        self.controller.cursor.execute("""
            SELECT C.cname
            FROM Company AS C
            WHERE C.industry = ?;""", (industry_answer[0],))
        industry_companies = self.controller.cursor.fetchall()
        
        
        self.controller.cursor.execute('''SELECT S.expected_salary
                                        FROM Salary_Question AS S
                                        WHERE S.user_ID = ?;''', (self.controller.currentUserId,))
        expected_salary = self.controller.cursor.fetchone()
        self.controller.cursor.execute("""
            SELECT C.cname
            FROM Company AS C 
            WHERE C.avg_starting_salary + 10000 > ? AND C.avg_starting_salary - 10000 < ?;
            """, (expected_salary[0], expected_salary[0],))
        salary_companies = self.controller.cursor.fetchall()
        
        
        self.controller.cursor.execute('''SELECT value_answer
                                        FROM Value_Question
                                        WHERE user_ID = ?;''', (self.controller.currentUserId,))
        value_answer = self.controller.cursor.fetchone()
        self.controller.cursor.execute("""
            SELECT Company.cname
            FROM Company
            LEFT JOIN Company_Value ON Company.cname = Company_Value.cname 
            WHERE Company_Value.value = ?;
            """, (value_answer[0],))
        value_companies = self.controller.cursor.fetchall()
        
        
        self.controller.cursor.execute('''SELECT location1, location2, location3
                                        FROM Location_Question
                                        WHERE user_ID = ?;''', (self.controller.currentUserId,))
        locations = self.controller.cursor.fetchone()
        self.controller.cursor.execute("""
            SELECT Company.cname
            FROM Company 
            LEFT JOIN Company_Location ON Company.cname = Company_Location.cname
            WHERE Company_Location.location IN (?, ?, ?);
            """, (locations[0], locations[1], locations[2]))
        location_companies = self.controller.cursor.fetchall()
        
        
        self.controller.cursor.execute('''SELECT benefit_answer
                                        FROM Benefit_Question
                                        WHERE user_ID = ?;''', (self.controller.currentUserId,))
        benefit_answer = self.controller.cursor.fetchone()
        self.controller.cursor.execute("""
            SELECT Company.cname
            FROM Company 
            LEFT JOIN Company_Benefit ON Company.cname = Company_Benefit.cname 
            WHERE Company_Benefit.benefit = ?;
            """, (benefit_answer[0],))
        benefit_companies = self.controller.cursor.fetchall()
        
        
        self.controller.cursor.execute('''SELECT time_answer
                                        FROM Time_Question
                                        WHERE user_ID = ?;''', (self.controller.currentUserId,))
        time_answer = self.controller.cursor.fetchone()
        self.controller.cursor.execute("""
            SELECT Company.cname
            FROM Company 
            LEFT JOIN Job_Listing ON Company.cname = Job_Listing.cname 
            WHERE Job_Listing.full_part_temp = ?;
            """, (time_answer[0],))
        time_companies = self.controller.cursor.fetchall()
        
        
        newIndustryCompanies = []
        for company in industry_companies:
            newIndustryCompanies.append(company[0])
        
        newSalaryCompanies = []
        for company in salary_companies:
            newSalaryCompanies.append(company[0])
        
        newValueCompanies = []
        for company in value_companies:
            newValueCompanies.append(company[0])
        
        newLocationCompanies = []
        for company in location_companies:
            newLocationCompanies.append(company[0])
        
        newBenefitCompanies = []
        for company in benefit_companies:
            newBenefitCompanies.append(company[0])
        
        newTimeCompanies = []
        for company in time_companies:
            newTimeCompanies.append(company[0])
        
        for company in companies:
            score = 0
            
            if company[0] in newIndustryCompanies:
                score += 10
            if company[0] in newSalaryCompanies:
                score += 10
            if company[0] in newValueCompanies:
                score += 10
            if company[0] in newLocationCompanies:
                score += 10
            if company[0] in newBenefitCompanies:
                score += 10
            if company[0] in newTimeCompanies:
                score += 10
            
            score_percentage = (score / 60) * 100
            company_scores.append((company[0], score_percentage))
        
        sorted_companies = sorted(company_scores, key=lambda x: x[1], reverse=True)
        
        top_company = sorted_companies[0]
        match_strength = top_company[1] / 100
        self.controller.cursor.execute("""
            INSERT INTO Recommendation (user_ID, match_strength, cname)
            VALUES (?, ?, ?);
            """, (self.controller.currentUserId, top_company[1], top_company[0],))
        self.controller.conn.commit()
        
        return top_company


class Pathways(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Pathways')
        self.geometry(f"{CONST_HEIGHT}x{CONST_WIDTH}+600+100")
        self.resizable(False,False)
        
        self.conn = sqlite3.connect('pathways.sql') 
        self.cursor = self.conn.cursor()
        
        self.currentUserId = -1
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (LandingPage, SignInPage, CreateAccPage, ProfilePage, QuizPage, QuizResultsPage):
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
    app.cursor.close()
    app.conn.close()
