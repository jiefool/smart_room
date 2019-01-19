try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import * 
class Calculator:

    def __init__(self, master):
        self.master = master
        master.title("Smart Room")

        self.entered_username = '';
        self.entered_password = '';

        vcmd = master.register(self.validate) # we have to wrap the command
        self.username_label = Label(master, text="Username:")
        self.username_entry = Entry(master, validate="key", validatecommand=(vcmd, 'username','%P'))

        self.password_label = Label(master, text="Password:")
        self.password_entry = Entry(master, validate="key", validatecommand=(vcmd, 'password', '%P'))

        self.login_button = Button(master, text="Login", command=lambda: self.login)

        # LAYOUT

        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=1, column=0)

        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=3, column=0)

        self.login_button.grid(row=4, column=0)
       

    def validate(self, field, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def login(self):
        if method == "add":
            self.total += self.entered_number
        elif method == "subtract":
            self.total -= self.entered_number
        else: # reset
            self.total = 0

        self.total_label_text.set(self.total)
        self.entry.delete(0, END)

root = Tk()
my_gui = Calculator(root)
root.mainloop()