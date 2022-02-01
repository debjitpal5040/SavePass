from tkinter import *
from tkinter import messagebox
import json
import pyperclip
import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '~', '@', '#', '$', '%', '^', '&', '(', ')', '*', '+', '_', '-', '=', '<', '>', '?', '/', '|', '{', '}', '[', ']', ';', ':', ',']

def password_generator():
    nr_letters = random.randint(6, 8)
    nr_symbols = random.randint(3, 5)
    nr_numbers = random.randint(3, 5)
    password = [random.choice(letters) for i in range(nr_letters)]
    password += [random.choice(symbols) for i in range(nr_symbols)]
    password += [random.choice(numbers) for i in range(nr_numbers)]
    random.shuffle(password)
    password = "".join(password)
    return password

WINDOW_BG = "black"
FIELD_COLORS = "white"
FIELD_FONT_COLOR = "green"
LABEL_COLOR = "white"
FONT = ("Ubuntu", 15, "bold")

def get_password():
    password = password_generator()
    pyperclip.copy(password)
    password_entry.delete(0, END)
    password_entry.insert(END, password)

def database_manager(new_user_entry):
    try:
        with open("data.json", mode="r") as old_password_file:
            password_data = json.load(old_password_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open("data.json", mode="w") as new_password_file:
            json.dump(new_user_entry, new_password_file, indent=4)
    else:
        password_data.update(new_user_entry)
        with open("data.json", mode="w") as old_password_file:
            json.dump(password_data, old_password_file, indent=4)
    finally:
        website_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)

def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please fill all the fields")
    else:
        is_ok = messagebox.askokcancel(title="Confirm entries", message=f"These are the credentials you entered\n"
                                                                        f"Email/Username : {email}"
                                                                        f"\nPassword : {password}\nDo you want to save these ?")
        if is_ok:
            pyperclip.copy(password)
            new_entry_in_json = {
                website:
                    {
                        "Email": email,
                        "Password": password
                    }
            }
            database_manager(new_entry_in_json)

def search_password():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please enter a website to search")
    else:
        try:
            with open("data.json", mode="r") as old_password_file:
                password_data = json.load(old_password_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            messagebox.showinfo(title="No passwords saved", message="You have not yet saved any passwords")
        else:
            if website in password_data:
                email = password_data[website]["Email"]
                password = password_data[website]["Password"]
                is_clipboard = messagebox.askokcancel(title=website, message=f"Email/Username : {email}\nPassword : {password}"
                                                    f"\n\nSave to clipboard ?")
                if is_clipboard:
                    pyperclip.copy(password)
                    messagebox.showinfo(
                        title="Saved to clipboard", message="Password has been saved to clipboard")
            else:
                messagebox.showinfo(title="Password not saved for this website", message=f"The password for {website}\n" f"has not been saved")

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg=WINDOW_BG)

PASS_IMG = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200, bg=WINDOW_BG, highlightthickness=0)
canvas.config()
canvas.create_image(100, 100, image=PASS_IMG)
canvas.grid(column=1, row=0)

website_label = Label(text="Website", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
website_label.grid(column=0, row=1, sticky=W)

email_label = Label(text="Email/Username", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
email_label.grid(column=0, row=2, sticky=W)

password_label = Label(text="Password", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
password_label.grid(column=0, row=3, sticky=W)
window.grid_columnconfigure(1, weight=1)

website_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
website_entry.insert(END, string="")
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
email_entry.insert(END, string="")
email_entry.grid(column=1, row=2)

password_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
password_entry.insert(END, string="")
password_entry.grid(column=1, row=3)

search_button = Button(text="Search", font=FONT, command=search_password)
search_button.grid(column=5, row=1)

generate_button = Button(text="Generate Strong Password", font=FONT, command=get_password)
generate_button.grid(column=5, row=3)

add_button = Button(text="Save Credentials", font=FONT, command=save_password)
add_button.grid(column=1, row=5)

dummy_label = Label(bg=WINDOW_BG)
dummy_label.grid(column=0, row=4, sticky=W)
dummy_label2 = Label(bg=WINDOW_BG)
dummy_label2.grid(column=4, row=3, sticky=W)

window.mainloop()