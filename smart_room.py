#!/usr/bin/python

from Tkinter import *   ## notice capitalized T in Tkinter 
import time
import serial


class Login():

    def __init__(self, master):
        # defines a grid 50 x 50 cells in the main window

        self.master=master
        self.master.title('Smart Room Login')
        self.master.geometry('400x250')
        self.rows = 0
        while self.rows < 10:
            self.master.rowconfigure(self.rows, weight=1)
            self.master.columnconfigure(self.rows, weight=1)
            self.rows += 1
 
 
        # adds username entry widget and defines its properties
        self.username_box = Entry(self.master)
        self.username_box.insert(0, 'Enter Username')
        self.username_box.bind('<FocusIn>', self.clear_widget)
        self.username_box.bind('<FocusOut>', self.repopulate_defaults)
        self.username_box.grid(row=1, column=5, sticky='NS')
         
         
        # adds password entry widget and defines its properties
        self.password_box = Entry(self.master, show='*')
        self.password_box.insert(0, '     ')
        self.password_box.bind("<FocusIn>", self.clear_widget)
        self.password_box.bind('<FocusOut>', self.repopulate_defaults)
        self.password_box.bind('<Return>', self.login)
        self.password_box.grid(row=2, column=5, sticky='NS')
         
         
        # adds login button and defines its properties
        self.login_btn = Button(self.master, text='Login', command=self.login)
        self.login_btn.bind('<Return>', self.login)
        self.login_btn.grid(row=5, column=5, sticky='NESW')

        # adds login button and defines its properties
        self.quit_btn = Button(self.master, text='Quit', command=self.quit)
        self.quit_btn.bind('<Return>', self.quit)
        self.quit_btn.grid(row=6, column=5, sticky='NESW')

        self.login_text = StringVar()
        self.login_label = Label(self.master, textvariable=self.login_text)
        self.login_label.grid(row=7, column=5, sticky='NESW')
 
 
    def clear_widget(self, event):
     
        # will clear out any entry boxes defined below when the user shifts
        # focus to the widgets defined below
        if self.username_box == self.master.focus_get() and self.username_box.get() == 'Enter Username':
            self.username_box.delete(0, END)
        elif self.password_box == self.password_box.focus_get() and self.password_box.get() == '     ':
            self.password_box.delete(0, END)
     
    def repopulate_defaults(self, event):
     
        # will repopulate the default text previously inside the entry boxes defined below if
        # the user does not put anything in while focused and changes focus to another widget
        if self.username_box != self.master.focus_get() and self.username_box.get() == '':
            self.username_box.insert(0, 'Enter Username')
        elif self.password_box != self.master.focus_get() and self.password_box.get() == '':
            self.password_box.insert(0, '     ')
     
    def login(self, *event):
     
        # Able to be called from a key binding or a button click because of the '*event'
        # If I wanted I could also pass the username and password I got above to another 
        # function from here.

        if self.username_box.get() == 'admin' and self.password_box.get() == '1234':
            self.login_text.set("Credentials correct.")
            self.master.withdraw()
            root2 = Toplevel(self.master)
            smartRoomDashboard = Dashboard(root2)
        else:
            self.login_text.set("Unable to login with those credentials.")
     
       

    def quit(self, *event):
        self.master.destroy()

class Dashboard():
    

    def __init__(self, master):
        self.lt0 = False
        self.lt1 = False
        self.lt2 = False
        self.lt3 = False
        self.lt4 = False
        self.overridest = False


        self.master=master
        self.master.title('Smart Room Dashboard')
        self.master.geometry('400x250')

        self.rows = 0
        while self.rows < 10:
            self.master.rowconfigure(self.rows, weight=1)
            self.master.columnconfigure(self.rows, weight=1)
            self.rows += 1

        self.login_text = StringVar()
        self.login_label = Label(self.master, textvariable=self.login_text)
        self.login_label.grid(row=1, column=5, sticky='NESW')
        self.login_text.set("Dashboard") 


        self.override_btn = Button(self.master, text='Override', command=self.override)
        self.override_btn.grid(row=6, column=2, sticky='NESW')

        self.light0_btn = Button(self.master, text='Light 1', command=self.light_control(0) )
        self.light0_btn.grid(row=6, column=3, sticky='NESW')

        self.light1_btn = Button(self.master, text='Light 2', command=self.light_control(1))
        self.light1_btn.grid(row=6, column=4, sticky='NESW')

        self.light2_btn = Button(self.master, text='Light 3', command=self.light_control(2))
        self.light2_btn.grid(row=6, column=5, sticky='NESW')

        self.light3_btn = Button(self.master, text='Light 4', command=self.light_control(3))
        self.light3_btn.grid(row=6, column=6, sticky='NESW')

        self.lightAll_btn = Button(self.master, text='Light All', command=self.light_control(4))
        self.lightAll_btn.grid(row=6, column=6, sticky='NESW')



        # adds login button and defines its properties
        self.back_btn = Button(self.master, text='Back', command=self.back)
        self.back_btn.grid(row=6, column=5, sticky='NESW')

    def light_control(self, light):
        #light 1
        if light == 0 and self.lt0 == False:
            self.lt0 = True
            self.send_command("LT01")
        if light == 0 and self.lt0 == True:
            self.lt0 = False
            self.send_command("LT00")

        #light 2
        if light == 1 and self.lt1 == False:
            self.lt1 = True
            self.send_command("LT11")
        if light == 1 and self.lt1 == True:
            self.lt1 = False
            self.send_command("LT10")

        #light 3
        if light == 2 and self.lt2 == False:
            self.lt2 = True
            self.send_command("LT21")
        if light == 2 and self.lt2 == True:
            self.lt2 = False
            self.send_command("LT20")

        #light 4
        if light == 3 and self.lt3 == False:
            self.lt3 = True
            self.send_command("LT31")
        if light == 3 and self.lt3 == True:
            self.lt3 = False
            self.send_command("LT30")

        #light all
        if light == 4 and self.lt4 == False:
            self.lt4 = True
            self.send_command("LT41")
        if light == 4 and self.lt4 == True:
            self.lt4 = False
            self.send_command("LT40")

    def override(self):
        if (self.overridest):
            self.send_command("OV0")
            self.overridest=False
        else:
            self.send_command("OV1")
            self.overridest=True

    def send_command(self, command):
        ser.write(command)
        time.sleep(1)

    def back(self):
        self.master.withdraw()
        root2 = Toplevel(self.master)
        smartRoom = Login(root2)
         

def main():
    root = Tk();
    smartRoom=Login(root)
    root.mainloop()

if __name__ == '__main__':

    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    main()         
        