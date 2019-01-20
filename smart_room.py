#!/usr/bin/python

import Tkinter as tk ## notice capitalized T in Tkinter 
import time
import threading
import Queue
import serial


class SerialThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            if ser.inWaiting():
                text = ser.readline()
                self.queue.put(text)


class Login(tk.Tk):

    def __init__(self):
        # defines a grid 50 x 50 cells in the main window
        tk.Tk.__init__(self)

        self.title('Smart Room Login')
        self.geometry('400x250')
        self.rows = 0
        while self.rows < 10:
            self.rowconfigure(self.rows, weight=1)
            self.columnconfigure(self.rows, weight=1)
            self.rows += 1
 
 
        # adds username entry widget and defines its properties
        self.username_box = tk.Entry(self)
        self.username_box.insert(0, 'Enter Username')
        self.username_box.bind('<FocusIn>', self.clear_widget)
        self.username_box.bind('<FocusOut>', self.repopulate_defaults)
        self.username_box.grid(row=1, column=5, sticky='NS')
         
         
        # adds password entry widget and defines its properties
        self.password_box = tk.Entry(self, show='*')
        self.password_box.insert(0, '     ')
        self.password_box.bind("<FocusIn>", self.clear_widget)
        self.password_box.bind('<FocusOut>', self.repopulate_defaults)
        self.password_box.bind('<Return>', self.login)
        self.password_box.grid(row=2, column=5, sticky='NS')
         
         
        # adds login button and defines its properties
        self.login_btn = tk.Button(self, text='Login', command=self.login)
        self.login_btn.bind('<Return>', self.login)
        self.login_btn.grid(row=5, column=5, sticky='NESW')

        # adds login button and defines its properties
        self.quit_btn = tk.Button(self, text='Quit', command=self.quit)
        self.quit_btn.bind('<Return>', self.quit)
        self.quit_btn.grid(row=6, column=5, sticky='NESW')

        self.login_text = tk.StringVar()
        self.login_label = tk.Label(self, textvariable=self.login_text)
        self.login_label.grid(row=7, column=5, sticky='NESW')
 
 
    def clear_widget(self, event):
     
        # will clear out any entry boxes defined below when the user shifts
        # focus to the widgets defined below
        if self.username_box == self.focus_get() and self.username_box.get() == 'Enter Username':
            self.username_box.delete(0, tk.END)
        elif self.password_box == self.password_box.focus_get() and self.password_box.get() == '     ':
            self.password_box.delete(0, tk.END)
     
    def repopulate_defaults(self, event):
     
        # will repopulate the default text previously inside the entry boxes defined below if
        # the user does not put anything in while focused and changes focus to another widget
        if self.username_box != self.focus_get() and self.username_box.get() == '':
            self.username_box.insert(0, 'Enter Username')
        elif self.password_box != self.focus_get() and self.password_box.get() == '':
            self.password_box.insert(0, '     ')
     
    def login(self, *event):
     
        # Able to be called from a key binding or a button click because of the '*event'
        # If I wanted I could also pass the username and password I got above to another 
        # function from here.

        if self.username_box.get() == 'admin' and self.password_box.get() == '1234':
            self.login_text.set("Credentials correct.")
            root2 = tk.Toplevel(self)
            smartRoomDashboard = Dashboard(root2)
            self.destroy()
        else:
            self.login_text.set("Unable to login with those credentials.")
     
       

    def quit(self, *event):
        self.destroy()

class Dashboard(tk.Tk):
    

    def __init__(self, master):
        tk.Tk.__init__(self)
        self.lt0 = False
        self.lt1 = False
        self.lt2 = False
        self.lt3 = False
        self.lt4 = False
        self.overridest = False


        self.title('Smart Room Dashboard')
        self.geometry('400x350')

        self.rows = 0
        while self.rows < 10:
            self.rowconfigure(self.rows, weight=1)
            self.columnconfigure(self.rows, weight=1)
            self.rows += 1


        self.labelframe0 = tk.LabelFrame(self, text="Override System")
        self.labelframe0.grid(row=1, column=1, columnspan=2, sticky='NESW')
        self.labelframe0.columnconfigure(0, weight=1)
        self.labelframe0.rowconfigure(0, weight=1)


        self.override_btn = tk.Button(self.labelframe0, text='Override', command=self.override)
        self.override_btn.grid(row=0, column=0, sticky='NESW')



        self.labelframe1 = tk.LabelFrame(self, text="Lights Control")
        self.labelframe1.grid(row=2, column=1, rowspan=2, columnspan=2, sticky='NESW')
        self.labelframe1.columnconfigure(0, weight=1)
        self.labelframe1.columnconfigure(1, weight=1)
        self.labelframe1.rowconfigure(0, weight=1)
        self.labelframe1.rowconfigure(1, weight=1)
        self.labelframe1.rowconfigure(2, weight=1)

        # self.login_label = Label(self.labelframe, text='Lights Control')
        # self.login_label.grid(row=2, column=0, sticky='NESW')


        self.light0_btn = tk.Button(self.labelframe1, text='Light 1', command=lambda:self.light_control(0) )
        self.light0_btn.grid(row=0, column=0, sticky='NESW')

        self.light1_btn = tk.Button(self.labelframe1, text='Light 2', command=lambda:self.light_control(1))
        self.light1_btn.grid(row=0, column=1, sticky='NESW')

        self.light2_btn = tk.Button(self.labelframe1, text='Light 3', command=lambda:self.light_control(2))
        self.light2_btn.grid(row=1, column=0, sticky='NESW')

        self.light3_btn = tk.Button(self.labelframe1, text='Light 4', command=lambda:self.light_control(3))
        self.light3_btn.grid(row=1, column=1, sticky='NESW')

        self.lightAll_btn = tk.Button(self.labelframe1, text='All Lights', command=lambda:self.light_control(4))
        self.lightAll_btn.grid(row=2, column=0, sticky='NESW')



        self.labelframe2 = tk.LabelFrame(self, text="Thermal Sensor Data")
        self.labelframe2.grid(row=1, column=3, rowspan=2, columnspan=2, sticky='NESW')

        self.index = 0
        while self.index < 4:
            self.labelframe2.columnconfigure(self.index, weight=1)
            self.labelframe2.rowconfigure(self.index, weight=1)
            self.index = self.index + 1

        self.k = 1
        for self.i in  range(4):
            for self.j in  range(4):
                tk.Button(self.labelframe2, text=str(self.k)).grid(row=int(self.i), column = int(self.j))
                self.j = self.j + 1
                self.k = self.k +1 
            self.i = self.i + 1



        self.labelframe3 = tk.LabelFrame(self, text="IRMS")
        self.labelframe3.grid(row=3, column=3, sticky='NESW')
        self.labelframe3.columnconfigure(0, weight=1)
        self.labelframe3.rowconfigure(0, weight=1)

        self.irms_text = tk.StringVar()
        self.irms_label = tk.Label(self.labelframe3, textvariable=self.irms_text)
        self.irms_label.grid(row=0, column=0, sticky='NESW')
        self.irms_text.set("123")


        self.labelframe4 = tk.LabelFrame(self, text="Power(Watt)")
        self.labelframe4.grid(row=3, column=4, sticky='NESW')
        self.labelframe4.columnconfigure(0, weight=1)
        self.labelframe4.rowconfigure(0, weight=1)

        self.power_text = tk.StringVar()
        self.power_label = tk.Label(self.labelframe4, textvariable=self.power_text)
        self.power_label.grid(row=0, column=0, sticky='NESW')
        self.power_text.set("123")




        # adds login button and defines its properties
        self.back_btn = tk.Button(self, text='Back', command=self.back)
        self.back_btn.grid(row=5, column=1, columnspan=4, sticky='NESW')


        self.queue = Queue.Queue()
        thread = SerialThread(self.queue)
        thread.start()
        self.process_serial()

    def light_control(self, light):
        if self.lt0 and self.lt1 and self.lt2 and self.lt3:
            self.lt4 = True
        else:
            self.lt4 = False


        #light 1
        if light == 0 and self.lt0 == False:
            self.lt0 = True
            self.send_command("LT01")
        elif light == 0 and self.lt0 == True:
            self.lt0 = False
            self.send_command("LT00")

        #light 2
        elif light == 1 and self.lt1 == False:
            self.lt1 = True
            self.send_command("LT11")
        elif light == 1 and self.lt1 == True:
            self.lt1 = False
            self.send_command("LT10")

        #light 3
        elif light == 2 and self.lt2 == False:
            self.lt2 = True
            self.send_command("LT21")
        elif light == 2 and self.lt2 == True:
            self.lt2 = False
            self.send_command("LT20")

        #light 4
        elif light == 3 and self.lt3 == False:
            self.lt3 = True
            self.send_command("LT31")
        elif light == 3 and self.lt3 == True:
            self.lt3 = False
            self.send_command("LT30")

        #light all
        elif light == 4 and self.lt4 == False:
            self.lt0 = True
            self.lt1 = True
            self.lt2 = True
            self.lt3 = True
            self.lt4 = True
            self.send_command("LT41")
        elif light == 4 and self.lt4 == True:
            self.lt0 = False
            self.lt1 = False
            self.lt2 = False
            self.lt3 = False
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
        smartRoom = Login()
        self.destroy()
         
    def process_serial(self):
        while self.queue.qsize():
            try:
                # self.text.delete(1.0, 'end')
                # self.text.insert('end', self.queue.get())
                self.serial_data = self.queue.get()

                # if not self.serial_data.strip():
                #     self.data_split = self.serial_data.split("|")
                #     self.irms_text.set(self.data_split[0])
                #     self.power_text.set(self.data_split[1])
                #     self.sensor_data = self.data_split[2].split(",")

                #     for widget in labelframe2.winfo_children():
                #         widget.destroy()


                #     self.k = 0
                #     for self.i in  range(4):
                #         for self.j in  range(4):
                #             tk.Button(self.labelframe2, text=str(self.sensor_data[self.k])).grid(row=int(self.i), column = int(self.j))
                #             self.j = self.j + 1
                #             self.k = self.k +1 
                #         self.i = self.i + 1


                #     print self.sensor_data
                print self.serial_data
            except Queue.Empty:
                pass
        self.after(100, self.process_serial)


def main():
    app = Login()
    app.mainloop()

    # root = Tk();
    # smartRoom=Login(root)
    # root.mainloop()

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
        