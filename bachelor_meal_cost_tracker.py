from tkinter import *
from tkinter import messagebox
from db import Database

db = Database('store.db')


def populate_list():
    bachelor_list.delete(0, END)
    for row in db.fetch():
        bachelor_list.insert(END, row)


def add_item():
    if student_text.get() == '' or date_text.get() == '' or shift_text.get() == '' or meal_text.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    db.insert(student_text.get(), date_text.get(),
              shift_text.get(), meal_text.get())
    bachelor_list.delete(0, END)
    bachelor_list.insert(END, (student_text.get(), date_text.get(),
                            shift_text.get(), meal_text.get()))
    clear_text()
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = bachelor_list.curselection()[0]
        selected_item = bachelor_list.get(index)

        student_entry.delete(0, END)
        student_entry.insert(END, selected_item[1])
        date_entry.delete(0, END)
        date_entry.insert(END, selected_item[2])
        shift_entry.delete(0, END)
        shift_entry.insert(END, selected_item[3])
        meal_entry.delete(0, END)
        meal_entry.insert(END, selected_item[4])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()


def update_item():
    db.update(selected_item[0], student_text.get(), date_text.get(),
              shift_text.get(), meal_text.get())
    populate_list()


def clear_text():
    student_entry.delete(0, END)
    date_entry.delete(0, END)
    shift_entry.delete(0, END)
    meal_entry.delete(0, END)


# Create window object
app = Tk()

# Student
student_text = StringVar()
student_label = Label(app, text='Student Name', font=('bold', 14), pady=20)
student_label.grid(row=0, column=0, sticky=W)
student_entry = Entry(app, textvariable=student_text)
student_entry.grid(row=0, column=1)
# Date
date_text = StringVar()
date_label = Label(app, text='Date', font=('bold', 14))
date_label.grid(row=0, column=2, sticky=W)
date_entry = Entry(app, textvariable=date_text)
date_entry.grid(row=0, column=3)
# Shift
shift_text = StringVar()
shift_label = Label(app, text='Shift', font=('bold', 14))
shift_label.grid(row=1, column=0, sticky=W)
shift_entry = Entry(app, textvariable=shift_text)
shift_entry.grid(row=1, column=1)
# meal
meal_text = StringVar()
meal_label = Label(app, text='Meal Cost', font=('bold', 14))
meal_label.grid(row=1, column=2, sticky=W)
meal_entry = Entry(app, textvariable=meal_text)
meal_entry.grid(row=1, column=3)
# Parts List (Listbox)
bachelor_list = Listbox(app, height=8, width=50, border=0)
bachelor_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)
# Set scroll to listbox
bachelor_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=bachelor_list.yview)
# Bind select
bachelor_list.bind('<<ListboxSelect>>', select_item)

# Buttons
add_btn = Button(app, text='Add Entry', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text='Remove Entry', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text='Update Entry', width=12, command=update_item)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text='Clear Entry', width=12, command=clear_text)
clear_btn.grid(row=2, column=3)

app.title('Bachelor Meal Cost Tracker')
app.geometry('700x350')

# Populate data
populate_list()

# Start program
app.mainloop()


# To create an executable, install pyinstaller and run
# '''
# pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' part_manager.py
# '''