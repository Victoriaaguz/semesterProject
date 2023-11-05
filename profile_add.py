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
        username TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT,
        bio TEXT,
        location TEXT,
        avail TEXT
    );''')

conn.commit()
profile_frame = None
user_profiles = {}

def save_profile_changes(username, full_name_entry, bio_entry, location_entry, avail_entry):
    new_full_name = full_name_entry.get()
    new_bio = bio_entry.get()
    new_location = location_entry.get()
    new_avail = avail_entry.get()

    # Define a dictionary to hold the updated profile data
    updated_profile = {
        "full_name": new_full_name,
        "bio": new_bio,
        "location": new_location,
        "avail": new_avail
    }

    # Update user profiles in the dictionary
    user_profile = user_profiles.get(username, {})
    user_profile.update(updated_profile)

    # Define a list of column names to be updated in the database
    columns_to_update = list(updated_profile.keys())

    # Create the SET clause for the SQL UPDATE statement
    set_clause = ', '.join([f"{column} = ?" for column in columns_to_update])

    # Construct the SQL UPDATE statement
    update_query = f"UPDATE users SET {set_clause} WHERE username = ?"

    # Extract the values for the SQL statement
    values = list(updated_profile.values())
    values.append(username)  # Add the username as the last value

    # Execute the SQL statement to update the database
    cursor.execute(update_query, values)
    conn.commit()
    
    messagebox.showinfo('Success', 'Profile updated successfully.')

    # Return to the user's profile
    open_profile(username)


def cancel_edit(username):
    # Return without saving changes to db
    open_profile(username)
    
def edit_user_profile(username):
    global edit_frame
    edit_frame = customtkinter.CTkFrame(app, bg_color='#001220', fg_color='#001220', width=470, height=360)
    edit_frame.place(x=0, y=0)

    edit_label = customtkinter.CTkLabel(edit_frame, font=font1, text='Edit Profile', text_color='#fff', bg_color='#001220')
    edit_label.place(x=180, y=20)

    # Check if user has existing profile
    user_profile = user_profiles.get(username, {})
    
    # Create entries for editing user information
    full_name_entry = customtkinter.CTkEntry(edit_frame, font=font3, text_color='#fff', fg_color='#001a2e',
                                             bg_color='#121111', border_color='#004780', border_width=3,
                                             placeholder_text=f'Full Name ({user_profile.get("full_name", "")})',
                                             placeholder_text_color='#a3a3a3', width=300)
    full_name_entry.place(x=85, y=100)

    bio_entry = customtkinter.CTkEntry(edit_frame, font=font3, text_color='#fff', fg_color='#001a2e',
                                         bg_color='#121111', border_color='#004780', border_width=3,
                                         placeholder_text=f'Bio ({user_profile.get("bio", "")})',
                                         placeholder_text_color='#a3a3a3', width=300)
    bio_entry.place(x=85, y=150)

    location_entry = customtkinter.CTkEntry(edit_frame, font=font3, text_color='#fff', fg_color='#001a2e',
                                            bg_color='#121111', border_color='#004780', border_width=3,
                                            placeholder_text=f'Location ({user_profile.get("location", "")})',
                                            placeholder_text_color='#a3a3a3', width=300)
    location_entry.place(x=85, y=200)

    avail_entry = customtkinter.CTkEntry(edit_frame, font=font3, text_color='#fff', fg_color='#001a2e',
                                         bg_color='#121111', border_color='#004780', border_width=3,
                                         placeholder_text=f'Availability ({user_profile.get("avail", "")})',
                                         placeholder_text_color='#a3a3a3', width=300)
    avail_entry.place(x=85, y=250)

    # Create a "Save" button to save the changes to the profile
    save_button = customtkinter.CTkButton(edit_frame, font=font3, text='Save', text_color='#fff', fg_color='#00965d', hover_color='#006e44', bg_color='#121111', cursor='hand2', width=100, command= lambda: save_profile_changes(username, full_name_entry, bio_entry, location_entry, avail_entry))
    save_button.place(x=150, y=300)

    # Create a "Cancel" button to go back to the user profile
    cancel_button = customtkinter.CTkButton(edit_frame, font=font3, text='Cancel', text_color='#fff', fg_color='#ff4a4a', hover_color='#a61b1b', bg_color='#121111', cursor='hand2', width=100, command= lambda: cancel_edit(username))
    cancel_button.place(x=250, y=300)

def go_back_to_login():
    global profile_frame
    global edit_frame
    if edit_frame is not None: 
        edit_frame.destroy()
    if profile_frame is not None:
        profile_frame.destroy()
    frame2.place(x=0, y=0)

def open_profile(username):
    global profile_frame

    profile_frame = customtkinter.CTkFrame(app, bg_color='#001220', fg_color='#001220', width=470, height=360)
    profile_frame.place(x=0, y=0)

    profile_label = customtkinter.CTkLabel(profile_frame, font=font1, text=f'Welcome, {username}', text_color='#fff',
                                           bg_color='#001220')
    profile_label.place(x=180, y=20)

    user_info_label = customtkinter.CTkLabel(profile_frame, font=font3, text='User Information:', text_color='#fff',
                                             bg_color='#001220')
    user_info_label.place(x=150, y=100)

    # Retrieve user information from the database based on the username
    cursor.execute('SELECT full_name, bio, location, avail FROM users WHERE username = ?', [username])
    user_profile_data = cursor.fetchone()

    if user_profile_data:
        full_name, bio, location, avail = user_profile_data

        # Display user profile information
        full_name_label = customtkinter.CTkLabel(profile_frame, font=font3, text=f'Full Name: {full_name}',
                                                 text_color='#fff', bg_color='#001220')
        full_name_label.place(x=150, y=140)

        bio_label = customtkinter.CTkLabel(profile_frame, font=font3, text=f'Bio: {bio}',
                                           text_color='#fff', bg_color='#001220')
        bio_label.place(x=150, y=180)

        location_label = customtkinter.CTkLabel(profile_frame, font=font3, text=f'Location: {location}',
                                                text_color='#fff', bg_color='#001220')
        location_label.place(x=150, y=220)

        avail_label = customtkinter.CTkLabel(profile_frame, font=font3, text=f'Availability: {avail}',
                                            text_color='#fff', bg_color='#001220')
        avail_label.place(x=150, y=260)
    else:
        # Display default values or a message if the user doesn't exist in the database
        full_name_label = customtkinter.CTkLabel(profile_frame, font=font3, text='Full Name: Not available',
                                                 text_color='#fff', bg_color='#001220')
        full_name_label.place(x=150, y=140)

        bio_label = customtkinter.CTkLabel(profile_frame, font=font3, text='Bio: Not available',
                                           text_color='#fff', bg_color='#001220')
        bio_label.place(x=150, y=180)

        location_label = customtkinter.CTkLabel(profile_frame, font=font3, text='Location: Not available',
                                                text_color='#fff', bg_color='#001220')
        location_label.place(x=150, y=220)

        avail_label = customtkinter.CTkLabel(profile_frame, font=font3, text='Availability: Not available',
                                            text_color='#fff', bg_color='#001220')
        avail_label.place(x=150, y=260)

    # Add an "Edit Profile" button
    edit_profile_button = customtkinter.CTkButton(profile_frame, font=font3, text='Edit Profile', text_color='#fff',
                                                  fg_color='#00965d', hover_color='#006e44', bg_color='#121111',
                                                  cursor='hand2', width=120, command=lambda: edit_user_profile(username))
    edit_profile_button.place(x=150, y=300)

    # A button to log out
    logout_button = customtkinter.CTkButton(profile_frame, font=font3, text='Log Out', text_color='#fff',
                                            fg_color='#00965d', hover_color='#006e44', bg_color='#121111', cursor='hand2',
                                            width=100, command=go_back_to_login)
    logout_button.place(x=150, y=330)



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
                open_profile(username)
            else:
                messagebox.showerror('Error', 'Invalid password.')
        else:
            user_profiles[username] = {} # Empty profile for user
            messagebox.showerror('Error','Invalid username.')
    else: 
        messagebox.showerror('Error', 'Enter all data.')


def login():
    global frame2
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