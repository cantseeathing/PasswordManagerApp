from tkinter import *
from tkinter import messagebox
import base64
import random
import pandas as pd

BACKGROUND = "white"
FONT_NAME = "Areal"
FONT_COLOR = "black"
FONT_SIZE = 9
FILE_NAME = "password_list.txt"
DEFUALT_EMAIL = "mahmoued_999@hotmail.com"
ENCODE = True
PASSWORD = "123"

global passcode_entry
global window3


def check_database(file_name):
    try:
        with open(file_name, mode="r") as file:
            content = file.read()
            database = content
            if ENCODE:
                # database = [values for values in content.split("\n") if values != ""]
                database = [(base64.b64decode(values.encode("ascii"))).decode("ascii") for values in
                            content.split("\n") if values != ""]
    except FileNotFoundError:
        file = open(file_name, mode="w")
        content = ""
        file.write(str(content))
        database = content
    return database


def save_password():
    password = password_entry.get()
    user = user_entry.get()
    website = website_entry.get()
    if password == "" or user == "" or website == "":
        messagebox.showerror(title="Missing information", message="Please fill all the required information!")
    else:
        confirmation = messagebox.askokcancel(title="Confirmation", message=f"Please confirm the following information:"
                                                                            f"\nWebsite: {website}\nEmail/User: "
                                                                            f"{user}\nPassword: {password}")
        if confirmation:
            with open(FILE_NAME, mode="a") as file:
                new_entry = str(str(website) + "|" + str(user) + "|" + str(password))
                if ENCODE:
                    new_entry = new_entry.encode("ascii")
                    base64_bytes = base64.b64encode(new_entry)
                    base64_string = base64_bytes.decode("ascii")
                    output = str(base64_string) + str("\n")
                else:
                    output = new_entry + str('\n')
                file.write(str(output))
                file.close()
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)
    letters_list = [random.choice(letters) for char in range(nr_letters)]
    symbols_list = [random.choice(symbols) for char in range(nr_symbols)]
    numbers_list = [random.choice(numbers) for char in range(nr_numbers)]
    password_list = letters_list + symbols_list + numbers_list
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(END, string=password)


def check_passcode():
    if passcode_entry.get() == PASSWORD:
        window3.destroy()
        show_password()
    else:
        messagebox.showerror(title="Password Database", message="Wrong password!")


def check_password():
    global window3
    global passcode_entry
    window.destroy()
    window3 = Tk()
    window3.focus()
    window3.config(padx=25, pady=25, background=BACKGROUND)
    window3.title("Password Database")

    passcode_label = Label(text="Enter the password to access the database:", background=BACKGROUND)
    passcode_label.grid(column=0, row=0)

    passcode_entry = Entry(width=30)
    passcode_entry.insert(END, string="")
    passcode_entry.focus()
    passcode_entry.grid(row=1, column=0)

    passcode_button = Button(text="Access Database", command=check_passcode)
    passcode_button.grid(row=2, column=0)


def show_password():
    db = check_database(FILE_NAME)
    if len(db) != 0:
        window2 = Tk()
        window2.config(padx=25, pady=25, background=BACKGROUND)
        window2.title("Password Database")
        pass_list = []
        user_list = []
        site_list = []
        for i in range(len(db)):
            temp = db[i].split("|")
            pass_list.append(temp[2])
            user_list.append(temp[1])
            site_list.append(temp[0])
        df = pd.DataFrame(columns=["Website", "Email/User", "Password"], index=range(len(db)))
        for i in range(len(db)):
            df.iloc[i] = [site_list[i], user_list[i], pass_list[i]]
        df.set_index("Website", inplace=True)
        print(df)
        data_label = Label(text=df, background=BACKGROUND)
        data_label.grid(row=0, column=0)
    else:
        messagebox.showerror(title="Password Database", message="Nothing to show, empty database!")


# # UI SETUP
dataset = check_database(file_name=FILE_NAME)
# WINDOW SETUP
window = Tk()
window.config(padx=25, pady=25, background=BACKGROUND)
window.title("Password Manager App v1.0")
# LOGO SETUP
canvas = Canvas(width=200, height=200, bg=BACKGROUND, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)
# LABELS SETUP
website_label = Label(text="Website:", background=BACKGROUND)
website_label.grid(column=0, row=1)

user_label = Label(text="User Name/Email:", background=BACKGROUND)
user_label.grid(column=0, row=2)

password_label = Label(text="Password:", background=BACKGROUND)
password_label.grid(column=0, row=3)
# ENTRIES SETUP
website_entry = Entry(width=35)
website_entry.focus()
website_entry.insert(END, string="")
website_entry.grid(row=1, column=1, columnspan=2)

user_entry = Entry(width=35)
user_entry.insert(END, string=DEFUALT_EMAIL)
user_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=30)
password_entry.insert(END, string="")
password_entry.grid(row=3, column=1)
# BUTTONS SETUP
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add Password", width=22, command=save_password)
add_button.grid(row=4, column=1)

show_button = Button(text="Show Passwords", width=22, command=check_password)
show_button.grid(row=4, column=2)

window.mainloop()
