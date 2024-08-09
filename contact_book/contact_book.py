from tkinter import *
from tkinter import messagebox, ttk
import re
import os

root = Tk()

root.geometry('600x600')
root.title("Contact Book")

datas = []

contacts_file = "contacts.txt"


def is_valid_email(email):
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(regex, email)


def load_contacts():
    global datas
    if os.path.exists(contacts_file):
        with open(contacts_file, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    datas.append(line.split('|'))


def save_contacts():
    with open(contacts_file, "w") as file:
        for contact in datas:
            file.write('|'.join(contact) + '\n')


def add():
    global datas
    name = Name.get()
    number = Number.get()
    email = Email.get()
    addr = address.get(1.0, "end-1c")

    if not number.isdigit():
        messagebox.showerror(
            "Invalid Input", "Phone number should be an integer.")
        return

    if not is_valid_email(email):
        messagebox.showerror(
            "Invalid Input", "Email ID is not in correct format.")
        return

    datas.append([name, number, email, addr])
    update_book()
    save_contacts()
    reset()


def view():
    try:
        selected_item = tree.selection()[0]
        selection_index = int(tree.item(selected_item, 'values')[0])
    except IndexError:
        messagebox.showerror(
            "Selection Error", "Please select a contact to view.")
        return

    Name.set(datas[selection_index][0])
    Number.set(datas[selection_index][1])
    Email.set(datas[selection_index][2])
    address.delete(1.0, "end")
    address.insert(1.0, datas[selection_index][3])


def edit():
    global datas
    try:
        selected_item = tree.selection()[0]
        selection_index = int(tree.item(selected_item, 'values')[0])
    except IndexError:
        messagebox.showerror(
            "Selection Error", "Please select a contact to edit.")
        return

    name = Name.get()
    number = Number.get()
    email = Email.get()
    addr = address.get(1.0, "end-1c")

    if not number.isdigit():
        messagebox.showerror(
            "Invalid Input", "Phone number should be an integer.")
        return

    if not is_valid_email(email):
        messagebox.showerror(
            "Invalid Input", "Email ID is not in correct format.")
        return

    datas[selection_index] = [name, number, email, addr]

    update_book()
    save_contacts()

    reset()


def delete():
    try:
        selected_item = tree.selection()[0]
        selection_index = int(tree.item(selected_item, 'values')[0])
        del datas[selection_index]
        update_book()
        save_contacts()
    except IndexError:
        messagebox.showerror(
            "Selection Error", "Please select a contact to delete.")


def reset():
    Name.set('')
    Number.set('')
    Email.set('')
    address.delete(1.0, "end")


def update_book():
    for i in tree.get_children():
        tree.delete(i)
    for index, (n, p, e, a) in enumerate(datas):
        tree.insert("", "end", iid=index+1, values=(index+1, n, p, e, a))


Name = StringVar()
Number = StringVar()
Email = StringVar()

main_frame = Frame(root, padx=10, pady=10)
main_frame.pack(fill=BOTH, expand=True)

Label(main_frame, text='Contact Book', font='arial 18 bold').pack(pady=10)

form_frame = Frame(main_frame, pady=10)
form_frame.pack()

Label(form_frame, text='Name', font='arial 12 bold').grid(
    row=0, column=0, sticky=W, pady=5)
Entry(form_frame, textvariable=Name, width=50,
      font='arial 12').grid(row=0, column=1, pady=5)

Label(form_frame, text='Phone No.', font='arial 12 bold').grid(
    row=1, column=0, sticky=W, pady=5)
Entry(form_frame, textvariable=Number, width=50,
      font='arial 12').grid(row=1, column=1, pady=5)

Label(form_frame, text='Email ID', font='arial 12 bold').grid(
    row=2, column=0, sticky=W, pady=5)
Entry(form_frame, textvariable=Email, width=50,
      font='arial 12').grid(row=2, column=1, pady=5)

Label(form_frame, text='Address', font='arial 12 bold').grid(
    row=3, column=0, sticky=NW, pady=5)
address = Text(form_frame, width=37, height=5, font='arial 12')
address.grid(row=3, column=1, pady=5)

button_frame = Frame(main_frame, pady=10)
button_frame.pack()

Button(button_frame, text="Add", font="arial 12 bold", command=add,
       width=10, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10, pady=5)
Button(button_frame, text="View", font="arial 12 bold", command=view,
       width=10, bg="#2196F3", fg="white").grid(row=0, column=1, padx=10, pady=5)
Button(button_frame, text="Edit", font="arial 12 bold", command=edit,
       width=10, bg="#FF9800", fg="white").grid(row=0, column=2, padx=10, pady=5)
Button(button_frame, text="Delete", font="arial 12 bold", command=delete,
       width=10, bg="#f44336", fg="white").grid(row=0, column=3, padx=10, pady=5)
Button(button_frame, text="Reset", font="arial 12 bold", command=reset,
       width=10, bg="#FFC107", fg="white").grid(row=0, column=4, padx=10, pady=5)

list_frame = Frame(main_frame, pady=10)
list_frame.pack()

columns = ('Index', 'Name', 'Phone Number', 'Email', 'Address')
tree = ttk.Treeview(list_frame, columns=columns, show='headings')
tree.heading('Index', text='Index')
tree.heading('Name', text='Name')
tree.heading('Phone Number', text='Phone Number')
tree.heading('Email', text='Email')
tree.heading('Address', text='Address')
tree.pack(fill=BOTH, expand=True)

load_contacts()
update_book()

root.mainloop()
