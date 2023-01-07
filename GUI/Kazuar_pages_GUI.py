import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText

import sqlite3
import os
import sys
import time

from subprocess import Popen, PIPE
import subprocess

from tkinter import messagebox
from function_GUI import terminal_for_sec_in
from Kazuar_databases_GUI import database_secin, database_sec_out, database_anti_tamper, database_automation_test
import xml.dom.minidom
from PIL import ImageTk, Image

user = ("Calibri", 10, 'bold')
FONT = ("Calibri", 19, 'bold')
LARGE_FONT = ("Calibri", 19, 'bold')
LARGE_FONT_button_title = ("Calibri", 50, 'bold')
LARGE_FONT_button_title2 = ("Calibri", 40, 'bold')
LARGE_FONT_button = ("Calibri", 22, 'bold')
LARGE_FONT_button1 = ("Calibri", 25, 'bold')
LARGE_FONT_button_next = ("Calibri", 15, 'bold')

with sqlite3.connect('Kazuar.db') as db:
    c = db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS sec_out_input_user_db (
                                                                Date integer,
                                                                User text,
                                                                SN_Kazuar_Board text,
                                                                SN_SOM_Board text,
                                                                Som_version text
                                                                )""")
c.execute( """CREATE TABLE IF NOT EXISTS sec_in_input_user_db (
                                                    Date integer,
                                                    User text,
                                                    SN text,
                                                    pass text,
                                                    description text
                                                    )""" )
c.execute("""CREATE TABLE IF NOT EXISTS AT_input_user_db (
                                                        Date integer,
                                                        User text,
                                                        SN_Kazuar_Board text,
                                                        AT_version integer,
                                                        Result text 
                                                        )""")
c.execute("""CREATE TABLE IF NOT EXISTS database_automation (
                                     Date integer,
                                     User text,
                                     EMS text,
                                     ODM_SN integer,
                                     Platform_Model text,
                                     Processor_GEN text,
                                     Processor integer,
                                     DDR_Size integer,
                                     Screen_Model text,
                                     Keyboard_Configuration text,
                                     Switching_Board text,
                                     Kazuar_Board text,
                                     SOM text,
                                     Kazuar_Laptop_Model text,
                                     Kazuar_Laptop_SN text,
                                     SecIn_Version integer,
                                     SecOut_Version integer,
                                     AT_Version integer
                                     )""")

db.commit()
db.close()


class secin:

    def __init__ (self, master=None, app_sec_in=None):


        self.string_to_search=None
        self.file_name=None
        self.label_countdown = None
        self.menu = None
        self.failure = None
        self.text_p = None
        self.stdErrValue = None
        self.stdOutValue = None
        self.communicateRes = None
        self.mainProcess = None
        self.run = None
        self.next_menu = None
        self.next = None
        self.next_log_f_stop_process = None
        self.off_stop_process = None
        self.log_f_stop_process = None
        self.title_stop_process = None
        self.buttonClicked = None
        self.answer_connected = None
        self.text = None
        self.text_options = None
        self.command = None
        self.popen = None
        self.running = None
        self.execute_r = None
        self.label = None
        self.text = None
        self.stopper = None
        self.database_secin = None
        self.frame = None
        self.off_2 = None
        self.last_line = None
        self.title2 = None
        self.log_f_2 = None
        self.next_log_f_2 = None
        self.off = None
        self.title = None
        self.log_f = None
        self.next_log_f = None
        self.title1 = None
        self.log_f_1 = None
        self.next_log_f_1 = None
        self.c = None
        self.conn = None
        self.c = None
        self.root_sec_in_database_query = None
        self.button = None
        self.img = None
        ##########################################
        # read and parse XML document
        self.DOMTree = xml.dom.minidom.parse("GUI_Config_Pages_File.xml")

        # create attribute for XML document
        self.xmlDocument = self.DOMTree.documentElement
        ##########################################


        self.user_enter = StringVar()
        self.board_sn = StringVar()
        self.board_sn.set(self.get_element_value(self.xmlDocument,"boardsn"))

        self.reason = StringVar()
        self.reason.set(self.get_element_value(self.xmlDocument,"SelectReason"))

        self.countdown = StringVar()
        self.countdown.set(self.get_element_value(self.xmlDocument,"StartTime"))

        self.si_version = StringVar()
        self.si_version.set(self.get_element_value(self.xmlDocument,"siVersion"))

        self.FileSi = StringVar()
        self.FileSi = self.get_element_value(self.xmlDocument,"ProcessFileSi")

        self.WorkingDirectory = StringVar()
        self.WorkingDirectory = self.get_element_value(self.xmlDocument,"ProcessTerminalSiDirectory")

        self.FileFailureSi = StringVar()
        self.FileFailureSi = self.get_element_value(self.xmlDocument,"FileToSaveDebag")

        self.PcPassword = StringVar()
        self.PcPassword = self.get_element_value(self.xmlDocument,"TesterPcPassword")

        self.FileForResults = StringVar()
        self.FileForResults = self.get_element_value(self.xmlDocument,"FileForResults")

        self.FailuresReasonsFile = StringVar()
        self.FailuresReasonsFile = self.get_element_value(self.xmlDocument,"FailuresReasonsFile")


        self.master = master
        # self.self = self

        self.app_sec_in = app_sec_in
        self.widget_secin()
        self.conn = sqlite3.connect('Kazuar.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user')
        self.user_enter = self.c.fetchall()[0][0]

        # get value of an XML element with specified name
    def get_element_value (self, parent,name):
        if parent.childNodes:
            for node in parent.childNodes:
                if node.nodeType == node.ELEMENT_NODE:
                    if node.tagName == name:
                        if node.hasChildNodes:
                            child = node.firstChild
                            return child.nodeValue
        return None

    # set value of an XML element with specified name
    def set_element_value (self, parent,name,value):
        if parent.childNodes:
            for node in parent.childNodes:
                if node.nodeType == node.ELEMENT_NODE:
                    if node.tagName == name:
                        if node.hasChildNodes:
                            child = node.firstChild
                            child.nodeValue = value
        return None

    def widget_secin(self):
        self.frame = tk.Frame( self.master, bg='light sky blue' )
        self.title = Frame(self.frame, padx=10, pady=50, bg="light sky blue")
        self.log_f = Frame(self.frame, padx=10, pady=50, bg="light sky blue")
        self.off = Frame(self.frame, padx=200, pady=60, bg="light sky blue")
        self.next_log_f = Frame(self.frame, padx=300, pady=70, bg="light sky blue",
                                highlightbackground='blue', highlightthickness=20, highlightcolor='blue')
        Label(self.title, text='Secure Input', font=LARGE_FONT_button_title, bg="light sky blue",
              fg="black").grid(row=0, column=0, padx=25, sticky=N)
        Label(self.log_f, text='Kazuar Board\nSerial Number', font=LARGE_FONT_button, bg="light sky blue",
              fg="black").grid(row=0, column=0, pady=25, padx=40, sticky=N)

        Entry(self.log_f, textvariable=self.board_sn, bd=10, font=LARGE_FONT_button).grid(row=1, column=0, pady=10  )

        Label(self.off, text="Secure Input\nVersion", font=LARGE_FONT_button,
              bg="light sky blue").grid(row=4, column=0, pady=25, padx=40, sticky=N)
        options = ("0.0.18".split())
        menu = OptionMenu(self.off, self.si_version, *options)
        menu.config(font=LARGE_FONT_button, indicatoron=OFF)
        menu.grid(row=5, column=0, pady=20, padx=40, sticky=N)

        Button(self.next_log_f, text="Start\nBurning", bg="green", fg="white", font=FONT,
               command=self.check_sn_board_input, bd=12).grid(row=2, column=0, padx=200, ipadx=60)
        Button(self.next_log_f, text="Menu", bg="red", fg="white", font=FONT,
               command=self.go_back, bd=12).grid(row=2, column=2, padx=450, ipadx=100, ipady=30)
        self.title.pack()
        self.log_f.pack()
        self.off.pack()
        self.next_log_f.pack(ipadx=400, fill=X)
        ###########################################################################################################
        self.title1 = Frame(self.frame, padx=10, pady=1, bg="light sky blue")
        self.log_f_1 = Frame(self.frame, padx=10, pady=20, bg="light sky blue")
        self.next_log_f_1 = Frame(self.frame, padx=350, pady=30, bg="light sky blue",
                                  highlightbackground='blue', highlightthickness=20, highlightcolor='blue')

        left_label = Label(self.title1, bg="light sky blue", text="Secure Input", font=LARGE_FONT_button_title)
        left_label.pack(fill="x")

        Label(self.log_f_1, text="1. Place Kazuar Board into the JIG and tight\n"
                                 "2. Connect the Kazuar board to connector type C\n"
                                 "3. Connect the connector type C to tester PC",
              font=LARGE_FONT, bg="light sky blue").pack()
        Label(self.log_f_1, text="***** Check if red LED on Kazuar board bottom is ON *****",
              font=LARGE_FONT, bg="light sky blue", fg='red').pack()
        self.img = ImageTk.PhotoImage(Image.open("/home/tester/PycharmProjects/GUI_production_kazuar/image"
                                                 "/secin1.png"))
        Label(self.log_f_1, image=self.img, borderwidth=0, bg='light sky blue', relief="flat").pack(pady=15)
        Button(self.next_log_f_1, text="Start\nBurning", bg="green", fg="white", font=FONT,
               command=self.page_to_start_burning, bd=12).grid(row=2, column=0, padx=100, ipadx=50, pady=20)
        Button(self.next_log_f_1, text="Back", bg="blue", fg="white", font=FONT,
               command=self.back_to_main, bd=12).grid(row=2, column=1, padx=100, ipadx=100, ipady=30, pady=20)
        Button(self.next_log_f_1, text="Menu", bg="red", fg="white", font=FONT,
               command=self.go_back, bd=12).grid(row=2, column=2, padx=100, ipadx=100, ipady=30, pady=20)
        ###############################################################################################
        self.title2 = Frame(self.frame, padx=10, pady=1, bg="light sky blue")
        self.log_f_2 = Frame(self.frame, padx=150, bg="light sky blue")
        self.off_2 = Frame(self.frame, padx=10, pady=90, bg="light sky blue")
        self.next_log_f_2 = Frame(self.frame, padx=10, bg="light sky blue",
                                  highlightbackground='blue', highlightthickness=20, highlightcolor='blue')
        left_label = Label(self.title2, bg="light sky blue", text="Secure Input", font=LARGE_FONT_button_title)
        left_label.pack(fill="x", pady=10)
        Label(self.off_2, bg="light sky blue", font=LARGE_FONT_button_title).grid(pady=60)
        Label(self.log_f_2, text="****************************", font=LARGE_FONT_button1,
              bg='light sky blue').pack(padx=500)
        Label(self.log_f_2, textvariable=self.board_sn, font=LARGE_FONT_button1, bg='light sky blue').pack(padx=500)

        self.label_countdown = Label(self.log_f_2,textvariable=self.countdown,font=user,
                                     bg='light sky blue')
        self.label_countdown.pack(padx=500, pady=10)

        Label(self.log_f_2, text="****************************", font=LARGE_FONT_button1,
              bg='light sky blue').pack(padx=500, pady=10)

        self.text = Button(self.log_f_2, text='Press\nStart Process', bg='light sky blue',
                           font=LARGE_FONT_button1, relief=FLAT)
        self.text.pack(ipadx=10)

        Label(self.off_2, text='', font=FONT, bg="light sky blue",
              fg="black").grid(row=2, column=0, padx=25, sticky=W)
        self.execute_r = Button(self.next_log_f_2, text="Start\nProcess", font=FONT, fg='white',
                                bg='green', command=self.check_sec_in_connect, bd=10)
        self.execute_r.grid(row=2, column=0, padx=50, ipadx=60)
        self.label = Label(self.next_log_f_2, text="", font=LARGE_FONT_button1, bg='light sky blue', fg='black',
                           relief=FLAT)
        self.label.grid(row=2, column=1, padx=130, ipadx=60)

        self.stopper = Button(self.next_log_f_2, text="Stop\nProcess", font=FONT, fg='white',
                              bg='red', command=self.stop_process, bd=10, state=DISABLED)
        self.stopper.grid(row=2, column=2, padx=130, ipadx=60)

        self.menu = Button(self.next_log_f_2, text="Menu", font=FONT, fg='white',
                              bg='red', command=self.stop_process, bd=10)
        self.menu.grid(row=2, column=3, padx=300, ipadx=100, ipady=30)
        #################################################################################################
        self.title_stop_process = Frame(self.frame, padx=10, pady=1, bg="light sky blue")
        self.log_f_stop_process  = Frame(self.frame, padx=10, pady=100   , bg="light sky blue")
        self.off_stop_process  = Frame(self.frame, padx=10, pady=150, bg="light sky blue")
        self.next_log_f_stop_process  = Frame(self.frame, padx=10, pady=30, bg="light sky blue",
                                  highlightbackground='blue', highlightthickness=20, highlightcolor='blue')
        left_label = Label(self.title_stop_process , bg="light sky blue", text="Secure Input", font=LARGE_FONT_button_title)
        left_label.pack(fill="x")
        Label(self.log_f_stop_process,text='Process uncompleted..  ',bg="light sky blue",
              font=LARGE_FONT_button1).grid(pady=30)

        Label(self.log_f_stop_process, text='Stop Process\nReason  ', bg="light sky blue",
              font=LARGE_FONT_button).grid(pady=20)


        options_stop_process = ("Error in process terminal", "Wrong Serial Number", "USB Cable disconnected to PC",
                                "USB Cable disconnected to K.B", "USB Cable damaged", "Kazuar Board damaged".split())
        menu_stop_process = OptionMenu(self.log_f_stop_process, self.reason, *options_stop_process)
        menu_stop_process.config(font=LARGE_FONT)
        menu_stop_process.grid(pady=20)

        self.next = Button(self.next_log_f_stop_process, text="Next Bord", bg="blue", fg="white", font=FONT,
               command=self.check_stop_process, bd=12)
        self.next.grid(row=2, column=0, padx=400, ipadx=50, ipady=15)
        Label(self.next_log_f_stop_process, text="", bg="light sky blue"
              ).grid(row=2, column=1, padx=100, ipadx=100, ipady=15)
        self.next_menu = Button(self.next_log_f_stop_process, text="Menu", bg="red", fg="white", font=FONT,
               command=self.check_stop_process, bd=12)
        self.next_menu.grid(row=2, column=2, padx=100, ipadx=100, ipady=15)
        ##############################################################################################

    def update (self, seconds):
        global after
        if seconds >= 0:
            self.countdown.set(self.seconds_to_time(seconds))
            after = self.label_countdown.after(500,lambda: self.update(seconds - 1))

            if self.countdown.get() == '00:00:00':
                self.stop_process()
        else:
            self.label_countdown.after_cancel(after)

    def seconds_to_time (self, seconds):
        hours = seconds // 3600
        seconds -= hours * 3600
        minutes = seconds // 60
        seconds -= minutes * 60
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    def kill_process(self):
        import os, signal
        def process():

            name = "server"
            try:
                # iterating through each instance of the process
                for line in os.popen("ps ax | grep " + name):
                    fields = line.split()
                    # extracting Process ID from the output
                    pid = fields[0]
                    # terminating process
                    os.kill(int(pid), signal.SIGKILL)
                print("Process Successfully terminated")
            except:
                print('hi')

        process()

    def check_stop_process(self):
        if self.reason.get() == 'Select':
            messagebox.showerror('error', 'Mast to choice Stopping Process reason')
        elif self.reason.get() == 'Error in process terminal':
            error_in_terminal = messagebox.showerror('error', 'Reconnect the USB cable\nand flash it again ')
            if error_in_terminal == 'ok':
                self.back_to_main()
            #######

        else:
            self.result_fail()

    def stop_process(self):
        self.kill_process()
        self.title2.pack_forget()
        self.log_f_2.pack_forget()
        self.off_2.pack_forget()
        self.next_log_f_2.pack_forget()
        self.title_stop_process.pack()
        self.log_f_stop_process.pack(pady=100)
        self.off_stop_process.pack(pady=100)
        self.next_log_f_stop_process.pack(ipadx=1000)

    def check_sec_in_connect (self):
        msg_sec_in = tk.messagebox.askquestion('cmd', 'Are you sure the connector type C connected? ')
        if msg_sec_in == 'yes':
            import os
            x = os.system("lsusb | grep Microchip")
            if x == 0:
                print("connected")
                self.update(seconds = int(self.get_element_value(self.xmlDocument ,"ProcessTimeSeconds")))
                # def change_process_page_characters():
                self.execute_r.config(state = DISABLED)
                self.label.config(text = 'Connected to the process..\nDo not touch the system!!')
                self.label.config(bg = 'red' ,fg = 'white')
                self.text.config(text = 'In-Process')
                self.text.config(bg = 'green' ,fg = 'white')

                self.menu.grid_forget()
                self.stopper.config(state = NORMAL)

                """cmd displayed and run commend of flashing SecIn img """
                '''import working-directory, password, img file + file for logs from GUI_Config.xml'''
                import subprocess
                import os
                cmd=f"gnome-terminal --geometry=100x16+185+240  --working-directory={self.WorkingDirectory} -- bash -c \"echo " \
                    f"{self.PcPassword} | sudo -S ./{self.FileSi} |& tee {self.FileFailureSi}; exec bash\" "

                self.text_p=subprocess.Popen(args = [cmd] ,shell = True ,stdout = subprocess.PIPE ,
                                             preexec_fn = os.setsid ,stderr = subprocess.PIPE ,
                                             universal_newlines = True ,
                                             bufsize = 1 ,text = True ,encoding = 'utf-8')

                print('Working')
                self.text.config(text = 'Successful',bd = 10,bg = 'green',font = LARGE_FONT_button_title2,
                                 relief = RAISED)
                self.text.config(command = self.result_pass)
                self.update(seconds = int(self.get_element_value(self.xmlDocument,"ProcessTimeSeconds")))

                print('process completed!')

        # if self.text_p is None:
                # import schedule
                # def red_last_line ():
                #     readfile=open('/home/tester/SecIn/secin.txt' ,'r')
                #     line_list=readfile.readlines()
                #     readfile.close()
                #     print(line_list)
                #     print('last line: ' ,line_list[len(line_list) - 1])
                #
                #     if line_list[len(line_list) - 1] == 'Successful':
                #         self.text.config(text='Successful' ,bd=10 ,bg='green' ,font=LARGE_FONT_button_title2 ,
                #                          relief=RAISED)
                #         self.text.config(command=self.result_pass)
                #         self.update(seconds=int(self.get_element_value(self.xmlDocument ,"ProcessTimeSeconds")))
                #
                #         print('process completed!')
                #     else:
                #         self.text.config(text='In-Process' ,bd=10 ,bg='green' ,font=LARGE_FONT_button_title2 ,
                #                          relief=RAISED)
                #         print('In process')
                #
                # schedule.every(1).second.do(red_last_line)
                # while True:
                #     schedule.run_pending()

                # stdout_as_str=self.text_p.stdout.decode("utf-8")
                # poll=self.text_p.poll()
                # if poll is None:
                #     time.sleep(2)

                # self.text_p.subprocess is alive
                #     count=0
                #     print("Using readlines()")
                #
                #     with open("/home/tester/SecIn/secin.txt") as fp:
                #         lines_of_file=fp.readlines()
                #         print(f"Lines: {len(lines_of_file)}")
                #
                #         for line in lines_of_file:
                #             count+=1
                #             print("Line{}: {}".format(count ,line.strip()))
                #
                #             # if line.strip() == 'Secure Input eMMC is not yet exposed to us':
                #             #     print('wait..')
                #
                #             if line.strip() == 'Successful':
                #                 self.text.config(text='Successful')
                #                 self.text.config(command=self.result_pass)
                #                 self.update(seconds=int(self.get_element_value(self.xmlDocument ,"ProcessTimeSeconds")))
                #
                #                 print('process completed!')
                #
                #             else:
                #                 pass
                #                 self.text.config(text='In-Process' ,bd=10 ,bg='green' ,font=LARGE_FONT_button_title2 ,
                #                                  relief=RAISED)
                #                 print('In process')



            else:
                print("disconnected")
                ret = messagebox.showerror('error','cable disconnected\nor not approved!\nplease check it ')
                if ret == 'ok':
                    pass


                # if self.text_p:
                #     time.sleep(1)
                #     self.text.config(text='Successful', bd=10, bg='green', font=LARGE_FONT_button_title2, relief=RAISED)
                #     self.text.config(command=self.result_pass)
                #     print('Working1')
                #     # while subprocess.CalledProcessError is None:
                #     #     # ---- read a line from the process output ----
                #     #     msg = self.text_p.stdout.readline().strip()
                #     #     if not msg:
                #     #         self.text.config(text='Error!',state=DISABLED)
                #     #         terminal_close = messagebox.showerror('error','Terminal, closed!')
                #     #         if terminal_close == 'ok':
                #     #             self.stop_process()
                #     #         print('not Working1')
                #             # continue
                #             # print(msg)
                # else:
                #     print('not working')
                #     self.text.config(text='Error!',state=DISABLED)
                #     terminal_close = messagebox.showerror('error','Terminal, closed!')
                #     if terminal_close == 'ok':
                #         self.stop_process()




    def page_to_start_burning (self):
        self.title1.pack_forget()
        self.log_f_1.pack_forget()
        self.next_log_f_1.pack_forget()

        self.title2.pack()
        self.log_f_2.pack()
        self.off_2.pack(pady=10)
        self.next_log_f_2.pack(ipadx=1000, expand=True)
    def start_page_secin (self):
        self.frame.pack()

    def go_back (self):
        self.title1.pack_forget()
        self.log_f_1.pack_forget()
        self.next_log_f_1.pack_forget()
        self.title2.pack_forget()
        self.log_f_2.pack_forget()
        self.off_2.pack_forget()
        self.next_log_f_2.pack_forget()
        self.frame.pack_forget()
        self.app_sec_in.menu_page()

    def result_pass (self):
        with open(self.FileForResults, 'rb') as f:
            try:  # catch OSError in case of a one line file
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            self.last_line = f.readline().decode()
            print(self.last_line)
        # Create a database or connect to one
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        # Insert Into Table
        self.c.execute("INSERT INTO sec_in_input_user_db VALUES (:Date, :User, :SN, :pass, :description)",
                       {
                           'Date': time.strftime("%D %H:%M:%S"),
                           'User': self.user_enter,
                           'SN': self.board_sn.get().upper(),
                           'pass': 'YES',
                           'description': 'Process Completed!' + "\nVersion " + self.si_version.get()
                       })

        self.conn.commit()
        self.conn.close()
        print('pass')
        self.back_to_main()

    def result_fail (self):
        # self.kill_terminal_process()
        with open(self.FileForResults, 'rb') as f:
            try:  # catch OSError in case of a one line file
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            self.last_line = f.readline().decode()
            print(self.last_line)
        # Create a database or connect to one
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        # Insert Into Table
        self.c.execute("INSERT INTO sec_in_input_user_db VALUES (:Date, :User, :SN, :pass, :description)",
                       {
                           'Date': time.strftime("%D %H:%M:%S"),
                           'User': self.user_enter,
                           'SN': self.board_sn.get().upper(),
                           'pass': 'NO',
                           'description': self.last_line + "\nVersion " + self.si_version.get()
                       })

        self.conn.commit()
        self.conn.close()
        print('fail process')
        with open(self.FailuresReasonsFile, "a") as file_object:
            # Append board serial number + stop reason to the file
            file_object.write(f'\n{self.board_sn.get()} stop process due to + {self.reason.get()}'
                              f' + {time.strftime("%D %H:%M:%S")} + reason: {self.last_line} \n')
            print(file_object)
        self.back_to_main()

    def back_to_main (self):
        self.title_stop_process.pack_forget()
        self.log_f_stop_process.pack_forget()
        self.off_stop_process.pack_forget()
        self.next_log_f_stop_process.pack_forget()
        self.title1.pack_forget()
        self.log_f_1.pack_forget()
        self.next_log_f_1.pack_forget()
        self.title2.pack_forget()
        self.log_f_2.pack_forget()
        self.next_log_f_2.pack_forget()
        self.off_2.pack_forget()

        self.title.pack()
        self.log_f.pack()
        self.board_sn.set(self.get_element_value(self.xmlDocument,"boardsn"))
        self.off.pack()
        self.next_log_f.pack(ipadx=400, fill=X)

    def connection_board (self):
        self.log_f.pack_forget()
        self.title.pack_forget()
        self.off.pack_forget()
        self.next_log_f.pack_forget()
        #####
        self.title1.pack()
        self.log_f_1.pack()
        self.next_log_f_1.pack(ipadx=400, fill=X)


    def check_sn_board_input (self):
        self.board_sn.set(self.board_sn.get().upper())
        if self.board_sn.get() == "":
            messagebox.showerror('error!', 'Missing board S/N')
        else:
            self.check_number_latter_and_digit()

    def check_number_latter_and_digit(self):
        digit = letter = space = 0
        for ch in self.board_sn.get():
            if ch.isdigit():
                digit = digit + 1
            elif ch.isalpha():
                letter = letter + 1
            elif ch == '-':
                space = space + 1
            else:
                pass
        print("Letters:", letter)
        print("Digits:", digit)
        print("Characters:", space)
        print("letter + digit + space:" , letter + digit + space)
        if 20 <= letter + digit + space < 21:
            print('enough numbers')
            self.check_input_in_db()
        else:
            print('NOT enough numbers')
            messagebox.showerror('Error', 'Not enough numbers\nIn serial number\nPlease check.. ')

    def check_input_in_db (self):
        with sqlite3.connect('Kazuar_tester_PC.db') as self.db:
            self.c = self.db.cursor()

        find_user = 'SELECT SN FROM sec_in_input_user_db WHERE SN = ?'
        self.c.execute(find_user, [(self.board_sn.get())])

        if self.c.fetchall():
            messagebox.showerror('Error!', f'{self.board_sn.get()}\nAlready bernt!\nTry a different one.')
        else:
            self.connection_board()

class anti_tamper:
    def __init__(self, master=None, app_anti_tamper=None):

        self.name = None
        self.c2 = None
        self.next_menu_at = None
        self.next_at = None
        self.next_log_f_stop_process_at = None
        self.off_stop_process_at = None
        self.log_f_stop_process_at = None
        self.title_stop_process_at = None
        self.next_log_f_1_at = None
        self.log_f_1_at = None
        self.title1_at = None
        self.frame_anti_tamper = None
        self.text_result = None
        self.root_anti_tamper_database_query = None
        self.off_1 = None
        self.render2 = None
        self.load2 = None
        self.render = None
        self.load = None
        self.c1 = None
        self.off_2 = None
        self.last_line = None
        self.title2 = None
        self.log_f_2 = None
        self.next_log_f_2 = None
        self.off = None
        self.title = None
        self.log_f = None
        self.next_log_f = None
        self.title1 = None
        self.log_f_1 = None
        self.next_log_f_1 = None
        self.c = None
        self.conn = None
        self.c = None
        self.root_sec_in_database_query = None
        self.button = None
        self.img = None
        ##########################################
        # read and parse XML document
        self.DOMTree = xml.dom.minidom.parse("GUI_Config_Pages_File.xml")

        # create attribute for XML document
        self.xmlDocument = self.DOMTree.documentElement
        ##########################################
        self.master = master
        # self.board_sn_AT = StringVar()
        self.board_sn_AT = StringVar()
        self.board_sn_AT.set(self.getelementValue(self.xmlDocument,"boardsnAT"))
        self.board_sn = StringVar()
        self.reason_at = StringVar()
        self.reason_at.set(self.getelementValue(self.xmlDocument,"SelectReason"))

        self.AT_version = StringVar()
        self.AT_version.set(self.getelementValue(self.xmlDocument,"AntiTamperVersion"))

        self.PcPassword = StringVar()
        self.PcPassword = self.getelementValue(self.xmlDocument,"TesterPcPassword")

        self.WorkingDirectory = StringVar()
        self.WorkingDirectory = self.getelementValue(self.xmlDocument,"ProcessTerminalATDirectory")

        self.FileAT = StringVar()
        self.FileAT = self.getelementValue(self.xmlDocument,"ProcessFileSAT")

        self.FileForResultsAT = StringVar()
        self.FileForResultsAT = self.getelementValue(self.xmlDocument,"FileForResults")

        self.AntiTamperStatusWorkingDirectory = StringVar()
        self.AntiTamperStatusWorkingDirectory = self.getelementValue(self.xmlDocument,"AntiTamperStatusWorkingDirectory")

        self.FileForResultsAT = StringVar()
        self.FileForResultsAT = self.getelementValue(self.xmlDocument,"FileForResults")

        self.FileToAntiTamper = StringVar()
        self.FileToAntiTamper = self.getelementValue(self.xmlDocument,"FileToAntiTamper")

        self.FileToAntiTamper = StringVar()
        self.FileToAntiTamper = self.getelementValue(self.xmlDocument,"FileToAntiTamper")

        self.FailuresReasonsFile = StringVar()
        self.FailuresReasonsFile = self.getelementValue(self.xmlDocument,"FailuresReasonsFile")

        ##################################################################################################



        self.widget_anti_tamper()
        self.app_anti_tamper = app_anti_tamper
        self.conn = sqlite3.connect('Kazuar.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user')
        self.user_enter = self.c.fetchall()[0][0]

    # get value of an XML element with specified name
    def getelementValue (self, parent,name):
        if parent.childNodes:
            for node in parent.childNodes:
                if node.nodeType == node.ELEMENT_NODE:
                    if node.tagName == name:
                        if node.hasChildNodes:
                            child = node.firstChild
                            return child.nodeValue
        return None
    def widget_anti_tamper(self):
        self.frame_anti_tamper = tk.Frame(self.master, bg='light sky blue')
        self.title = Frame(self.frame_anti_tamper, padx=10, pady=50, bg="light sky blue")
        self.log_f = Frame(self.frame_anti_tamper, padx=10, pady=80, bg="light sky blue")
        self.next_log_f = Frame(self.frame_anti_tamper, padx=300, pady=80, bg="light sky blue",
                                highlightbackground='blue', highlightthickness=20, highlightcolor='blue', )
        Label(self.title, text='Burning Anti-Tamper', font=LARGE_FONT_button_title, bg="light sky blue",
              fg="black").grid(row=0, column=0, pady=5, padx=25, sticky=N)
        Label(self.log_f, text='Kazuar Board\nSerial Number', font=LARGE_FONT_button, bg="light sky blue",
              fg="black").grid(row=0, column=0, pady=20, padx=40, sticky=N)

        Entry(self.log_f, textvariable=self.board_sn_AT, bd=10,
              font=LARGE_FONT_button).grid(row=1, column=0, pady=10)
        # self.board_sn_AT.set('NS-KB31-R01-XXXXXXXX')
        Label(self.log_f, font=LARGE_FONT_button1, bg="light sky blue",
              relief="flat").grid(row=3, column=0, pady=5, padx=40, sticky=N)

        Label(self.log_f, text="AT Version", font=LARGE_FONT_button,
              bg="light sky blue").grid(row=4, column=0, pady=20, padx=40, sticky=N)
        options = ("0.0.8".split())
        menu = OptionMenu(self.log_f, self.AT_version, *options)
        menu.config(font=LARGE_FONT_button, indicatoron=OFF)
        # self.AT_version.set("0.0.8")
        menu.grid(row=5, column=0, pady=10, padx=40, sticky=N)

        Button(self.next_log_f, text="Start\nBurning", bg="green", fg="white", font=FONT,
               command=self.check_at_input, bd=12).grid(row=2, column=0, padx=200, ipadx=60, pady=20)
        Button(self.next_log_f, text="Menu", bg="red", fg="white", font=FONT,
               command=self.go_back_anti_tamper, bd=12).grid(row=2, column=2, padx=450, ipadx=100, ipady=30, pady=20)
        self.title.pack()
        self.log_f.pack()
        self.next_log_f.pack(ipadx=400, fill=X)
        ###########################################################################################################
        self.title1_at = Frame(self.frame_anti_tamper, padx=10, pady=1, bg="light sky blue")
        self.log_f_1_at = Frame(self.frame_anti_tamper, padx=10, pady=20, bg="light sky blue")
        self.next_log_f_1_at = Frame(self.frame_anti_tamper, padx=10, pady=30, bg="light sky blue",
                                  highlightbackground='blue', highlightthickness=20, highlightcolor='blue')

        left_label = Label(self.title1_at, bg="light sky blue", text="Anti-Tamper", font=LARGE_FONT_button_title)
        left_label.pack(fill="x")
        Label(self.log_f_1_at, text="1. Place Kazuar Board into the JIG and tight\n"
                                 "2. Connect J-Tag and type C connectors as the left image\n"
                                 "3. Connect J-Tag and type C cable to tester PC",
              font=LARGE_FONT, bg="light sky blue").pack()

        self.load = ImageTk.PhotoImage(Image.open("/home/tester/PycharmProjects/GUI_production_kazuar/image"
                               "/anti_tamper1.PNG"))
        Label(self.log_f_1_at, image=self.load).pack(pady=50, side=LEFT, padx=250)

        self.load2 = ImageTk.PhotoImage(Image.open("/home/tester/PycharmProjects/GUI_production_kazuar/image"
                                "/anti_tamper2.PNG"))
        Label(self.log_f_1_at, image=self.load2).pack(pady=50, side=LEFT, padx=50)

        Button(self.next_log_f_1_at, text="Start\nBurning", bg="green", fg="white", font=FONT,
               command=self.check_anti_tamper_connect, bd=12).grid(row=2, column=0, padx=100, ipadx=50, pady=20)
        Button(self.next_log_f_1_at, text="Back", bg="blue", fg="white", font=FONT,
               command=self.back_to_main_anti_tamper, bd=12).grid(row=2, column=1, padx=100,
                                                                  ipadx=100, ipady=30, pady=20)
        Button(self.next_log_f_1_at, text="Burning\nStatus", bg="green", fg="white", font=FONT,
               command=self.check_anti_tamper_status, bd=12).grid(row=2, column=2, ipadx=100, padx=100, pady=20)
        Button(self.next_log_f_1_at, text="Menu", bg="red", fg="white", font=FONT,
               command=self.go_back_anti_tamper, bd=12).grid(row=2, column=3, padx=100, ipadx=100, ipady=30, pady=20)
        ################################################################################################
        self.title2 = Frame(self.frame_anti_tamper, padx=10, pady=1, bg="light sky blue")
        self.log_f_2 = Frame(self.frame_anti_tamper, padx=10, pady=20, bg="light sky blue")
        self.off_2 = Frame(self.frame_anti_tamper, padx=10, pady=70, bg="light sky blue")
        self.next_log_f_2 = Frame(self.frame_anti_tamper, padx=300, pady=30, bg="light sky blue",
                                  highlightbackground='blue', highlightthickness=20, highlightcolor='blue')
        left_label = Label(self.title2, bg="light sky blue", text="Anti-Tamper", font=LARGE_FONT_button_title)
        left_label.pack(fill="x")

        Label(self.log_f_2, text="Burning Result", font=LARGE_FONT_button1,
              bg="light sky blue").pack(padx=500)
        Label(self.log_f_2, text="****************************", font=LARGE_FONT_button1,
              bg='light sky blue').pack(padx=500)
        Label(self.log_f_2, textvariable=self.board_sn_AT, font=LARGE_FONT_button1, bg='light sky blue').pack(padx=500)
        Label(self.log_f_2, text="****************************", font=LARGE_FONT_button1,
              bg='light sky blue').pack(padx=500, pady=20)
        self.text_result = Text(self.log_f_2, height=9, width=115, borderwidth=20, relief='sunken')
        self.text_result.pack(pady=20)

        Label(self.off_2, text='', font=FONT, bg="light sky blue",
              fg="black").grid(row=2, column=0, pady=5, padx=25, sticky=W)
        Button(self.next_log_f_2, text="Pass\nBurning", bg="green", fg="white", font=FONT,
               command=self.result_pass, bd=12).grid(row=2, column=0, padx=100, ipadx=60, pady=20)
        Label(self.next_log_f_2, text="",bg='light sky blue', font=FONT).grid(row=2,
                                                                               column=1, padx=100, ipadx=100, ipady=30, pady=20)
        Button(self.next_log_f_2, text="Fail\nBurning", bg="blue", fg="white", font=FONT,
               command=self.stop_process_at, bd=12).grid(row=2, column=2, padx=100, ipadx=60, pady=20)
        ########################################################################################################
        ###############################################################################################
        # self.title_stop_process_at = Frame(self.frame_anti_tamper, padx=10, pady=1, bg="light sky blue")
        # self.log_f_stop_process_at = Frame(self.frame_anti_tamper, padx=10, pady=150, bg="light sky blue")
        # self.off_stop_process_at = Frame(self.frame_anti_tamper, padx=10, pady=150, bg="light sky blue")
        # self.next_log_f_stop_process_at = Frame(self.frame_anti_tamper, padx=10, pady=30, bg="light sky blue",
        #                                      highlightbackground='blue', highlightthickness=20, highlightcolor='blue')
        # left_label = Label(self.title_stop_process_at, bg="light sky blue", text="Burning Secure Input",
        #                    font=LARGE_FONT_button_title)
        # left_label.pack(fill="x")
        #
        # Label(self.log_f_stop_process_at, text='Stopping Process\nReason  ', bg="light sky blue",
        #       font=LARGE_FONT_button).grid(pady=20)
        #
        # options_stop_process = ("Error in process terminal", "Wrong Serial Number", "J-TAG Cable disconnected to PC",
        #                         "J-TAG Cable disconnected to K.B","J-Link box damaged", "J-TAG Cable damaged", "Kazuar Board damaged".split())
        # menu_stop_process = OptionMenu(self.log_f_stop_process_at, self.reason_at, *options_stop_process)
        # menu_stop_process.config(font=LARGE_FONT)
        # self.reason_at.set("Select")
        # menu_stop_process.grid(pady=20)
        #
        # self.next_at = Button(self.next_log_f_stop_process_at, text="Next Bord", bg="blue", fg="white", font=FONT,
        #                    command=self.check_stop_process_at, bd=12)
        # self.next_at.grid(row=2, column=0, padx=400, ipadx=50, ipady=30, pady=20)
        # Label(self.next_log_f_stop_process_at, text="", bg="light sky blue"
        #       ).grid(row=2, column=1, padx=100, ipadx=100, ipady=30, pady=20)
        # self.next_menu_at = Button(self.next_log_f_stop_process_at, text="Menu", bg="red", fg="white", font=FONT,
        #                         command=self.check_stop_process_at, bd=12)
        # self.next_menu_at.grid(row=2, column=2, padx=100, ipadx=100, ipady=30, pady=20)
        #####################################################333
        self.title_stop_process_at = Frame(self.frame_anti_tamper,padx=10,pady=1,bg="light sky blue")
        self.log_f_stop_process_at = Frame(self.frame_anti_tamper,padx=10,pady=100,bg="light sky blue")
        self.off_stop_process_at = Frame(self.frame_anti_tamper,padx=10,pady=150,bg="light sky blue")
        self.next_log_f_stop_process_at = Frame(self.frame_anti_tamper,padx=10,pady=30,bg="light sky blue",
                                             highlightbackground='blue',highlightthickness=20,highlightcolor='blue')
        left_label = Label(self.title_stop_process_at,bg="light sky blue",text="Anti-Tamper",font=LARGE_FONT_button_title)
        left_label.pack(fill="x")
        Label(self.log_f_stop_process_at,text='Process uncompleted..  ',bg="light sky blue",
              font=LARGE_FONT_button1).grid(pady=30)

        Label(self.log_f_stop_process_at,text='Stop Process\nReason  ',bg="light sky blue",
              font=LARGE_FONT_button).grid(pady=20)

        options_stop_process = ("Error in process terminal","Wrong Serial Number","J-TAG Cable disconnected to PC",
                                "J-TAG Cable disconnected to K.B","J-Link box damaged","J-TAG Cable damaged",
                                "Kazuar Board damaged".split())
        menu_stop_process = OptionMenu(self.log_f_stop_process_at,self.reason_at,*options_stop_process)
        menu_stop_process.config(font=LARGE_FONT)
        menu_stop_process.grid(pady=20)
        # self.reason_at.set("Select")

        self.next_at = Button(self.next_log_f_stop_process_at,text="Next Bord",bg="blue",fg="white",font=FONT,
                           command=self.check_stop_process_at,bd=12)
        self.next_at.grid(row=2,column=0,padx=400,ipadx=50,ipady=15)
        Label(self.next_log_f_stop_process_at,text="",bg="light sky blue"
              ).grid(row=2,column=1,padx=100,ipadx=100,ipady=15)
        self.next_menu_at = Button(self.next_log_f_stop_process_at,text="Menu",bg="red",fg="white",font=FONT,
                                command=self.check_stop_process_at,bd=12)
        self.next_menu_at.grid(row=2,column=2,padx=100,ipadx=100,ipady=15)

    def check_stop_process_at(self):
        if self.reason_at.get() == 'Select':
            messagebox.showerror('error', 'Mast to choice Stopping Process reason')
        else:
            self.result_fail_at()

    def stop_process_at(self):
        self.kill_process_at()
        self.title2.pack_forget()
        self.log_f_2.pack_forget()
        self.off_2.pack_forget()
        self.next_log_f_2.pack_forget()
        self.title_stop_process_at.pack()
        self.log_f_stop_process_at.pack(pady=100)
        self.off_stop_process_at.pack(pady=100)
        self.next_log_f_stop_process_at.pack(ipadx=1000)
    def kill_process_at(self):
        import os, signal

        def process ():

            name = "server"
            try:
                # iterating through each instance of the process
                for line in os.popen("ps ax | grep " + name):
                    fields = line.split()
                    # extracting Process ID from the output
                    pid = fields[0]
                    # terminating process
                    os.kill(int(pid), signal.SIGKILL)
                print("Process Successfully terminated")
            except:
                print('hi')

        process()
    def start_page_ant_tamper(self):
        self.frame_anti_tamper.pack( )

    def go_back_anti_tamper(self):
        self.frame_anti_tamper.pack_forget( )
        self.app_anti_tamper.menu_page( )

    def check_at_input (self):
        if self.board_sn_AT.get() == "":
            messagebox.showerror('error!', 'Missing S/N number')
        else:
            self.check_number_latter_and_digit_at()
    def check_number_latter_and_digit_at(self):
        digit = letter = space = 0
        for ch in self.board_sn_AT.get():
            if ch.isdigit():
                digit = digit + 1
            elif ch.isalpha():
                letter = letter + 1
            elif ch == '-':
                space = space + 1
            else:
                pass
        print("Letters:", letter)
        print("Digits:", digit)
        print("Characters:", space)
        if 20 <= letter + digit + space < 21:
            print('enough numbers')
            self.check_secure_input_in_db()
        else:
            print('NOT enough numbers')
            messagebox.showerror('Error', 'Not enough numbers\nIn serial number\nPlease check.. ')


    def check_secure_input_in_db (self):
        with sqlite3.connect('Kazuar_tester_PC.db') as self.db:
            self.c=self.db.cursor()

        find_user = 'SELECT * FROM sec_in_input_user_db WHERE SN = ?'
        self.c.execute(find_user, [(self.board_sn_AT.get())])

        if not self.c.fetchall():
            messagebox.showerror('Error!', f'{self.board_sn_AT.get()}\nNot burnt yet!\nPlease burn Secure Input first!.')
        else:
            self.check_si_status_on_board()
    def check_si_status_on_board(self):
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT *, oid FROM sec_in_input_user_db WHERE SN = ?", (self.board_sn_AT.get(),))
        records = self.c.fetchall()

        for self.record in records:
            if self.record[3] == 'NO':
                print('status fail')
                messagebox.showerror('Error', f'{self.board_sn_AT.get()}\n failed in Secure Input burning!\n'
                                              f'Replace it with different one\nConnect Kazuar to check it ')
            else:
                print('status pass')
                self.check_input_in_anti_tamper_db()

    def check_input_in_anti_tamper_db (self):
            with sqlite3.connect('Kazuar_tester_PC.db') as self.db:
                self.c1=self.db.cursor()

            find_user='SELECT * FROM AT_input_user_db WHERE SN_Kazuar_Board = ?'
            self.c1.execute(find_user, [(self.board_sn_AT.get())])

            if self.c1.fetchall():
                messagebox.showerror('Error!', f'{self.board_sn_AT.get()}\nAlready burnt!\nTry a different one.')
            else:
                self.connect_anti_tamper_j_tag()

    def connect_anti_tamper_j_tag(self):
        self.title.pack_forget()
        self.log_f.pack_forget()
        self.next_log_f.pack_forget()

        self.title1_at.pack()
        self.log_f_1_at.pack()
        self.next_log_f_1_at.pack(ipadx=400, fill=X)

    def check_anti_tamper_connect (self):
        msg_anti_tamper=tk.messagebox.askquestion('cmd', 'Are you sure the anti tamper connected? ')
        if msg_anti_tamper == 'yes':
            x = os.system("lsusb | grep SEGGER")
            if x == 0:
                print("connected")
                self.terminal_for_anti_tamper()
                self.pass_fail_result()

            else:
                print("disconnected")
                ret = messagebox.showerror('error', 'cable disconnected\nor not approved!\nplease check it ')
                if ret == 'ok':
                    self.back_to_main_anti_tamper()

        else:
            pass

    def check_anti_tamper_status (self):
        msg_anti_tamper_status=tk.messagebox.askquestion('cmd', 'Re-connect the anti tamper')
        if msg_anti_tamper_status == 'yes':
            x = os.system("lsusb | grep SEGGER")
            if x == 0:
                print("connected")
                self.terminal_for_anti_tamper_status()
                self.status_result()

            else:
                print("disconnected")
                ret = messagebox.showerror('error', 'cable disconnected\nor not approved!\nplease check it ')
                if ret == 'ok':
                    self.back_to_main()
        else:
            pass
    def status_result(self):
        self.title1_at.pack_forget()
        self.log_f_1_at.pack_forget()
        self.next_log_f_1_at.pack_forget()
        self.text_result.pack_forget()


        self.title2.pack()
        self.log_f_2.pack()
        self.off_2.pack()
        self.next_log_f_2.pack(ipadx=400, fill=X)

    def pass_fail_result (self):
        self.title1_at.pack_forget()
        self.log_f_1_at.pack_forget()
        self.next_log_f_1_at.pack_forget()

        self.title2.pack()
        self.log_f_2.pack()
        self.off_2.pack()
        self.next_log_f_2.pack(ipadx=400, fill=X)
    def back_to_main_anti_tamper(self):
        self.title1_at.pack_forget()
        self.log_f_1_at.pack_forget()
        self.next_log_f_1_at.pack_forget()
        self.title2.pack_forget()
        self.log_f_2.pack_forget()
        self.next_log_f_2.pack_forget()
        self.off_2.pack_forget()
        self.title_stop_process_at.pack_forget()
        self.log_f_stop_process_at.pack_forget()
        self.next_log_f_stop_process_at.pack_forget()
        self.off_stop_process_at.pack_forget()

        self.title.pack()
        self.log_f.pack()
        self.board_sn_AT.set(self.getelementValue(self.xmlDocument,"boardsnAT"))
        self.next_log_f.pack(ipadx=400, fill=X)

    def terminal_for_anti_tamper (self):
        import subprocess
        import os
        cmd = "gnome-terminal --geometry=100x5+182+300 " \
              f"--working-directory={self.WorkingDirectory} -- bash -c \"echo " \
              f"{self.PcPassword} | sudo -S {self.FileAT}\""
        subprocess.Popen(args=[cmd], shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)

    def terminal_for_anti_tamper_status (self):
        import subprocess
        import os
        cmd = "gnome-terminal --geometry=100x5+182+300 " \
              f"--working-directory={self.AntiTamperStatusWorkingDirectory} -- bash -c \"echo " \
              f"{self.PcPassword} | sudo -S {self.FileToAntiTamper}\""
        subprocess.Popen(args=[cmd], shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)

    def result_pass (self):
        self.kill_process_at()
        # Create a database or connect to one
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        # Insert Into Table
        self.c.execute("INSERT INTO AT_input_user_db VALUES (:Date, :User, :SN_Kazuar_Board, :AT_version, :Result)",
                  {
                      'Date': time.strftime("%D %H:%M:%S"),
                      'User': self.user_enter,
                      'SN_Kazuar_Board': self.board_sn_AT.get().upper(),
                      'AT_version': self.AT_version.get(),
                      'Result': 'Process Completed!'
                  })

        self.conn.commit()
        self.conn.close()
        print('pass')
        self.back_to_main_anti_tamper()

    def result_fail_at (self):
        # Create a database or connect to one
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        # Insert Into Table
        self.c.execute("INSERT INTO AT_input_user_db VALUES (:Date, :User, :SN_Kazuar_Board, :AT_version, :Result)",
                  {
                      'Date': time.strftime("%D %H:%M:%S"),
                      'User': self.user_enter,
                      'SN_Kazuar_Board': self.board_sn_AT.get().upper(),
                      'AT_version': self.AT_version.get(),
                      'Result': 'fail'
                  })

        self.conn.commit()
        self.conn.close()
        print('fail')
        with open(self.FileForResultsAT, "a") as file_object:
            # Append board serial number + stop reason to the file
            file_object.write(f'\n{self.board_sn_AT.get()} stop process due to + {self.reason_at.get()}'
                              f' + {time.strftime("%D %H:%M:%S")}\n')
            print(file_object)
        self.back_to_main_anti_tamper()


class sec_out:

    def __init__(self, master=None, app_sec_out=None):
        self.text_p = None
        self.next_menu = None
        self.next = None
        self.title_stop_process = None
        self.log_f_stop_process = None
        self.off_stop_process = None
        self.next_log_f_stop_process = None
        self.menu = None
        self.stopper = None
        self.label = None
        self.execute_r = None
        self.text = None
        self.failure = None
        self.off_3 = None
        self.frame_sec_out = None
        self.button_confirmed_process = None
        self.title_sec_out =None
        self.log_f_sec_out = None
        self.but_sec_out = None
        self.next_log_f_sec_out = None
        self.but = None
        self.but_new = None
        self.but_confirmed = None
        self.title = None
        self.log_f = None
        self.next_log_f = None
        self.title1 = None
        self.log_f_1 = None
        self.next_log_f_1 = None
        self.title2 = None
        self.log_f_2 = None
        self.next_log_f_2 = None
        self.title3 = None
        self.log_f_3 = None
        self.next_log_f_3 = None
        self.title_input = None
        self.log_f_input = None
        self.next_log_f_input = None
        self.root_sec_out_database_query = None
        self.last_line = None
        self.off = None
        self.off_2 = None
        self.conn = None
        self.c = None
        self.c1 = None
        self.c2 = None
        self.button = None
        self.img = None
        ##########################################
        # read and parse XML document
        self.DOMTree = xml.dom.minidom.parse("GUI_Config_Pages_File.xml")

        # create attribute for XML document
        self.xmlDocument = self.DOMTree.documentElement
        ##########################################
        self.master = master

        self.board_sn = StringVar()
        self.board_sn.set(self.getelementValue(self.xmlDocument,"boardsn"))

        self.som_sn_sec_out = StringVar()
        self.som_sn_sec_out.set(self.getelementValue(self.xmlDocument,"sompn"))

        self.som_version = StringVar()
        self.som_version.set(self.getelementValue(self.xmlDocument,"somversion"))

        self.board_sn_sec_out = StringVar()
        self.board_sn_sec_out.set(self.getelementValue(self.xmlDocument,"boardSO"))

        self.reason_sec_out = StringVar()
        self.reason_sec_out.set(self.getelementValue(self.xmlDocument,"ReasonFailureSo"))

        self.WorkingDirectorySo = StringVar()
        self.WorkingDirectorySo = self.getelementValue(self.xmlDocument,"WorkingDirectorySo")
        self.PcPassword = StringVar()
        self.PcPassword = self.getelementValue(self.xmlDocument,"TesterPcPassword")
        # 12345
        self.FileForSoProcess = StringVar()
        self.FileForSoProcess = self.getelementValue(self.xmlDocument,"FlashImgFile")
        self.FileForSoProcessLogs = StringVar()
        self.FileForSoProcessLogs = self.getelementValue(self.xmlDocument,"FlashLogFile")
        # secout_log.txt



        self.widget_sec_out()
        self.root_sec_out_database_query = None
        self.app_sec_out = app_sec_out
        self.conn = sqlite3.connect('Kazuar.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user')
        self.user_enter = self.c.fetchall()[0][0]

    # get value of an XML element with specified name
    def getelementValue (self,parent, name):
        if parent.childNodes:
            for node in parent.childNodes:
                if node.nodeType == node.ELEMENT_NODE:
                    if node.tagName == name:
                        if node.hasChildNodes:
                            child = node.firstChild
                            return child.nodeValue
        return None


    def widget_sec_out(self):
        self.frame_sec_out = tk.Frame(self.master, bg='light sky blue')
        self.title_sec_out = Frame(self.frame_sec_out, padx=10, pady=20, bg="light sky blue")
        self.but_sec_out = Frame(self.frame_sec_out, padx=100, pady=80, bg="light sky blue")
        self.next_log_f_sec_out = Frame(self.frame_sec_out, padx=930, bg="light sky blue",
                                highlightbackground='blue', highlightthickness=20, highlightcolor='blue')
        left_label = Label(self.title_sec_out, bg="light sky blue", text="Burning Secure Output", font=LARGE_FONT_button_title)
        left_label.grid(row=0, column=0, pady=5, padx=25, sticky=N)

        Button(self.but_sec_out, text="Confirmed\nSOM", bg="green", fg='white', font=LARGE_FONT_button1,
               command=self.sec_out_input_confirm, bd=12, state=NORMAL).grid(row=2, column=0, pady=20, sticky=N, padx=150)

        Button(self.but_sec_out, text="New\nSOM", bg="slate blue", fg='white', font=LARGE_FONT_button1,
               command=self.sec_out_input_new, bd=12).grid(row=2, column=2, ipadx=120, pady=20, sticky=N)

        Button(self.next_log_f_sec_out, text="Menu", bg="red", fg="white", font=FONT,
               command=self.go_back_sec_out, bd=12).grid(row=4, column=1, padx=100, ipadx=100, ipady=30, sticky=N)

        self.title_sec_out.pack( )
        self.but_sec_out.pack(padx=500, ipadx=250, ipady=320)
        self.next_log_f_sec_out.pack(ipadx=1000)
        ###########################################################################################################
        self.title_input = Frame(self.frame_sec_out, padx=10, pady=1, bg="light sky blue")
        self.log_f_input = Frame(self.frame_sec_out, padx=10, pady=50, bg="light sky blue")
        self.next_log_f_input = Frame(self.frame_sec_out, padx=10, pady=50, bg="light sky blue",
                                      highlightbackground='blue', highlightthickness=20, highlightcolor='blue')

        Label(self.title_input, text='Burning Secure Output', font=LARGE_FONT_button_title, bg="light sky blue",
              fg="black").grid(row=0, column=0, pady=5, padx=25, sticky=N)
        Label(self.log_f_input, text='Kazuar Board\nSerial Number', font=LARGE_FONT_button, bg="light sky blue",
              fg="black").grid(row=0, column=0, pady=20, padx=40, sticky=N)

        Entry(self.log_f_input, textvariable=self.board_sn_sec_out, bd=10, font=LARGE_FONT_button).grid(row=1, column=0,
                                                                                                       pady=10)
        # self.board_sn_sec_out.set('NS-KB31-R01-XXXXXXXX')

        Label(self.log_f_input, text="SOM\nSerial Number", font=LARGE_FONT_button,
              bg="light sky blue").grid(row=2, column=0, pady=30, sticky=N)
        Entry(self.log_f_input, textvariable=self.som_sn_sec_out, font=LARGE_FONT_button,
              width=13, bd=10).grid(row=3, column=0, pady=10)
        # self.som_sn_sec_out.set('F8DC7AXXXXXX')

        Label(self.log_f_input, text="SOM Version ", font=LARGE_FONT_button,
              bg="light sky blue").grid(row=4, column=0, pady=30)
        options = ("full No-wifi".split( ))
        menu = OptionMenu(self.log_f_input, self.som_version, *options)
        menu.config(font=LARGE_FONT_button, bd=10)
        # self.som_version.set("full")
        menu.grid(ipadx=10, row=5, column=0)
        self.but_confirmed = Button(self.next_log_f_input, text="Confirmed\nSOM", bg="green", fg="white", font=FONT,
                                    command=self.check_som_board_input_confirm, bd=12)
        self.but_confirmed.grid(row=2, column=0, padx=100, pady=20)

        Button(self.next_log_f_input, text="SecOut\nMenu", bg="blue", fg="white", font=FONT,
               command=self.back_to_main, bd=12).grid(row=2, column=1, padx=100, ipadx=80, pady=20)
        self.but_new = Button(self.next_log_f_input, text="New\nSOM", bg="slate blue", fg="white", font=FONT,
                              command=self.check_som_board_input_new_som, bd=12)
        self.but_new.grid(row=2, column=2, padx=100, ipadx=100, pady=20)
        Button(self.next_log_f_input, text="Menu", bg="red", fg="white", font=FONT,
               command=self.go_back_sec_out, bd=12).grid(row=2, column=3, padx=100, ipadx=100, ipady=30, pady=20)
        ###########################################################################################################
        self.title1 = Frame(self.frame_sec_out, padx=10, pady=1, bg="light sky blue")
        self.log_f_1 = Frame(self.frame_sec_out, padx=10, pady=15, bg="light sky blue")
        self.next_log_f_1 = Frame(self.frame_sec_out, padx=10, pady=5, bg="light sky blue",
                                  highlightbackground='blue', highlightthickness=20, highlightcolor='blue')

        left_label = Label(self.title1, bg="light sky blue", text="Secure Output", font=LARGE_FONT_button_title)
        left_label.pack(fill="x")

        Label(self.log_f_1, text="1. Place Kazuar Board into the JIG and tight\n"
                                 "2. Connect the Kazuar board to connector type C\n"
                                 "3. Connect the connector type C to tester PC",
              font=LARGE_FONT, bg="light sky blue").pack( )
        Label(self.log_f_1, text="***** Check if red LED on Kazuar board bottom is ON *****",
              font=LARGE_FONT, bg="light sky blue", fg='red').pack( )
        self.img = ImageTk.PhotoImage(Image.open("/home/tester/PycharmProjects/GUI_production_kazuar/image"
                                                 "/secin1.png"))
        Label(self.log_f_1, image=self.img, borderwidth=0, bg='light sky blue', relief="flat").pack(pady=15)
        self.button_confirmed_process = Button(self.next_log_f_1, text="Confirmed\nSOM", bg="green", fg="white",
                                               font=FONT,
                                               command=self.completed_process_sec_out, bd=12)
        self.button_confirmed_process.grid(row=2, column=0, padx=100, pady=20)
        Button(self.next_log_f_1, text="Back", bg="blue", fg="white", font=FONT,
               command=self.back_to_main, bd=12).grid(row=2, column=1, padx=100, ipadx=100, ipady=30, pady=20)
        Button(self.next_log_f_1, text="New\nSOM", bg="slate blue", fg="white", font=FONT,
               command=self.start_process_new_som, bd=12).grid(row=2, column=2, padx=100, ipadx=100, pady=20)
        Button(self.next_log_f_1, text="Menu", bg="red", fg="white", font=FONT,
               command=self.go_back_sec_out, bd=12).grid(row=2, column=3, padx=100, ipadx=100, ipady=30, pady=20)
        ###############################################################################################
        self.title2 = Frame(self.frame_sec_out, padx=10, pady=1, bg="light sky blue")
        self.log_f_2 = Frame(self.frame_sec_out, padx=150, bg="light sky blue")
        self.off_2 = Frame(self.frame_sec_out, padx=10, pady=90, bg="light sky blue")
        self.next_log_f_2 = Frame(self.frame_sec_out, padx=10, bg="light sky blue",
                                  highlightbackground='blue', highlightthickness=20, highlightcolor='blue')
        left_label = Label(self.title2, bg="light sky blue", text="Secure Output", font=LARGE_FONT_button_title)
        left_label.pack(fill="x", pady=10)
        Label(self.off_2, bg="light sky blue", font=LARGE_FONT_button_title).grid(pady=60)
        Label(self.log_f_2, text="****************************", font=LARGE_FONT_button1,
              bg='light sky blue').pack(padx=500)
        Label(self.log_f_2, textvariable=self.board_sn_sec_out, font=LARGE_FONT_button1, bg='light sky blue').pack(padx=500)
        self.failure = Label(self.log_f_2, text="****************************", font=LARGE_FONT_button1,
                             bg='light sky blue')
        self.failure.pack(padx=500, pady=50)
        self.text = Button(self.log_f_2, text='Press\nStart Process', bg='light sky blue',
                           font=LARGE_FONT_button1, relief=FLAT)
        self.text.pack(ipadx=10)

        Label(self.off_2, text='', font=FONT, bg="light sky blue",
              fg="black").grid(row=2, column=0, padx=25, sticky=W)
        self.execute_r = Button(self.next_log_f_2, text="Start\nProcess", font=FONT, fg='white',
                                bg='green', command=self.check_sec_out_connect, bd=10)
        self.execute_r.grid(row=2, column=0, padx=50, ipadx=60)
        self.label = Label(self.next_log_f_2, text="", font=LARGE_FONT_button1, bg='light sky blue', fg='black',
                           relief=FLAT)
        self.label.grid(row=2, column=1, padx=130, ipadx=60)

        self.stopper = Button(self.next_log_f_2, text="Stop\nProcess", font=FONT, fg='white',
                              bg='red', command=self.stop_process_sec_out, bd=10, state=DISABLED)
        self.stopper.grid(row=2, column=2, padx=130, ipadx=60)

        self.menu = Button(self.next_log_f_2, text="Menu", font=FONT, fg='white',
                           bg='red', command=self.stop_process_sec_out, bd=10)
        self.menu.grid(row=2, column=3, padx=300, ipadx=100, ipady=30)
        #################################################################################################
        self.title_stop_process = Frame(self.frame_sec_out, padx=10, pady=1, bg="light sky blue")
        self.log_f_stop_process = Frame(self.frame_sec_out, padx=10, pady=150, bg="light sky blue")
        self.off_stop_process = Frame(self.frame_sec_out, padx=10, pady=150, bg="light sky blue")
        self.next_log_f_stop_process = Frame(self.frame_sec_out, padx=10, pady=30, bg="light sky blue",
                                             highlightbackground='blue', highlightthickness=20, highlightcolor='blue')
        left_label = Label(self.title_stop_process, bg="light sky blue", text="Secure Output",
                           font=LARGE_FONT_button_title)
        left_label.pack(fill="x")

        Label(self.log_f_stop_process, text='Stopping Process\nReason  ', bg="light sky blue",
              font=LARGE_FONT_button).grid(pady=20)

        options_stop_process = ("Error in process terminal", "Wrong Serial Number", "USB Cable disconnected to PC",
                                "USB Cable disconnected to K.B", "USB Cable damaged", "Kazuar Board damaged".split())
        menu_stop_process = OptionMenu(self.log_f_stop_process, self.reason_sec_out, *options_stop_process)
        menu_stop_process.config(font=LARGE_FONT)
        # self.reason_sec_out.set("Select")
        menu_stop_process.grid(pady=20)

        self.next = Button(self.next_log_f_stop_process, text="Next Bord", bg="blue", fg="white", font=FONT,
                           command=self.check_stop_process_sec_out, bd=12)
        self.next.grid(row=2, column=0, padx=400, ipadx=50, ipady=30, pady=20)
        Label(self.next_log_f_stop_process, text="", bg="light sky blue"
              ).grid(row=2, column=1, padx=100, ipadx=100, ipady=30, pady=20)
        self.next_menu = Button(self.next_log_f_stop_process, text="Menu", bg="red", fg="white", font=FONT,
                                command=self.check_stop_process_sec_out, bd=12)
        self.next_menu.grid(row=2, column=2, padx=100, ipadx=100, ipady=30, pady=20)
        ########################################################################################################
        self.title3 = Frame(self.frame_sec_out, padx=10, pady=1, bg="light sky blue")
        self.log_f_3 = Frame(self.frame_sec_out, padx=10, pady=20, bg="light sky blue")
        self.off_3 = Frame(self.frame_sec_out, padx=10, pady=50, bg="light sky blue")
        self.next_log_f_3 = Frame(self.frame_sec_out, padx=50, pady=30, bg="light sky blue",
                                  highlightbackground='blue', highlightthickness=20, highlightcolor='blue')
        left_label = Label(self.title3, bg="light sky blue", text="Secure Output", font=LARGE_FONT_button_title)
        left_label.pack(fill="x")

        Label(self.log_f_3, text="Burning Result", font=LARGE_FONT_button1,
              bg="light sky blue").pack(padx=500)
        Label(self.log_f_3, text="****************************", font=LARGE_FONT_button1,
              bg='light sky blue').pack(padx=500)
        Label(self.log_f_3, textvariable=self.board_sn_sec_out, font=LARGE_FONT_button1, bg='light sky blue').pack(
            padx=500)
        Label(self.log_f_3, text='+', font=LARGE_FONT_button1, bg='light sky blue').pack(
            padx=500)
        Label(self.log_f_3, textvariable=self.som_sn_sec_out, font=LARGE_FONT_button1,
              bg='light sky blue').pack(padx=500)
        Label(self.log_f_3, text="Process Completed!", font=LARGE_FONT_button1,
              bg='light sky blue').pack(padx=500, pady=20)
        Label(self.log_f_3, text="****************************", font=LARGE_FONT_button1,
              bg='light sky blue').pack(padx=500, pady=20)
        Label(self.off_3, text="", bg="light sky blue", fg="white"
              , relief=FLAT).grid(row=2, column=1, padx=100, ipadx=100, ipady=30, pady=20)

        Button(self.next_log_f_3, text="New\nBoard", bg="green", fg="white", font=FONT,
               command=self.back_to_main, bd=12).grid(row=2, column=0, padx=500, ipadx=80, pady=20)

        Button(self.next_log_f_3, text="Menu", bg="red", fg="white", font=FONT,
               command=self.go_back_sec_out, bd=12).grid(row=2, column=2, padx=100, ipadx=100, ipady=30, pady=20)
        #######################################################################################################
    def kill_process(self):
        import os, signal

        def process ():

            name = "server"
            try:
                # iterating through each instance of the process
                for line in os.popen("ps ax | grep " + name):
                    fields = line.split()
                    # extracting Process ID from the output
                    pid = fields[0]
                    # terminating process
                    os.kill(int(pid), signal.SIGKILL)
                print("Process Successfully terminated")
            except:
                print('hi')

        process()
    def check_stop_process_sec_out(self):
        if self.reason_sec_out.get() == 'Select':
            messagebox.showerror('error', 'Mast to choice Stopping Process reason')
        else:
            if self.next:
                self.result_fail_sec_out()
            elif self.next_menu:
                self.result_fail_sec_out()
            else:
                pass
    def stop_process_sec_out(self):
        self.kill_process()
        self.title2.pack_forget()
        self.log_f_2.pack_forget()
        self.off_2.pack_forget()
        self.next_log_f_2.pack_forget()
        self.title_stop_process.pack()
        self.log_f_stop_process.pack(pady=100)
        self.off_stop_process.pack(pady=100)
        self.next_log_f_stop_process.pack(ipadx=1000)
        
    def start_page_sec_out(self):
        self.frame_sec_out.pack( )

    def go_back_sec_out(self):
        self.title_input.pack_forget()
        self.log_f_input.pack_forget()
        self.next_log_f_input.pack_forget()
        self.title1.pack_forget()
        self.log_f_1.pack_forget()
        self.next_log_f_1.pack_forget()
        self.title3.pack_forget()
        self.log_f_3.pack_forget()
        self.off_3.pack_forget()
        self.next_log_f_3.pack_forget()

        self.frame_sec_out.pack_forget( )
        self.app_sec_out.menu_page( )

   
    def result_pass_sec_out (self):
            # Create a database or connect to one
            self.conn = sqlite3.connect('Kazuar_tester_PC.db')
            self.c = self.conn.cursor( )
            # Insert Into Table
            self.c.execute("INSERT INTO sec_out_input_user_db VALUES (:Date, :User, :SN_Kazuar_Board, :SN_SOM_Board, "
                           ":Som_version)",
                           {
                               'Date': time.strftime("%D %H:%M:%S"),
                               'User': self.user_enter,
                               'SN_Kazuar_Board': self.board_sn_sec_out.get().upper(),
                               'SN_SOM_Board': self.som_sn_sec_out.get().upper(),
                               'Som_version': self.som_version.get().upper()
                           })

            self.conn.commit( )
            self.conn.close( )
            print('pass')

    def result_fail_sec_out (self):
        # Create a database or connect to one
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        # Insert Into Table
        self.c.execute("INSERT INTO sec_out_input_user_db VALUES (:Date, :User, :SN_Kazuar_Board, :SN_SOM_Board, "
                       ":Som_version)",
                       {
                           'Date': time.strftime("%D %H:%M:%S"),
                           'User': self.user_enter,
                           'SN_Kazuar_Board': self.board_sn_sec_out.get().upper(),
                           'SN_SOM_Board': self.som_sn_sec_out.get().upper(),
                           'Som_version': self.som_version.get().upper()
                       })

        self.conn.commit()
        self.conn.close()
        print('fail')
        self.back_to_main()


        '''cmd displayed and run commend of flashing SecIn img '''

    def check_sec_out_connect (self):
            msg_sec_out = tk.messagebox.askquestion('cmd', 'Are you sure the connector type C connected? ')
            if msg_sec_out == 'yes':
                import os
                x = os.system("lsusb | grep Microchip")
                if x == 0:
                    print("connected")
                    self.execute_r.config(state=DISABLED)
                    self.label.config(text='Connected to the process..\nDo not touch the system!!')
                    self.label.config(bg='red',fg='white')
                    self.menu.grid_forget()
                    self.stopper.config(state=NORMAL)

                    import subprocess
                    import os


                    cmd = f"gnome-terminal --geometry=100x16+185+240  --working-directory={self.WorkingDirectorySo} -- bash -c \"echo " \
                          f"{self.PcPassword} | sudo -S ./{self.FileForSoProcess} |& tee {self.FileForSoProcessLogs}; exec bash\" "
                    self.text_p = subprocess.Popen(args=[cmd],shell=True,stdout=subprocess.PIPE,
                                                   preexec_fn=os.setsid,stderr=subprocess.PIPE,
                                                   universal_newlines=True)

                    print('Working')
                    if self.text_p:
                        time.sleep(1)
                        self.text.config(text='Successful',bd=10,bg='green',font=LARGE_FONT_button_title2,
                                         relief=RAISED)
                        self.text.config(command=self.completed_process_sec_out)
                        print('Working1')
                else:
                    print("disconnected")
                    ret = messagebox.showerror('error','cable disconnected\nor not approved!\nplease check it ')
                    if ret == 'ok':
                        pass

    def completed_process_sec_out (self):
            self.result_pass_sec_out()
            self.title1.pack_forget( )
            self.log_f_1.pack_forget( )
            self.next_log_f_1.pack_forget( )
            self.title_input.pack_forget( )
            self.log_f_input.pack_forget( )
            self.next_log_f_input.pack_forget( )
            self.title2.pack_forget()
            self.log_f_2.pack_forget()
            self.off_2.pack_forget()
            self.next_log_f_2.pack_forget()

            self.title3.pack( )
            self.log_f_3.pack()
            self.off_3.pack(pady=30)
            self.next_log_f_3.pack(ipadx=1000, expand=True)


    def pass_fail_result (self):
            self.title1.pack_forget( )
            self.log_f_1.pack_forget( )
            self.next_log_f_1.pack_forget( )

            self.title2.pack( )
            self.log_f_2.pack( )
            self.off_2.pack( )
            self.next_log_f_2.pack( )

    def back_to_main (self):
            self.title1.pack_forget( )
            self.log_f_1.pack_forget( )
            self.next_log_f_1.pack_forget( )
            self.title2.pack_forget( )
            self.log_f_2.pack_forget( )
            self.next_log_f_2.pack_forget( )
            self.off_2.pack_forget( )
            self.title_input.pack_forget( )
            self.log_f_input.pack_forget( )
            self.next_log_f_input.pack_forget( )
            self.but_new.config(state=ACTIVE)
            self.but_confirmed.config(state=ACTIVE)
            self.title3.pack_forget( )
            self.log_f_3.pack_forget( )
            self.off_3.pack_forget()
            self.next_log_f_3.pack_forget( )
            self.title_stop_process.pack_forget()
            self.log_f_stop_process.pack_forget()
            self.off_stop_process.pack_forget()
            self.next_log_f_stop_process.pack_forget()

            self.title_sec_out.pack()
            self.but_sec_out.pack(padx=500, ipadx=250, ipady=320)
            self.next_log_f_sec_out.pack(ipadx=1000)

    def sec_out_input_new (self):
            self.title_sec_out.pack_forget()
            self.but_sec_out.pack_forget()
            self.next_log_f_sec_out.pack_forget()

            self.som_sn_sec_out.set(self.getelementValue(self.xmlDocument,"sompn"))
            self.board_sn_sec_out.set(self.getelementValue(self.xmlDocument,"boardSO"))
            self.but_confirmed.config(state=DISABLED)

            self.title_input.pack( )
            self.log_f_input.pack( )
            self.next_log_f_input.pack(fill=X, ipadx=50)

    def sec_out_input_confirm (self):
            self.title_sec_out.pack_forget( )
            self.but_sec_out.pack_forget()
            self.next_log_f_sec_out.pack_forget( )
            self.som_sn_sec_out.set(self.getelementValue(self.xmlDocument,"sompn"))
            self.board_sn_sec_out.set(self.getelementValue(self.xmlDocument,"boardSO"))

            self.but_new.config(state=DISABLED)

            self.title_input.pack( )
            self.log_f_input.pack( )
            self.next_log_f_input.pack(fill=X, ipadx=50)

    def connect_board_sec_out (self):
            self.log_f_input.pack_forget( )
            self.title_input.pack_forget( )
            self.next_log_f_input.pack_forget( )
            self.button_confirmed_process.config(state=DISABLED)

            #####
            self.title1.pack( )
            self.log_f_1.pack( )
            self.next_log_f_1.pack( )

        #######################################################################3333
    def start_process_new_som(self):
        self.title1.pack_forget()
        self.log_f_1.pack_forget()
        self.next_log_f_1.pack_forget()

        self.title2.pack()
        self.log_f_2.pack()
        self.off_2.pack()
        self.next_log_f_2.pack()
    def check_som_board_input_confirm (self):
            if self.board_sn_sec_out.get( ) == "" or self.som_sn_sec_out.get( ) == "":
                messagebox.showerror('error!', 'Missing S/N number')
            else:
                self.check_number_latter_and_digit_confirm_som( )

    def check_number_latter_and_digit_confirm_som(self):
        digit = letter = space = 0
        digit_som = letter_som = space_som = 0
        for ch in self.board_sn_sec_out.get():
            if ch.isdigit():
                digit = digit + 1
            elif ch.isalpha():
                letter = letter + 1
            elif ch == '-':
                space = space + 1
            else:
                pass
        print("Letters:", letter)
        print("Digits:", digit)
        print("Characters:", space)
        for ch_som in self.som_sn_sec_out.get():
            if ch_som.isdigit():
                digit_som = digit_som + 1
            elif ch_som.isalpha():
                letter_som = letter_som + 1
            elif ch_som == '-':
                space_som = space_som + 1
            else:
                pass
        print("Letters:", letter_som)
        print("Digits:", digit_som)
        print("Characters:", space_som)
        if 20 <= letter + digit + space < 21 and 12 <= letter_som + digit_som + space_som < 13:
            print('enough numbers')
            self.check_input_in_sec_out_db()
        else:
            print('NOT enough numbers')
            messagebox.showerror('Error', 'Not enough numbers\nIn serial numbers\nPlease check.. ')

    def check_input_in_sec_out_db (self):
            with sqlite3.connect('Kazuar_tester_PC.db') as self.db:
                self.c = self.db.cursor( )
            find_user = 'SELECT SN FROM sec_in_input_user_db WHERE SN = ?'
            self.c.execute(find_user, [(self.board_sn_sec_out.get( ))])
            if not self.c.fetchall( ):
                messagebox.showerror('Error!', f'{self.board_sn_sec_out.get()}\nNot burnt yet!\nPlease burn Secure Input first!')
            else:
                self.check_input_in_db( )

    def check_input_in_db (self):
            with sqlite3.connect('Kazuar_tester_PC.db') as self.db:
                self.c = self.db.cursor( )
                self.c1 = self.db.cursor( )
                self.c2 = self.db.cursor( )
            find_data = 'SELECT * FROM sec_out_input_user_db WHERE SN_SOM_Board = ? and SN_Kazuar_Board = ?'
            self.c.execute(find_data, [(self.som_sn_sec_out.get( )), (self.board_sn_sec_out.get( ))])
            find_data1 = 'SELECT * FROM sec_out_input_user_db WHERE SN_Kazuar_Board = ?'
            self.c1.execute(find_data1, [(self.board_sn_sec_out.get( ))])
            find_data2 = 'SELECT * FROM sec_out_input_user_db WHERE SN_SOM_Board = ?'
            self.c2.execute(find_data2, [(self.som_sn_sec_out.get( ))])
            if self.c.fetchall( ):
                messagebox.showerror('Error!',
                                     f'Kazuar Board-{self.board_sn_sec_out.get( )} and\nSOM-{self.som_sn_sec_out.get( )}\n'
                                     f'already burned!\nTry a different ones.')
            elif self.c1.fetchall( ):
                messagebox.showerror('Error!', f'Kazuar Board- {self.board_sn_sec_out.get( )}\nalready burned!\nTry a '
                                               f'different one.')
            elif self.c2.fetchall( ):
                messagebox.showerror('Error!',
                                     f'SOM- {self.som_sn_sec_out.get( )}\nalready burned!\nTry a different one.')
            else:
                self.completed_process_sec_out( )

    def check_som_board_input_new_som (self):
            if self.board_sn_sec_out.get( ) == "" or self.som_sn_sec_out.get( ) == "":
                messagebox.showerror('error!', 'Missing S/N number')
            else:
                self.check_number_latter_and_digit_new_som( )

    def check_number_latter_and_digit_new_som(self):
        digit = letter = space = 0
        digit_som = letter_som = space_som = 0
        for ch in self.board_sn_sec_out.get():
            if ch.isdigit():
                digit = digit + 1
            elif ch.isalpha():
                letter = letter + 1
            elif ch == '-':
                space = space + 1
            else:
                pass
        print("Letters:", letter)
        print("Digits:", digit)
        print("Characters:", space)
        for ch_som in self.som_sn_sec_out.get():
            if ch_som.isdigit():
                digit_som = digit_som + 1
            elif ch_som.isalpha():
                letter_som = letter_som + 1
            elif ch_som == '-':
                space_som = space_som + 1
            else:
                pass
        print("Letters:", letter_som)
        print("Digits:", digit_som)
        print("Characters:", space_som)
        if 20 <= letter + digit + space < 21 and 12 <= letter_som + digit_som + space_som < 13:
            print('enough numbers')
            self.check_input_in_sec_out_new_som_db()
        else:
            print('NOT enough numbers')
            messagebox.showerror('Error', 'Not enough numbers\nIn serial numbers\nPlease check.. ')


    def check_input_in_sec_out_new_som_db (self):
            with sqlite3.connect('Kazuar_tester_PC.db') as self.db:
                self.c = self.db.cursor( )
            find_user = 'SELECT SN FROM sec_in_input_user_db WHERE SN = ?'
            self.c.execute(find_user, [(self.board_sn_sec_out.get( ))])
            if not self.c.fetchall( ):
                messagebox.showerror('Error!', f'{self.board_sn_sec_out.get()}\nnot burn yet!\nPlease burn Secure Input first!')
            else:
                self.check_input_in_new_som_db( )

    def check_input_in_new_som_db (self):
            with sqlite3.connect('Kazuar_tester_PC.db') as self.db:
                self.c = self.db.cursor( )
                self.c1 = self.db.cursor( )
                self.c2 = self.db.cursor( )
            find_data = 'SELECT * FROM sec_out_input_user_db WHERE SN_SOM_Board = ? and SN_Kazuar_Board = ?'
            self.c.execute(find_data, [(self.som_sn_sec_out.get( )), (self.board_sn_sec_out.get( ))])
            find_data1 = 'SELECT * FROM sec_out_input_user_db WHERE SN_Kazuar_Board = ?'
            self.c1.execute(find_data1, [(self.board_sn_sec_out.get( ))])
            find_data2 = 'SELECT * FROM sec_out_input_user_db WHERE SN_SOM_Board = ?'
            self.c2.execute(find_data2, [(self.som_sn_sec_out.get( ))])
            if self.c.fetchall( ):
                messagebox.showerror('Error!',
                                     f'Kazuar Board-{self.board_sn_sec_out.get( )} and\nSOM-{self.som_sn_sec_out.get( )}\n'
                                     f'already burned!\nTry a different ones.')
            elif self.c1.fetchall( ):
                messagebox.showerror('Error!', f'Kazuar Board- {self.board_sn_sec_out.get( )}\nalready burned!\nTry a '
                                               f'different one.')
            elif self.c2.fetchall( ):
                messagebox.showerror('Error!',
                                     f'SOM- {self.som_sn_sec_out.get( )}\nalready burned!\nTry a different one.')
            else:
                self.connect_board_sec_out( )
    

#####################################################################################################################
####################################################################################################################


class automation_test:
    def __init__(self, master=None, app_automation_test=None):

        self.frame_anti_tamper = None
        self.text_result = None
        self.root_anti_tamper_database_query = None
        self.off_1 = None
        self.render2 = None
        self.load2 = None
        self.render = None
        self.load = None
        self.c1 = None
        self.off_2 = None
        self.last_line = None
        self.title2 = None
        self.log_f_2 = None
        self.next_log_f_2 = None
        self.off = None
        self.title = None
        self.log_f = None
        self.next_log_f = None
        self.title1 = None
        self.log_f_1 = None
        self.next_log_f_1 = None
        self.c = None
        self.conn = None
        self.c = None
        self.root_sec_in_database_query = None
        self.button = None
        self.img = None
        self.master = master
        self.user_enter = StringVar()
        self.sn = StringVar()
        self.ip = StringVar()
        self.time_now = time.strftime("%D %H:%M:%S")
        self.rev = StringVar()
        self.ODM = StringVar()
        self.host_name = StringVar()
        self.EMS = 'Chayun'
        self.Processor_GEN = '10'
        self.Processor = 'i7'
        self.DDR_Size = '16G'
        self.Screen_Model = 'AOU'
        self.Keyboard_Configuration = 'QWERTY'
        self.Switching_Board = '1.1'
        self.Kazuar_Board = '3.1'
        self.SOM = '1.9'
        self.Kazuar_Laptop_Model = F'KB_CL{self.Processor_GEN}_KB{self.Kazuar_Board}'
        self.SecIn_Version = '0.0.12'
        self.SecOut_Version = '0.1.14'
        self.AT_Version = '0.0.8'
        self.app_automation_test = app_automation_test
        self.conn = sqlite3.connect('Kazuar.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user')
        self.user_enter = self.c.fetchall()[0][0]

        self.frame_automation_test = tk.Frame(self.master, bg='light sky blue')
        self.title_aut = Frame(self.frame_automation_test, padx=10, bg="light sky blue")
        self.log_f_aut = Frame(self.frame_automation_test, padx=10, pady=65, bg="light sky blue")
        self.next_log_f_aut = Frame(self.frame_automation_test, padx=300, bg="light sky blue",
                                highlightbackground='blue', highlightthickness=20, highlightcolor='blue', )

        left_label = Label(self.title_aut, bg="light sky blue", text="Automation Test", font=LARGE_FONT_button_title)
        left_label.pack(fill=X)

        Label(self.log_f_aut, text="ODM S/N", font=LARGE_FONT_button1, bg="light sky blue").grid(padx=650)
        Entry(self.log_f_aut, textvariable=self.sn, font=LARGE_FONT_button1, width=13).grid(padx=650)
        Label(self.log_f_aut, text="IP address", font=LARGE_FONT_button1, bg="light sky blue").grid(padx=650)
        Entry(self.log_f_aut, textvariable=self.ip, font=LARGE_FONT_button1, width=13).grid(padx=650)
        Label(self.log_f_aut, text="Host Name", font=LARGE_FONT_button1, bg="light sky blue").grid(padx=650)
        Entry(self.log_f_aut, textvariable=self.host_name, font=LARGE_FONT_button1, width=7).grid(padx=650)

        Label(self.log_f_aut, text="Kazuar Board Rev", font=LARGE_FONT_button, bg="light sky blue").grid(padx=650, pady=10)
        options = ("2x".split())
        ##2x
        menu = OptionMenu(self.log_f_aut, self.rev, *options)
        menu.config(font=LARGE_FONT_button)
        self.rev.set("2x")
        menu.grid()

        Label(self.log_f_aut, text="Platform Model", font=LARGE_FONT_button, bg="light sky blue").grid(padx=650, pady=20)
        options = ("Clevo Gen3".split())
        menu_odm = OptionMenu(self.log_f_aut, self.ODM, *options)
        menu_odm.config(font=LARGE_FONT_button)
        self.ODM.set("Clevo")
        menu_odm.grid()

        Button(self.next_log_f_aut, text="Start\nTest", bg="green", fg="white", font=FONT,
               command=self.cmd_automation, bd=12).grid(row=2, column=0, padx=200, ipadx=100, pady=20)
        Label(self.next_log_f_aut, text="", bg="light sky blue").grid(row=2, column=1, padx=100)
        Button(self.next_log_f_aut, text="Menu", bg="red", fg="white", font=FONT,
               command=self.go_back_aut, bd=12).grid(row=2, column=2, padx=450, ipadx=100, ipady=30, pady=20)

        self.title_aut.pack()
        self.log_f_aut.pack(pady=10, ipady=10)
        self.next_log_f_aut.pack(ipadx=1000)

    def start_page_automation_test (self):
        self.frame_automation_test.pack()

    def go_back_aut (self):
        self.frame_automation_test.pack_forget()
        self.app_automation_test.menu_page()

    def cmd_automation (self):
        if self.sn.get() == "" or self.ip.get() == "" or self.host_name.get() == "":
            messagebox.showerror("error", "Missing Data!")
        else:
            import os
            # -iptables -I INPUT 1 -p icmp --icmp-type echo-request -j ACCEPT
            os.system("gnome-terminal  --geometry=500x500+100+200 "
                      " --working-directory=/home/tester/workspace/automation/tests_collection "
                      "/hw_production_tests "
                      f" -- bash -c \" sudo -S pytest -v -m hardware_rev{self.rev.get()}"
                      f" --wifi_ip={self.ip.get().upper()} "
                      f"--html='/home/tester/Test_Results_Aoutomation/{self.host_name.get().upper()} - {self.time_now}.html'"
                      f"--self-contained-html"
                      f" --capture=tee-sys -rP -rF; "
                      "exec bash\"")
            if os.getcwd():
                self.submit()
                self.sn.set("")
                self.ip.set("")
                self.host_name.set("")

            # Create Submit Function For database
    def submit (self):
        # Create a database or connect to one
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        # Insert Into Table
        self.c.execute("INSERT INTO database_automation VALUES (:Date, :User, :EMS, :ODM_SN, :Platform_Model, "
                  ":Processor_GEN, "
                  ":Processor, :DDR_Size, :Screen_Model, :Keyboard_Configuration, :Switching_Board, "
                  ":Kazuar_Board, :SOM, :Kazuar_Laptop_Model, :Kazuar_Laptop_SN, :SecIn_Version, :SecOut_Version, "
                  ":AT_Version)",
                  {
                      'Date': self.time_now,
                      'User': self.user_enter,
                      'EMS': self.EMS,
                      'ODM_SN': self.sn.get().upper(),
                      'Platform_Model': self.ODM.get().upper(),
                      'Processor_GEN': self.Processor_GEN,
                      'Processor': self.Processor,
                      'DDR_Size': self.DDR_Size,
                      'Screen_Model': self.Screen_Model,
                      'Keyboard_Configuration': self.Keyboard_Configuration,
                      'Switching_Board': self.Switching_Board,
                      'Kazuar_Board': self.Kazuar_Board,
                      'SOM': self.SOM,
                      'Kazuar_Laptop_Model': self.Kazuar_Laptop_Model,
                      'Kazuar_Laptop_SN': self.host_name.get().upper(),
                      'SecIn_Version': self.SecIn_Version,
                      'SecOut_Version': self.SecOut_Version,
                      'AT_Version': self.AT_Version
                  })
        self.conn.commit()
        self.conn.close()
        self.sn.set("")
        self.ip.set("")
        self.host_name.set("")