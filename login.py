import customtkinter
import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage

app = customtkinter.CTk()
app.title('login')
app.geometry('450x360')
app.config(bg = '#2fa2c4')

font1 = ('Helvetica', 25, 'bold')
font2 = ('Arial', 17, 'bold')
font3 = ('Arial', 13, 'bold')
font4 = ('Arial', 13, 'bold','underline')

conn = sqlite3.connect('login.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL,
        password TEXT NOT NULL)''')

def signup():
    username = username_entry.get()
    password = password_entry.get()
    if username != '' and password != '':
        cursor.execute('SELECT username FROM users WHERE username=?',[username])
        if cursor.fetchone() is not None:
            messagebox.showerror('Error', 'Username already exists.')
        else: 
            encoded_password = password.encode('utf-8')
            hash_password = bcrypt.hashpw(encoded_password,bcrypt.gensalt())
            #print(hash_password)
            cursor.execute('INSERT INTO users VALUES (?, ?)', [username, hash_password])
            conn.commit()
            messagebox.showinfo('Success', 'Account has been created.')
    else:
        messagebox.showerror('Error', 'Enter all data.')

def login_account():
    username = username_entry2.get()
    password = password_entry2.get()
    if username != '' and password != '':
        cursor.execute('SELECT password FROM users WHERE username=?',[username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                messagebox.showinfo('Success', 'Logged in successfully.')
            else:
                messagebox.showerror('Error', 'Invalid password.')
        else:
            messagebox.showerror('Error','Invalid username.')
    else: 
        messagebox.showerror('Error', 'Enter all data.')


def login():
    frame1.destroy()
    frame2 = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=470, height=360)
    frame2.place(x=0, y=0)
    
    #image1 = PhotoImage(file="1.png")
    #image1_label = Label(frame2,image=image1,bg='#001220')
    #image1_label.place(x=0,y=0)
    #frame2.image1 = image1
    
    login_label2 = customtkinter.CTkLabel(frame2,font=font1,text='Log in',text_color='#fff',bg_color='#001220')
    login_label2.place(x=280,y=20)
    
    global username_entry2
    global password_entry2 
    
    username_entry2 = customtkinter.CTkEntry(frame2,font=font2, text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Username',placeholder_text_color='#a3a3a3',width=200,height=50)
    username_entry2.place(x=230,y=150)
    
    password_entry2 = customtkinter.CTkEntry(frame2,font=font2,show='*',text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Password', placeholder_text_color='#a3a3a3',width=200,height=50)
    password_entry2.place(x=230,y=220)
    
    login_button2 =customtkinter.CTkButton(frame2,command = login_account,text_color='#fff',text='Login in',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2', corner_radius=5, width=120)
    login_button2.place(x=230,y=290)

frame1 = customtkinter.CTkFrame(app, bg_color='#001220', fg_color='#001220',width = 470, height = 360)
frame1.place(x = 0, y = 0)

#image_path = "Together_image.jpg"
#image1 = PhotoImage(file=image_path)
#image_label = Label(frame1, image=image1,bg='#001220')
#image1_label.place(x=0, y=0)

signup_label = customtkinter.CTkLabel(frame1, font=font1, text='Sign up',text_color='#fff', bg_color='#001220')
signup_label.place(x=230, y=20)

username_entry = customtkinter.CTkEntry(frame1, font= font2,text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text ='Username',placeholder_text_color='#a3a3a3',width=200, height=50)
username_entry.place(x=230,y=150)

password_entry = customtkinter.CTkEntry(frame1, font=font2, show= '*', text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text='Password', placeholder_text_color='#a3a3a3',width=200,height=50)
password_entry.place(x=230,y=220)

signup_button = customtkinter.CTkButton(frame1,font=font2,command=signup, text_color='#fff',text='Sign up',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2', corner_radius=5, width=120)
signup_button.place(x=230,y=290)

login_label = customtkinter.CTkLabel(frame1, font=font3,text='Already have an account?', text_color='#fff',bg_color='#001220')
login_label.place(x=230,y=330)

login_button = customtkinter.CTkButton(frame1,command=login, font=font4, text_color='#00bf77',text='Login',fg_color='#001220', hover_color='#001220',cursor='hand2', width=40)
login_button.place(x=395,y=330)


app.mainloop()