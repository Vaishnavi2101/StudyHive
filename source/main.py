import tkinter as tk
from tkinter import Scrollbar
from tkinter import messagebox
import mysql.connector

# Establishing database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="wise2"
)
cursor = db.cursor()

# Create tables if not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        password VARCHAR(255)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_groups (
        id INT AUTO_INCREMENT PRIMARY KEY,
        group_name VARCHAR(255) UNIQUE,
        creator_id INT,
        FOREIGN KEY (creator_id) REFERENCES user(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS group_members (
        group_id INT,
        user_id INT,
        FOREIGN KEY (group_id) REFERENCES study_groups(id),
        FOREIGN KEY (user_id) REFERENCES user(id),
        PRIMARY KEY (group_id, user_id)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        group_name VARCHAR(255),
        question_text LONGTEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        question_id INT,
        user_id INT,
        answer_text LONGTEXT,
        FOREIGN KEY (question_id) REFERENCES questions(id),
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
""")

db.commit()


def login_page():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("1700x1700")
    def login():
        username = username_entry.get()
        password = password_entry.get()

        cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        if result:
            login_window.destroy()
            main_page(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

    def open_register_page():
        login_window.destroy()
        register_page()
    tk.Label(login_window, text="Login", font=("Helvetica", 30, "bold")).pack(pady=10)
    tk.Label(login_window, text="Username:", font=("Helvetica", 12)).pack()
    username_entry = tk.Entry(login_window, width=30,font=("Helvetica", 14))  # Increase the height to 5 lines
    username_entry.pack(pady=10,ipady=10)
    
    tk.Label(login_window, text="Password:", font=("Helvetica", 12)).pack()
    password_entry = tk.Entry(login_window,show="*", width=30,font=("Helvetica", 14))  # Increase the height to 5 lines
    password_entry.pack(pady=10,ipady=10)
    frame = tk.Frame(login_window)
    frame.pack(pady=10)

    tk.Label(frame, text="Not a user?", font=("Helvetica", 12)).pack(side="left")
    tk.Button(frame, text="Register", command=open_register_page, width="10", height="1", font=("Helvetica", 12), fg="black", bg="pink").pack(side="left", padx=10)
    tk.Button(login_window, text="Login", command=login,width="10",height="1" ,font=("Helvetica", 12),fg="black",bg="pink").pack(pady=10)
    #tk.Button(login_window, text="Register", command=open_register_page,width="10",height="1" ,font=("Helvetica", 12),fg="black",bg="pink").pack(pady=10)

    login_window.mainloop()

def register_page():
    def back_to_login():
        register_window.destroy()
        login_page()
    def register():
        username = username_entry.get()
        password = password_entry.get()
        if not username:
            messagebox.showerror("Registration Failed", "Username cannot be empty.")
            return
        if any(char.isdigit() for char in username):
            messagebox.showerror("Registration Failed", "Username cannot contain numbers.")
            return

        # Check if username length is less than 6 characters
        if len(username) < 6:
            messagebox.showerror("Registration Failed", "Username should be at least 6 characters long.")
            return

        if len(password) < 6:
            messagebox.showerror("Registration Failed", "Password should contain at least 6 characters.")
            return

        cursor.execute("SELECT id FROM user WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            messagebox.showerror("Registration Failed", "Username already exists. Please choose a different one.")
        else:
            cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            messagebox.showinfo("Registration Successful", "Account created successfully. You can now login.")
            register_window.destroy()
            login_page()

    register_window = tk.Tk()
    register_window.title("Register")
    register_window.geometry("1700x1700")
    tk.Label(register_window, text="Register", font=("Helvetica", 30, "bold")).pack(pady=10)
    tk.Label(register_window, text="Username:", font=("Helvetica", 12)).pack()
    username_entry = tk.Entry(register_window, width=30,font=("Helvetica", 14))  # Increase the height to 5 lines
    username_entry.pack(pady=10,ipady=10)
    
    tk.Label(register_window, text="Password:", font=("Helvetica", 12)).pack()
    password_entry = tk.Entry(register_window,show="*", width=30,font=("Helvetica", 14))  # Increase the height to 5 lines
    password_entry.pack(pady=10,ipady=10)


    tk.Button(register_window, text="Register", command=register,width="10",height="1" ,font=("Helvetica", 12),fg="black",bg="pink").pack(pady=10)
    tk.Button(register_window, text="Back to Login", command=back_to_login, width="15", height="1", font=("Helvetica", 12), fg="black", bg="pink").pack(pady=10)
    create_window_buttons(register_window, lambda: register_window.destroy())

    register_window.mainloop()


def main_page(username):
    root = tk.Tk()
    root.title("Group Management")
    root.geometry("1700x1700")

    def logout():
        root.destroy()
        login_page()

    def create_group():
        create_group_window(root, username)

    def join_group():
        join_group_window(root, username)

    # Create frame to hold the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, fill=tk.X)  # Pack the frame at the top of the window
    tk.Button(root, text="Create group", command=create_group,width="15",height="2" ,font=("Helvetica", 12),fg="black",bg="pink").pack(pady=10)
    tk.Button(root, text="Join group", command=join_group,width="15",height="2" ,font=("Helvetica", 12),fg="black",bg="pink").pack(pady=10)
    tk.Button(button_frame, text="Logout", command=logout,width="10",height="2" ,font=("Helvetica", 12),fg="black",bg="pink").pack(side=tk.RIGHT, padx=10)
    

    tk.Label(root, text="Joined Groups:", font=("Helvetica", 20, "bold")).pack(pady=10)
    joined_groups = get_joined_groups(username)
    for group in joined_groups:
        tk.Button(root, text=group, command=lambda g=group: group_page(root, g, username),width="10",height="2" ,font=("Helvetica", 12),fg="black",bg="pink").pack(padx=10,pady=10)

    root.mainloop()
    
def create_group_window(root, username):
    def submit_group(group_name):
        try:
            cursor.execute("SELECT id FROM user WHERE username = %s", (username,))
            creator_id = cursor.fetchone()[0]

            cursor.execute("SELECT group_name FROM study_groups WHERE LOWER(group_name) = LOWER(%s)", (group_name,))
            existing_group = cursor.fetchone()
            if existing_group:
                messagebox.showerror("Error", f"Group '{group_name}' already exists")
            else:
                cursor.execute("INSERT INTO study_groups (group_name, creator_id) VALUES (%s, %s)", (group_name, creator_id))
                db.commit()
                messagebox.showinfo("Group Created", f"Group '{group_name}' created successfully!")
                joined_groups = get_joined_groups(username)
                refresh_joined_groups(joined_groups)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to check or create group '{group_name}': {err}")

        group_window.destroy()

    group_window = tk.Toplevel(root)
    group_window.title("Create Group")
    group_window.geometry("1700x1700")
    
    label_group_name = tk.Label(group_window, text="Enter Group Name:",font=("Helvetica", 15))
    label_group_name.pack(pady=10,ipady=10)

    entry_group_name = tk.Entry(group_window,width="30", font=("Helvetica", 12))
    entry_group_name.pack(pady=5,ipady=10)

    submit_button = tk.Button(group_window, text="Submit",
                              command=lambda: submit_group(entry_group_name.get()),
                              font=("Helvetica", 12),bg="pink",fg="black",width=10,height="2")
    submit_button.pack(pady=10)

    create_window_buttons(group_window)

def join_group_window(root, username):
    def join_group():
        group_name = entry_group_name.get()
        try:
            cursor.execute("SELECT id FROM study_groups WHERE group_name = %s", (group_name,))
            group_id_result = cursor.fetchone()
            if group_id_result:
                group_id = group_id_result[0]
                cursor.execute("SELECT id FROM user WHERE username = %s", (username,))
                user_id_result = cursor.fetchone()
                if user_id_result:
                    user_id = user_id_result[0]
                    cursor.execute("INSERT INTO group_members (group_id, user_id) VALUES (%s, %s)", (group_id, user_id))
                    db.commit()
                    messagebox.showinfo("Group Joined", f"You have successfully joined the group '{group_name}'!")
                    join_window.destroy()
                    main_page(username) 
                else:
                    messagebox.showerror("Error", "User ID not found")
            else:
                messagebox.showerror("Error", f"Group '{group_name}' not found")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to join group '{group_name}': {err}")

    join_window = tk.Toplevel(root)
    join_window.title("Join Group")
    join_window.geometry("1700x1700")

    label_group_name = tk.Label(join_window, text="Enter Group Name:", font=("Helvetica", 15))
    label_group_name.pack(pady=10)

    entry_group_name = tk.Entry(join_window,width="30" ,font=("Helvetica", 12))
    entry_group_name.pack(pady=5,ipady=10)

    join_button = tk.Button(join_window, text="Join", command=join_group, font=("Helvetica", 12),width="10",height="2",fg="black",bg="pink")
    join_button.pack(pady=10)

    create_window_buttons(join_window)

def get_joined_groups(username):
    cursor.execute("""
        SELECT study_groups.group_name FROM study_groups 
        INNER JOIN group_members ON study_groups.id = group_members.group_id 
        INNER JOIN user ON user.id = group_members.user_id 
        WHERE user.username = %s
    """, (username,))
    return cursor.fetchall()


def create_window_buttons(window, back_command=None):
    def back():
        if back_command:
            back_command()
        else:
            window.destroy()

    back_button = tk.Button(window, text="Back", command=back, width=20, height=2)
    back_button.pack(side=tk.BOTTOM, pady=10)
    
def group_page(root, group_name, username):
    group_name = group_name[0]  
    def display_questions(group_name):
        try:
            cursor.execute("SELECT * FROM questions WHERE group_name = %s", (group_name,))
            questions = cursor.fetchall()

            for question in questions:
                question_label = tk.Label(group_window, text=question[2], font=("Helvetica", 12))
                question_label.pack(pady=5)
        
                
                answer_button = tk.Button(group_window, text="Answer", command=lambda q=question: display_answers(q[0],q[2], username))
                answer_button.pack(pady=2)
        except mysql.connector.Error as err:
            print("Error fetching questions:", err)

    group_window = tk.Toplevel(root)
    group_window.title(group_name)
    group_window.geometry("1700x1700")

    tk.Label(group_window, text=f"Group: {group_name}", font=("Helvetica", 15)).pack(pady=10)

    post_question_button = tk.Button(group_window, text="Post Question", command=lambda: post_question(group_name, username),font=("Helvetica",15),width="20",height="1",bg="pink",fg="black")
    post_question_button.pack(pady=5)

    display_questions(group_name)

    create_window_buttons(group_window, lambda: group_window.destroy())


def post_question(group_name, username):
    def submit_question():
        question_text = question_entry.get()
        try:
            cursor.execute("INSERT INTO questions (group_name, question_text) VALUES (%s, %s)", (group_name, question_text))
            db.commit()
            messagebox.showinfo("Question Posted", "Your question has been posted successfully!")
            question_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to post question: {err}")

    question_window = tk.Toplevel()
    question_window.title("Post Question")
    question_window.geometry("1700x1700")

    tk.Label(question_window, text="Enter Your Question:", font=("Helvetica", 15)).pack(pady=5)
    question_entry = tk.Entry(question_window, width=50)
    question_entry.pack(pady=5,ipady=10)

    submit_button = tk.Button(question_window, text="Submit", command=submit_question,bg="pink",fg="black",width="15",height="1",font=("Helevetica",10))
    submit_button.pack(pady=10)

    create_window_buttons(question_window)

    question_window.mainloop()
def display_answers(question_id, question_text, username):
    def submit_answer(username):
        answer = answer_entry.get()
        try:
            cursor.execute("SELECT id FROM user WHERE username = %s", (username,))
            user_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO answers (question_id, user_id, answer_text) VALUES (%s, %s, %s)",
                           (question_id, user_id, answer))
            db.commit()

            messagebox.showinfo("Answer Submitted", "Your answer has been submitted successfully!")
            answer_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to submit answer: {err}")

    answer_window = tk.Toplevel()
    answer_window.title("Answer Question")
    answer_window.geometry("1700x800")

    tk.Label(answer_window, text="Question:", font=("Helvetica", 15)).pack(pady=10)
    tk.Label(answer_window, text=question_text, font=("Helvetica", 15)).pack(pady=10)

    tk.Label(answer_window, text="Answers:", font=("Helvetica", 15)).pack(pady=10)

    # Create a Frame to hold the answers
    answer_frame = tk.Frame(answer_window)
    answer_frame.pack(pady=10)

    try:
        cursor.execute("SELECT answer_text FROM answers WHERE question_id = %s", (question_id,))
        answers = cursor.fetchall()

        # Create a Scrollbar
        scrollbar = Scrollbar(answer_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Text widget to display answers
        answer_text = tk.Text(answer_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        answer_text.pack(expand=True, fill=tk.BOTH)

        scrollbar.config(command=answer_text.yview)

        # Display answers in the Text widget
        for idx, answer in enumerate(answers, start=1):
            answer_text.insert(tk.END, f"{idx}. {answer[0]}\n\n")

    except mysql.connector.Error as err:
        print("Error fetching answers:", err)

    tk.Label(answer_window, text="Your Answer:", font=("Helvetica", 15)).pack()
    answer_entry = tk.Entry(answer_window, width=50)
    answer_entry.pack(pady=10, ipady=10)

    submit_button = tk.Button(answer_window, text="Submit", command=lambda: submit_answer(username), bg="pink", fg="black", width="15", height="1", font=("Helvetica", 15))
    submit_button.pack(pady=10)

    create_window_buttons(answer_window)

    answer_window.mainloop()


login_page()