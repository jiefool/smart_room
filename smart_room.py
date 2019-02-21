#!/usr/bin/python

import Tkinter as tk ## notice capitalized T in Tkinter 
import time
import threading
import Queue
import mysql.connector
import serial
import datetime as dt
import tkMessageBox





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
        self.geometry('600x450')
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

        mycursor.execute("SELECT * FROM users WHERE username='"+ self.username_box.get() +"' AND password='"+ self.password_box.get() +"'")
        myresult = mycursor.fetchall()

        self.row = len(myresult)


        if self.row > 0:
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
        self.lt5 = False
        self.overridest = False
        self.adminpass = ""


        self.title('Smart Room Dashboard')
        self.geometry('600x450')

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


        self.light0_btn = tk.Button(self.labelframe1, text='AC 1', command=lambda:self.light_control(0) )
        self.light0_btn.grid(row=0, column=0, sticky='NESW')

        self.light1_btn = tk.Button(self.labelframe1, text='AC 2', command=lambda:self.light_control(1))
        self.light1_btn.grid(row=0, column=1, sticky='NESW')

        self.light2_btn = tk.Button(self.labelframe1, text='Light 1', command=lambda:self.light_control(2))
        self.light2_btn.grid(row=1, column=0, sticky='NESW')

        self.light3_btn = tk.Button(self.labelframe1, text='Light 2', command=lambda:self.light_control(3))
        self.light3_btn.grid(row=1, column=1, sticky='NESW')

        self.lightAll_btn = tk.Button(self.labelframe1, text='All Lights', command=lambda:self.light_control(4))
        self.lightAll_btn.grid(row=2, column=0, sticky='NESW')

        self.lightAll_btn = tk.Button(self.labelframe1, text='All Aircons', command=lambda:self.light_control(5))
        self.lightAll_btn.grid(row=2, column=1, sticky='NESW')



        self.labelframe2 = tk.LabelFrame(self, text="Thermal Sensor Data")
        self.labelframe2.grid(row=1, column=3, rowspan=2, columnspan=1, sticky='NESW')

        self.index = 0
        while self.index < 4:
            self.labelframe2.columnconfigure(self.index, weight=1)
            self.labelframe2.rowconfigure(self.index, weight=1)
            self.index = self.index + 1


        self.labelframe2b = tk.LabelFrame(self, text="Thermal Sensor 2 Data")
        self.labelframe2b.grid(row=1, column=4, rowspan=2, columnspan=1, sticky='NESW')

        self.index = 0
        while self.index < 4:
            self.labelframe2b.columnconfigure(self.index, weight=1)
            self.labelframe2b.rowconfigure(self.index, weight=1)
            self.index = self.index + 1

        # self.k = 1
        # for self.i in  range(4):
        #     for self.j in  range(4):
        #         tk.Button(self.labelframe2, text=str(self.k)).grid(row=int(self.i), column = int(self.j))
        #         self.j = self.j + 1
        #         self.k = self.k +1 
        #     self.i = self.i + 1



        self.labelframe3 = tk.LabelFrame(self, text="IRMS")
        self.labelframe3.grid(row=3, column=3, sticky='NESW')
        self.labelframe3.columnconfigure(0, weight=1)
        self.labelframe3.rowconfigure(0, weight=1)


        self.irms_label = tk.Label(self.labelframe3, text="123")
        self.irms_label.grid(row=0, column=0, sticky='NESW')
        


        self.labelframe4 = tk.LabelFrame(self, text="Power(Watt)")
        self.labelframe4.grid(row=3, column=4, sticky='NESW')
        self.labelframe4.columnconfigure(0, weight=1)
        self.labelframe4.rowconfigure(0, weight=1)

        self.power_label = tk.Label(self.labelframe4, text="123")
        self.power_label.grid(row=0, column=0, sticky='NESW')


        #input class schedule
        self.labelframe5 = tk.LabelFrame(self, text="Input Class Schedules")
        self.labelframe5.grid(row=4, column=1, rowspan=2, columnspan=2, sticky='NESW')
        self.labelframe5.columnconfigure(0, weight=1)
        self.labelframe5.rowconfigure(0, weight=1)


        self.DAY_OPTIONS = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ]

        self.sched_day = tk.StringVar(self)
        self.sched_day.set(self.DAY_OPTIONS[0])

        self.w_day = tk.OptionMenu(self.labelframe5, self.sched_day, *self.DAY_OPTIONS, command=self.day_selected)
        self.w_day.grid(row=0, column=0, sticky='NESW')

        self.Today= dt.datetime(2019,1,1,7)
        self.date_list = [self.Today + dt.timedelta(minutes=60*x) for x in range(0, 31)]
        self.TIME_OPTIONS = [x.strftime('%H:%M') for x in self.date_list]

        self.sched_time = tk.StringVar(self)
        self.sched_time.set(self.TIME_OPTIONS[0])

        self.w_time = tk.OptionMenu(self.labelframe5, self.sched_time, *self.TIME_OPTIONS, command=self.time_start_selected)
        self.w_time.grid(row=0, column=1, sticky='NESW')

        self.sched_time = tk.StringVar(self)
        self.sched_time.set(self.TIME_OPTIONS[0])

        self.w_time = tk.OptionMenu(self.labelframe5, self.sched_time, *self.TIME_OPTIONS, command=self.time_end_selected)
        self.w_time.grid(row=0, column=2, sticky='NESW')

        self.add_sched = tk.Button(self.labelframe5, text='Add Schedule', command=self.save_sched)
        self.add_sched.grid(row=1, column=0, columnspan=3, sticky='NESW')


        #class schedules
        self.labelframe6 = tk.LabelFrame(self, text="Class Schedules")
        self.labelframe6.grid(row=4, column=3, rowspan=2, columnspan=1, sticky='NESW')
        self.labelframe6.columnconfigure(0, weight=1)
        self.labelframe6.rowconfigure(0, weight=1)

        self.class_schedules()


        #temperature
        self.tempframe = tk.LabelFrame(self, text="Temperature")
        self.tempframe.grid(row=4, column=4, rowspan=1, columnspan=1, sticky='NESW')
        self.tempframe.columnconfigure(0, weight=1)
        self.tempframe.rowconfigure(0, weight=1)

        self.temp_label = tk.Label(self.tempframe, text="123")
        self.temp_label.grid(row=0, column=0, sticky='NESW')


        #password
        self.passframe = tk.LabelFrame(self, text="Set Password")
        self.passframe.grid(row=5, column=4, rowspan=1, columnspan=1, sticky='NESW')
        self.passframe.columnconfigure(0, weight=1)
        self.passframe.rowconfigure(0, weight=1)
        self.passframe.rowconfigure(1, weight=1)

        self.getpass()
        self.passentry = tk.Entry(self.passframe)
        self.passentry.insert(0, self.adminpass)
        self.passentry.grid(row=0, column=0, sticky='NESW')

        self.changepass_btn = tk.Button(self.passframe, text='Set Pass', command=self.setpass)
        self.changepass_btn.grid(row=1, column=0, columnspan=1, sticky='NESW')


        #back button
        self.back_btn = tk.Button(self, text='Back', command=self.back)
        self.back_btn.grid(row=6, column=1, columnspan=4, sticky='NESW')


        self.queue = Queue.Queue()
        thread = SerialThread(self.queue)
        thread.start()
        self.process_serial()

    def setpass(self):
        print "set pass"
        self.query = "UPDATE users SET password = %s WHERE username = %s "
        self.args = (self.passentry.get(), "admin")
        mycursor.execute(self.query, self.args)
        mydb.commit()

    def getpass(self):
        mycursor.execute("SELECT * FROM users")
        myresult = mycursor.fetchall()
        for item in myresult:
            self.adminpass = item[2]

    def save_sched(self):
        self.query = "INSERT INTO class_schedules(day,start_time, end_time) " \
                "VALUES(%s,%s,%s)"
        self.args = (self.day_sched, self.time_start_sched, self.time_end_sched)
        mycursor.execute(self.query, self.args)

        if mycursor.lastrowid:
            print('last insert id', mycursor.lastrowid)
        else:
            print('last insert id not found')
        
        mydb.commit()
        self.class_schedules()

    def class_schedules(self):
        mycursor.execute("SELECT * FROM class_schedules")
        myresult = mycursor.fetchall()

        for child in self.labelframe6.winfo_children():
            child.destroy()

        self.lrow = 0;
        for item in myresult:
            self.day_label = tk.Label(self.labelframe6, text=str(item[1]))
            self.day_label.grid(row=self.lrow, column=0, sticky='NESW')

            starttime = self.strfdelta(item[2], "{hours}:{minutes}")
            self.time_start_label = tk.Label(self.labelframe6, text=starttime)
            self.time_start_label.grid(row=self.lrow, column=1, sticky='NSW')

            endtime = self.strfdelta(item[3], "{hours}:{minutes}")
            self.time_end_label = tk.Label(self.labelframe6, text=endtime)
            self.time_end_label.grid(row=self.lrow, column=2, sticky='NSW')

            self.button = tk.Button(self.labelframe6, text="Remove", command=lambda x=item: self.remove_sched(x[0]))
            self.button.grid(row=self.lrow, column=3, sticky='NESW')
            self.lrow += 1;

        
    def strfdelta(self, tdelta, fmt):
        d = {"days": tdelta.days}
        d["hours"], rem = divmod(tdelta.seconds, 3600)
        d["minutes"], d["seconds"] = divmod(rem, 60)
        return fmt.format(**d)

    def remove_sched(self, sched_id): 
        print id
        result = tkMessageBox.askyesno("Delete","Would you like delete this schedule?")
        if(result):
            sql = "DELETE FROM class_schedules WHERE id=%i" % sched_id
            print sql
            mycursor.execute(sql)
            mydb.commit()
            self.class_schedules()

       



    def day_selected(self, selected_day):
        self.day_sched = selected_day


    def time_start_selected(self, selected_time):
        self.time_start_sched = selected_time

    def time_end_selected(self, selected_time):
        self.time_end_sched = selected_time
        

    def light_control(self, light):
        if  self.lt2 and self.lt3:
            self.lt4 = True
        else:
            self.lt4 = False

        if  self.lt0 and self.lt1:
            self.lt5 = True
        else:
            self.lt5 = False


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
            # self.lt0 = True
            # self.lt1 = True
            self.lt2 = True
            self.lt3 = True
            self.lt4 = True
            self.send_command("LT41")
        elif light == 4 and self.lt4 == True:
            # self.lt0 = False
            # self.lt1 = False
            self.lt2 = False
            self.lt3 = False
            self.lt4 = False
            self.send_command("LT40")

        #light aircon
        elif light == 5 and self.lt5 == False:
            self.lt0 = True
            self.lt1 = True
            # self.lt2 = True
            # self.lt3 = True
            # self.lt4 = True
            self.lt5 = True
            self.send_command("LT51")
        elif light == 5 and self.lt5 == True:
            self.lt0 = False
            self.lt1 = False
            # self.lt2 = False
            # self.lt3 = False
            # self.lt4 = False
            self.lt5 = False
            self.send_command("LT50")

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
                self.process_serial_data(self.serial_data)
                self.check_time()
                
               
                # print self.serial_data
            except Queue.Empty:
                pass
        self.after(100, self.process_serial)

    def check_time(self):
        mycursor.execute("SELECT * FROM class_schedules")
        myresult = mycursor.fetchall()
        current_dt = dt.datetime.now()
        c_year = current_dt.year
        c_month = current_dt.month
        c_day = current_dt.day
        c_day_name = current_dt.strftime("%a")

        print str(current_dt)
        print c_year
        print c_month
        print c_day
        print c_day_name

        for item in  myresult:
            dt_string_start = "%d/%d/%d %s" % (c_year, c_month, c_day, item[2])
            dt_string_end = "%d/%d/%d %s" % (c_year, c_month, c_day, item[3])

            print dt_string_start
            print dt_string_end

            if c_day_name == item[1]:
                dt_start = dt.datetime.strptime(dt_string_start, '%Y/%m/%d %H:%M:%S')
                dt_end = dt.datetime.strptime(dt_string_end, '%Y/%m/%d %H:%M:%S')
                if dt_start <= current_dt and current_dt <= dt_end: 
                # if dt_start <= current_dt: 
                    print "send override false"
                    self.send_command("OV0")
                else:
                    print "send override true"
                    self.send_command("OV1")


    def process_serial_data(self, serial_data):
        print serial_data
        if len(serial_data) > 0:
            self.data_split=serial_data.split("|")
            self.irms = self.data_split[0]
            self.power = self.data_split[1]
            self.thermal = self.data_split[2].split(",")
            self.thermal2 = self.data_split[3].split(",")
            self.temp = self.data_split[4]

            print self.irms
            print self.power
            print self.thermal
            print self.thermal2

            self.irms_label = tk.Label(self.labelframe3, text=str(self.irms))
            self.irms_label.grid(row=0, column=0, sticky='NESW')

            self.power_label = tk.Label(self.labelframe4, text=str(self.power))
            self.power_label.grid(row=0, column=0, sticky='NESW')

            self.temp_label = tk.Label(self.tempframe, text=str(self.temp))
            self.temp_label.grid(row=0, column=0, sticky='NESW')

            if len(self.thermal) == 16:
                for widget in self.labelframe2.winfo_children():
                    widget.destroy()

                self.k = 0
                for self.i in  range(4):
                    for self.j in  range(4):
                        # self.thermal_text = "*" if self.thermal[self.k] > 30 else str(self.thermal[self.k])
                        self.thermal_text = self.thermal[self.k]
                        tk.Button(self.labelframe2, text=self.thermal_text).grid(row=int(self.i), column = int(self.j))
                        self.j = self.j + 1
                        self.k = self.k + 1 
                    self.i = self.i + 1


            if len(self.thermal2) == 16:
                for widget in self.labelframe2b.winfo_children():
                    widget.destroy()

                self.k = 0
                for self.i in  range(4):
                    for self.j in  range(4):
                        # self.thermal_text = "*" if self.thermal[self.k] > 30 else str(self.thermal[self.k])
                        self.thermal_text = self.thermal2[self.k]
                        tk.Button(self.labelframe2b, text=self.thermal_text).grid(row=int(self.i), column = int(self.j))
                        self.j = self.j + 1
                        self.k = self.k + 1 
                    self.i = self.i + 1

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


    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd='[nJu*b`x/+_"F3dk',
      database="smart_room"
    )

    mycursor = mydb.cursor()
   


    main()         
        