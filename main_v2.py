from tkinter import *
from tkinter import messagebox
import base64
import random
import pandas as pd
import json
import pdb

BACKGROUND = "white"
FONT_NAME = "Areal"
FONT_COLOR = "black"
FONT_SIZE = 9
FILE_NAME = "password_list.json"
DEFUALT_EMAIL = "mahmoued_999@hotmail.com"
ENCODE = True
PASSWORD = "123"

global passcode_entry
global window3


def check_database(file_name):
    try:
        with open(file_name, "r") as file:
            content = json.load(file)
            data = content
            if ENCODE and data != {}:
                for key in data.fromkeys(data):
                    value = str(key)
                    print(f'value: {value}')
                    decoded_value = (base64.b64decode(str(value).encode("ascii"))).decode("ascii")
                    # data[decoded_value] = data[(list(data.keys()))[i]]
                    # del data[(list(data.keys()))[i]]
                    data[decoded_value] = data.pop(value)
                    for j in (list(data[decoded_value].keys())):
                        value = str(data[decoded_value][j])
                        decoded_value_sub = (base64.b64decode(value.encode("ascii"))).decode("ascii")
                        data[decoded_value][j] = decoded_value_sub
            content.update(data)
    except FileNotFoundError:
        file = open(file_name, "w")
        content = {}
        json.dump(content, file, indent=4)
        file.close()
    return content


def save_password():
    password = password_entry.get()
    user = user_entry.get()
    website = website_entry.get()
    new_data = {
        website: {
            "email": user,
            "password": password
        }
    }
    if password == "" or user == "" or website == "":
        messagebox.showerror(title="Missing information", message="Please fill all the required information!")
    else:
        confirmation = messagebox.askokcancel(title="Confirmation", message=f"Please confirm the following information:"
                                                                            f"\nWebsite: {website}\nEmail/User: "
                                                                            f"{user}\nPassword: {password}")
        if confirmation:
            old_content = check_database(FILE_NAME)
            if ENCODE:
                for i in range(len(list(new_data.keys()))):
                    value = str((list(new_data.keys()))[i]).encode("ascii")
                    encoded_value = base64.b64encode(value).decode("ascii")
                    new_data[encoded_value] = new_data[(list(new_data.keys()))[i]]
                    del new_data[(list(new_data.keys()))[i]]
                    for j in (list(new_data[encoded_value].keys())):
                        value = str(new_data[encoded_value][j]).encode("ascii")
                        encoded_value_sub = base64.b64encode(value).decode("ascii")
                        new_data[encoded_value][j] = encoded_value_sub
                output = new_data
            else:
                output = new_data
                # data = check_database(file_name=FILE_NAME)
                # data.update(output)
            with open(FILE_NAME, "r") as data_file:
                old_data = json.load(data_file)
                old_data.update(output)
            with open(FILE_NAME, "w") as data_file:
                json.dump(old_data, data_file, indent=4)
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
        # pass_list = []
        # user_list = []
        # site_list = []
        # for i in range(len(db)):
        #     temp = db[i].split("|")
        #     pass_list.append(temp[2])
        #     user_list.append(temp[1])
        #     site_list.append(temp[0])
        # df = pd.DataFrame(columns=["Website", "Email/User", "Password"], index=range(len(db)))
        # for i in range(len(db)):
        #     df.iloc[i] = [site_list[i], user_list[i], pass_list[i]]
        # df.set_index("Website", inplace=True)
        df = pd.DataFrame(check_database(FILE_NAME))
        print(df)
        data_label = Label(text=df, background=BACKGROUND)
        data_label.grid(row=0, column=0)
    else:
        messagebox.showerror(title="Password Database", message="Nothing to show, empty database!")


# # UI SETUP
# dataset = check_database(file_name=FILE_NAME)
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
