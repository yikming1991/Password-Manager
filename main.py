from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pw():
    password_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, f"{password}")
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_info():
    website_to_save = website_input.get().upper()
    user_to_save = email_username_input.get()
    password_to_save = password_input.get()
    new_data = {
        website_to_save: {
            "email": user_to_save,
            "password": password_to_save,
            }
        }

    if website_to_save == "" or user_to_save == "" or password_to_save == "":
        messagebox.showinfo(title="Empty fields", message="Do not leave any fields empty!")
    try:
        with open("passwords.json", mode="r") as file:
            data = json.load(file)  # reading JSON data produces a list

    except FileNotFoundError:
        with open("passwords.json", mode="w") as file:
            json.dump(new_data, file, indent=4) # saving updated JSON data
            # file.write(f"{website_to_save}  |  {user_to_save}  |  {password_to_save}\n")

    else:
        data.update(new_data)   # Updating old data with new data, appends new data to existing dictionary
        with open("passwords.json", mode="w") as file:
            json.dump(data, file, indent=4)

    finally:
        website_input.delete(0, END)
        password_input.delete(0, END)
        # email_username_input.delete(0, END)

# ---------------------------- SEARCH ------------------------------- #
def search():
    website_to_search = website_input.get().upper()
    try:
        with open("passwords.json", mode="r") as file:
            data = json.load(file)  # reading JSON data produces a list

    except FileNotFoundError:
        messagebox.showinfo(title="No datafile found",
                            message="There is no password information stored yet.")
    else:
        try:
            login_info = data[website_to_search]
        except KeyError:
            password_input.delete(0, END)
            messagebox.showinfo(title="Website not found",
                                message="Details for that website does not exist.")
        else:
            # ------- Create popup box to display login info  ------- #
            # message = f"Email: {login_info['email']}" \
            #           f"\nPassword:{login_info['password']}"
            # messagebox.showinfo(title=f"Website - {website_to_search}", message=message)

            # ------- Populate email and password fields for easier copying ------- #
            email_username_input.delete(0,END)
            password_input.delete(0, END)
            email_username_input.insert(0, f"{login_info['email']}")
            password_input.insert(0, f"{login_info['password']}")
            messagebox.showinfo(title=f"Website - {website_to_search}",
                                message="Info found, see entry fields")


# ---------------------------- CLEAR ------------------------------- #
def clear():
    website_input.delete(0, END)
    password_input.delete(0, END)
    email_username_input.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.minsize(width=200, height=200)
window.config(padx=20, pady=20)

canvas = Canvas(height=200, width=200)
background = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=background)
canvas.grid(column=1, row=0, sticky="EW")

website = Label(text="Website:")
website.grid(column=0, row=1)
website_input = Entry()
website_input.focus()
website_input.grid(column=1, row=1, columnspan=1, sticky="EW")

email_username = Label(text="Email/Username:")
email_username.grid(column=0, row=2)
email_username_input = Entry()
email_username_input.insert(0, "yikming1991@gmail.com")
email_username_input.grid(column=1, row=2, columnspan=2, sticky="EW")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_input = Entry(width=21)
password_input.grid(column=1, row=3, sticky="EW")

add_button = Button(text="Add", width=45, command=save_info)
add_button.grid(column=1, row=4, columnspan=2)

generate_password = Button(text="Generate Password", command=generate_pw)
generate_password.grid(column=2, row=3, sticky="EW")

search_button = Button(text="Search", command=search)
search_button.grid(column=2, row=1, columnspan=1, sticky="EW")

clear_button = Button(text="Clear", width=45, command=clear)
clear_button.grid(column=1, row=5, columnspan=2)


window.mainloop()