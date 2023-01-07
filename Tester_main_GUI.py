import tkinter as tk
import tkinter as ttk
from tkinter import *
from tkinter import messagebox, StringVar
import time
from Kazuar_pages_GUI import secin, sec_out, anti_tamper, database_secin, database_sec_out,\
    database_anti_tamper, database_automation_test, automation_test
import sqlite3
from PIL import ImageTk, Image

user = ("Calibri", 10, 'bold')
FONT = ("Calibri", 19, 'bold')
LARGE_FONT = ("Calibri", 19, 'bold')
LARGE_FONT_button_title = ("Calibri", 50, 'bold')
LARGE_FONT_button = ("Calibri", 22, 'bold')
LARGE_FONT_button1 = ("Calibri", 25, 'bold')
LARGE_FONT_button_next = ("Calibri", 15, 'bold')
conn=sqlite3.connect('Kazuar.db')
c=conn.cursor()
c.execute('SELECT * FROM user')
user_enter=c.fetchall()[0][0]
print('User:' + user_enter)

with sqlite3.connect('Kazuar.db') as db:
    c = db.cursor()

class App:

    c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY,password TEX NOT NULL);')

    db.commit()
    db.close()
    def __init__(self, root_start=None):
        # self.page_1 = None
        self.bind = None
        self.entry = None
        self.enter_user = None
        self.c = None
        self.result_name = None
        self.result = None
        self.user_cosed = None
        self.username = StringVar()
        self.n_username = StringVar()
        self.password = StringVar()
        self.n_password = StringVar()
        self.user_enter = None
        self.enter = None
        self.root = root_start
        self.frame = tk.Frame(self.root, bg='black')
        self.frame.pack()


    # def widgets (self):
        self.title = Frame(self.frame, padx=10, pady=20, bg="black")
        self.logf = Frame(self.frame, padx=10, pady=20, bg="black")
        self.next_logf = Frame(self.frame, padx=10, pady=100, bg="black")
        self.query_logf = Frame(self.frame, padx=10, bg="black")
        self.next1_logf = Frame(self.frame, padx=10, bg="black")
        self.enter = ImageTk.PhotoImage(
            Image.open("/Capture3.PNG"))
        self.label = Label(self.title, image=self.enter, borderwidth=0, bg='black', relief="flat")
        self.label.pack()

        Label(self.logf, text='Username: ', font=LARGE_FONT_button, bg="black",
              fg="white").grid(pady=5, padx=25, sticky=W)
        Entry(self.logf, textvariable=self.username, bd=6, font=LARGE_FONT_button).grid(row=0, column=1,
                                                                            pady=10)
        Label(self.logf, text=' Password: ', font=LARGE_FONT_button, bg="black",
              fg="white").grid(sticky=W, pady=5, padx=25)
        self.entry = e  = tk.Entry(self.logf, textvariable=self.password, bd=6, font=LARGE_FONT_button, show="*")
        e.grid(row=1, column=1)
        e.bind("<Key>", self.entry_pass1)

        self.eye = ImageTk.PhotoImage(
            Image.open("/home/tester/PycharmProjects/GUI_production_kazuar/image/eye.png"))
        self.button_eye = Button(self.logf, image=self.eye, relief="flat", command=self.entry_pass1)
        self.button_eye.grid(row=1, column=1, ipadx=10, ipady=10, sticky=E)



        self.LOGIN_BUT = Button(self.next_logf, text=' Login ', bd=12, font=LARGE_FONT_button_next, command=self.login, bg="green",
               fg="white")
        self.LOGIN_BUT.grid(row=2, column=0, padx=60, ipadx=100, ipady=20)
        # self.LOGIN_BUT.bind('<Return>',self.login)

        self.Create = Button(self.next_logf, text=' Create Account ', bd=12, font=LARGE_FONT_button_next, command=self.cr,
               bg="#0059b3", fg="white")
        self.Create.grid(row=2, column=1, columnspan=2, padx=20, ipady=20)
        # self.Create.bind('<Return>',self.cr)

        self.users = Button(self.query_logf, text='User list', bd=12, font=LARGE_FONT_button_next,
               command=self.acsess, bg="orange", fg="white")
        self.users.grid(row=4, column=2, padx=50, ipady=20, ipadx=50)
        # self.users.bind('<Return>',self.acsess)

        self.logout_general = Button(self.query_logf,text= 'LogOut',bd=12,font=LARGE_FONT_button_next,
                                     command=self.exit_application,bg="red",fg="white")
        self.logout_general.grid(row=4, column=1, padx=100, ipady=20,ipadx=50)
        # self.logout_general.bind('<Return>',self.exit_application)


        self.title.pack()
        self.logf.pack()
        self.next_logf.pack()
        self.next1_logf.pack()
        self.query_logf.pack()

        self.crf = Frame(self.frame, padx=10, pady=50, bg="black")
        self.crf1 = Frame(self.frame, padx=10, pady=10, bg="black")
        Label(self.crf, text='Username: ', font=LARGE_FONT_button, bg="black",
              fg="white").grid(pady=5, padx=5, sticky=W)
        Entry(self.crf, textvariable=self.n_username, bd=6, font=LARGE_FONT_button).grid(row=0, column=1,
                                                                                         pady=20)
        Label(self.crf, text='Password: ', font=LARGE_FONT_button, pady=5, padx=7, bg="black",
              fg="white").grid(pady=5, padx=7, sticky=W)
        self.entry1 = e1 = tk.Entry(self.crf, textvariable=self.n_password, bd=5, font=LARGE_FONT_button, show="*")
        e1.grid(row=1, column=1)
        e1.bind("<Return>", self.entry_pass2)
        self.eye1 = ImageTk.PhotoImage(
            Image.open("/eye.png"))
        self.button_eye1 = Button(self.crf, image=self.eye1, relief="flat", command=self.entry_pass2)
        self.button_eye1.grid(row=1, column=1, ipadx=10, ipady=10, sticky=E)

        Button(self.crf1, text='Create\nNew Account', bd=12, font=LARGE_FONT_button_next,
               command=self.check_input,
               bg="green", fg="white").grid(row=0, column=0, pady=10, padx=100)
        Button(self.crf1, text='Back to\nLogin', bd=12, font=LARGE_FONT_button_next,
               command=self.refresh, bg="#0059b3", fg="white").grid(row=0, column=1, pady=10, padx=100,
                                                                    ipadx=30)

        self.page_1 = Page_1(master=self.root, app=self)

        # function before system log-out #
    @classmethod
    def exit_application (self):
        restart_msg=tk.messagebox.askquestion('Exit Application','Are you sure do you want to LogOut? ',
                                              icon = 'warning')
        if restart_msg == 'no':
            pass
        else:
            exit()
    def entry_pass1 (self):
        self.entry.config(show='')
        # Hide text after 1000 milliseconds
        self.entry.after(1000, lambda: self.entry.config(show='*'))

    def entry_pass2 (self):
        self.entry1.config(show='')
        # Hide text after 1000 milliseconds
        self.entry1.after(1000, lambda: self.entry1.config(show='*'))

    def main_page(self):
        self.frame.pack()

    def make_page_1(self):
        self.page_1 = Page_1(master=self.root, app=self)

        self.frame.pack_forget()
        self.page_1.start_page()
        self.username.set('')
        self.password.set('')


    def new_1(self):
        root_query_LOGIN.destroy()
        self.back_to_home()

    def new (self):
        root_Delete.destroy()
        self.back_to_home()
    def back_to_home(self):
        self.crf.pack_forget()
        self.crf1.pack_forget()
        self.username.set('')
        self.password.set('')
        self.title.pack()
        self.logf.pack()
        self.next_logf.pack()
        self.query_logf.pack()
        self.next1_logf.pack()


    def acsess (self):
        global fontStyle
        global fontStyle1
        global fontStyle2
        global root_query_
        global app_width, app_height, screen_width, screen_height, x, y
        root_query_LOGIN = Tk()
        root_query_LOGIN.title("Access Permission")
        root_query_LOGIN.config(bg="sky blue")
        global entry1
        global entry2
        global login
        global clock

        login = Label(root_query_LOGIN, text="Access permission", bg="sky blue", fg='black', relief=RAISED)
        login.pack(ipady=5, fill='x')

        def new_clock ():
            hour = time.strftime("%H")
            minute = time.strftime("%M")
            second = time.strftime("%S")
            am_pm = time.strftime("%p")

            clock_label.config(text=hour + ":" + minute + ":" + second + " " + am_pm)
            clock_label.after(1000, new_clock)

        clock_label = Label(root_query_LOGIN, text="", font=LARGE_FONT_button_next, fg="black", bg="sky blue")
        clock_label.pack(side=TOP, pady=10)

        new_clock()

        def check_input_list ():
            global button_query_accesses
            password_1 = "*"

            entered_password = password_entry.get()

            if entered_password == password_1:

                button_query_accesses = Button(root_query_LOGIN,
                                               text="Show\nList",
                                               command=self.query_accesses, bg="#0059b3", fg="white",
                                               font=LARGE_FONT_button_next,
                                               width=15, borderwidth=10)
                button_query_accesses.pack()
                password_entry.delete(0, END)

            else:
                anser_failed = Label(root_query_LOGIN, text="Login failed:\nInvalid username or password",
                                     bg="sky blue",
                                     fg="black",
                                     font=2)
                anser_failed.pack()

        password_frame = Frame(root_query_LOGIN, bg="sky blue")
        password_frame.pack()

        Label(password_frame, text="Password", bg="sky blue", font=1, fg="black").pack(side='left', padx=7)
        password_entry = Entry(password_frame, show="*", bd=3)
        password_entry.pack(side='right')

        go_button = Button(root_query_LOGIN, text="login!", command=check_input_list, bg="#0059b3", fg="white",
                           width=15,
                           font=1)
        go_button.pack(pady=15)

        bottom_frame = Frame(root_query_LOGIN, bg="sky blue")
        bottom_frame.pack()
        anser_login = Label(root_query_LOGIN, text="", bg="sky blue")
        anser_login.pack()

    def check_input (self):
        if self.n_username.get() == "" or self.n_password.get() == "":
            msg_box = tk.messagebox.showerror('Stop!!',
                                             'Missing username or password\nPlease check! ')
            if msg_box == 'ok':
                pass
        else:
            msg_box = tk.messagebox.askquestion('Warning', 'Are you sure about the\nUsername and Password? ',
                                               icon='warning')
            if msg_box == 'yes':
                self.new_user()
            else:
                tk.messagebox.showinfo('Return', 'You will now return to the application screen')


    def login (self):
        with sqlite3.connect('Kazuar.db') as self.db:
            self.c = self.db.cursor()
        find_user = 'SELECT * FROM user WHERE username = ? and password = ?'
        self.c.execute(find_user, [(self.username.get()), (self.password.get())])
        self.result = self.c.fetchall()
        if self.result:
            self.make_page_1()

        else:
            messagebox.showerror('Error','User Name or Password\nIncorrect!\nPlease Try again.. ')
            print("no connection ")


    def new_user(self):
        global c, db
        with sqlite3.connect('Kazuar.db') as db:
            c = db.cursor()
        c.execute('DELETE from user')
        print('we deleted', c.rowcount, 'records from the table.')

        find_user = 'SELECT username FROM user WHERE username = ?'
        c.execute(find_user, [(self.n_username.get())])

        if c.fetchall():
            ms.showerror('Error!', 'Username is already taken, try a different one.')
        else:
            insert = 'INSERT INTO user(username,password) VALUES(?,?)'
            c.execute(insert, [(self.n_username.get()), (self.n_password.get())])

            db.commit()
            # self.head.pack_forget()
            self.crf.pack_forget()
            self.crf1.pack_forget()
            self.back_to_home()

    @staticmethod
    def query_accesses():
        global root_query_accesses, c, record, records
        global db, record_id, query_label, print_records_secure, button_query_accesses
        global app_width, app_height, screen_width, screen_height, x, y
        button_query_accesses.pack_forget()
        db = sqlite3.connect('Kazuar.db')
        c = db.cursor()
        c.execute("SELECT *, oid FROM user")
        records = c.fetchall()
        root_query_accesses = Tk()
        root_query_accesses.attributes('-zoomed', True)
        root_query_accesses.config(bg='black')
        root_query_accesses.title(' Users details ')
        main_frame = Frame(root_query_accesses)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame, bg='black')
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        print_records_secure = ''
        for record in records:
            print_records_secure += "USERNAME: " + str(record[0]) + " , " + "PASSWORD: " + str(
                '*#*#*#*#*#*#*#*#') + "   " + "[" + str(record[2]) + "]" + "\n"

        query_label = Label(second_frame, text=str(print_records_secure), bg="sky blue", fg="black",
                            font=('calibri', 18, 'bold'))
        query_label.grid()
        record_id = record[2]
        root_query_accesses.mainloop()
        db.commit()

        db.close()

    def refresh(self):
        self.crf.pack_forget()
        self.crf1.pack_forget()
        self.back_to_home()

    def log(self):

        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.crf1.pack_forget()
        self.logf.pack()
        self.next1_logf.pack()

    def cr(self):
        self.query_logf.pack_forget()
        self.next1_logf.pack_forget()
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.next_logf.pack_forget()
        # self.head['text'] = 'Create New Account'
        self.crf.pack()
        self.crf1.pack()

class Page_1:


    def __init__(self, master=None, app=None):
        self.reset_button = None
        self.search_button = None
        self.som_button = None
        self.var1 = None
        self.kb_button = None
        self.var2 = None
        self.records1 = None
        self.records = None
        self.c1 = None
        self.automation_test = None
        self.Console = None
        self.database_automation_test = None
        self.user_enter = None
        self.conn = None
        self.c = None
        self.result = None
        self.database_anti_tamper = None
        self.database_sec_out = None
        self.TESTER = None
        self.root_all_database_query = None
        self.databases_secin = None
        self.database_secin = None
        self.username = StringVar()
        self.n_username = StringVar()
        self.password = StringVar()
        self.n_password = StringVar()
        self.master = master
        self.root = root
        self.app = app
        self.frame_app = tk.Frame(self.master, bg='black')
        self.board_sn_search = StringVar()
        self.som_sn_sec_out_search = StringVar()
        self.username = StringVar()

        self.title = Frame(self.frame_app, padx=10, bg="black")
        self.log_f_right = Frame(self.frame_app, padx=10, bg="black")
        self.log_f_left = Frame(self.frame_app, padx=10, bg="black")
        self.log_f_center = Frame(self.frame_app, bg="black")
        self.next_log_f = Frame(self.frame_app, bg="black")
        self.img = ImageTk.PhotoImage(
            Image.open("/home/tester/PycharmProjects/GUI_production_kazuar/image/Capture3.PNG"))
        self.button = Label(self.title, image=self.img, borderwidth=0, bg='black', relief="flat")
        self.button.grid(row=0, column=0, sticky=N)
        Label(self.title, text='Kazuar Production', font=LARGE_FONT_button_title, bg="black",
              fg="white").grid(row=1, column=0, sticky=N)

        self.secin_but = Button(self.log_f_left, text="Burning\nSecure Input", font=LARGE_FONT_button, bg="white", bd=12,
               command=self.secin_page, highlightbackground='blue',
               highlightthickness=10)
        self.secin_but.grid(row=0, column=0, padx=25, sticky=N, pady=20, ipadx=60)
        self.AT_but = Button(self.log_f_left, text="Burning\nAnti-Tamper", font=LARGE_FONT_button, bg="white", bd=12,
               command=self.anti_tamper_page, highlightbackground='blue',
               highlightthickness=10)
        self.AT_but.grid(row=1, column=0, padx=25, sticky=N, pady=20, ipadx=70)
        self.secout_but = Button(self.log_f_left, text="Burning\nSecure Output", font=LARGE_FONT_button, bg="white", bd=12,
               command=self.sec_out_page, highlightbackground='blue',
               highlightthickness=10)
        self.secout_but.grid(row=2, column=0, padx=25, sticky=N, pady=20, ipadx=30)
     
        ####################################################################################################
        self.automation_but = Button(self.log_f_right, text="Automation\nTest", font=LARGE_FONT_button, bg="white", bd=12,
               command=self.test_for_automation, highlightbackground='blue',
               highlightthickness=10)
        self.automation_but.grid(row=1, column=0, padx=25, sticky=N, pady=20, ipadx=105)
        self.iso_but = Button(self.log_f_right, text="ISO\nBaseOs", font=LARGE_FONT_button, bg="white", bd=12,
               command='', highlightbackground='blue',
               highlightthickness=10)
        self.iso_but.grid(row=0, column=0, padx=25, sticky=N, pady=20, ipadx=180)

        self.db_but = Button(self.log_f_right, text="Data\nBases", font=LARGE_FONT_button, bg="white", bd=12,
               command=self.check_password_for_all_database, highlightbackground='blue',
               highlightthickness=10)
        self.db_but.grid(row=2, column=0, padx=25, sticky=N, pady=20, ipadx=200)
        Label(self.log_f_center, bg="black", fg='white',
              text='Hi\n' + str(user_enter), font=user).grid(row=0, column=0)
        self.search = ImageTk.PhotoImage(
            Image.open("/home/tester/PycharmProjects/GUI_production_kazuar/image/search_gui_1.png"))
        self.button_search = Button(self.log_f_center,image=self.search,command=self.search_root_page,bd=10, highlightbackground='blue',
               highlightthickness=10)
        self.button_search.grid(row=1, column=0, pady=50)

        self.LogOut = Button(self.next_log_f, text="LogOut", font=LARGE_FONT_button, bg="red", bd=12,
               command=self.go_back, highlightbackground='blue', highlightthickness=10)
        self.LogOut.pack(ipadx=150, ipady=20, pady=50)

        self.title.pack()
        self.log_f_left.pack(side=LEFT)
        self.log_f_right.pack(side=RIGHT)

        self.next_log_f.pack(side=BOTTOM, ipadx=20)
        self.log_f_center.pack(side=BOTTOM, pady=100)
        self.secin = secin(master=self.root, app_sec_in=self)
        self.sec_out = sec_out(master=self.root, app_sec_out=self)
        self.anti_tamper = anti_tamper(master=self.root, app_anti_tamper=self)

        # self.secin_but.bind('<Key>',self.secin_page)
        # self.secout_but.bind('<Key>',self.sec_out_page)
        # self.AT_but.bind('<Key>',self.anti_tamper_page)
        #
        # self.automation_but.bind('<Key>',self.test_for_automation)
        # # self.iso_but.bind('<Return>',self.sec_out_page)
        # self.button_search.bind('<Key>',self.search_root_page)
        # self.db_but.bind('<Key>',self.permission_for_database)
        # self.LogOut.bind('<Key>',self.go_back)

        # menu database page
        ####################################################################################################
        self.title_menu_db = Frame(self.frame_app,bg="light sky blue")

        self.log_f_menu_db = Frame(self.frame_app,bg="light sky blue")
        self.next_log_f_menu_db = Frame(self.frame_app, bg="light sky blue",
                                    highlightbackground='blue', highlightthickness=20, highlightcolor='blue')
        left_label = Label(self.title_menu_db,bg="light sky blue",text="Kazuar\nProduction DataBases",
                           font=LARGE_FONT_button_title)
        left_label.pack(fill="x", ipadx=500)
        Button(self.log_f_menu_db,text="Search\nSerial Number",font=LARGE_FONT_button,bg="white",bd=12,
               command=self.search_sn_page,highlightbackground='blue',
               highlightthickness=10).grid(row=0,column=0,padx=1000,sticky=N,pady=100, ipadx=50)
        Button(self.log_f_menu_db,text="Data\nBases",font=LARGE_FONT_button,bg="white",bd=12,
               command=self.permission_for_database,highlightbackground='blue',
               highlightthickness=10).grid(row=1,column=0,padx=1000,sticky=N,pady=20,ipadx=190)

        Button(self.next_log_f_menu_db,text="Menu",bg="red",fg="white",font=FONT,
               command=self.go_back1,bd=12).grid(row=4,column=0,ipady=30,pady=10, ipadx=130, padx=1080)

        # left database menu
        ###############################################################################
        self.frame_database = tk.Frame(self.master, bg="light sky blue")
        self.title_db = Frame(self.frame_app, bg="light sky blue")

        self.log_f_left_db = Frame(self.frame_app, bg="light sky blue")


        left_label = Label(self.title_db, bg="light sky blue", text="Kazuar\nProduction DataBases",
                           font=LARGE_FONT_button_title)
        left_label.pack(fill="x")
        self.si_butt = Button(self.log_f_left_db, text='Security Input\nDataBases', bd=12, command=self.database_secin_page,
               font=FONT)
        self.si_butt.grid(row=0, column=0, ipady=10, pady=20, ipadx=30, padx=1000)
        self.so_butt = Button(self.log_f_left_db, text='Security Output\nDataBases', bd=12, command=self.database_sec_out_page,
               font=FONT)
        self.so_butt.grid(row=1, column=0, ipady=10, pady=20, padx=1000)
        self.at_butt = Button(self.log_f_left_db, text='Anti-Tamper\nDataBases', bd=12, command=self.database_anti_tamper_page,
               font=FONT)
        self.at_butt.grid(row=2, column=0, ipady=10, pady=20, ipadx=45, padx=1000)
        self.aut_but = Button(self.log_f_left_db, text='Automation\nDataBases', bd=12,
               command=self.database_automation_test_page,
               font=FONT)
        self.aut_but.grid(row=3, column=0, ipady=10, pady=20, ipadx=54, padx=1000)

        Button(self.log_f_left_db,text="Menu",bg="red",fg="white",font=FONT,
               command=self.go_back1,bd=12).grid(row=4, column=0, ipady=30, pady=50, ipadx=140, padx=1000)
        # right search kazuar board
        #########################################################################################
        self.title_search_sn = Frame(self.frame_app,bg="light sky blue")
        self.log_f_search_sn= Frame(self.frame_app,bg="light sky blue")
        self.log_f_next_search_sn= Frame(self.frame_app,bg="light sky blue")
        self.next_log_f_search_sn = Frame(self.frame_app, bg="light sky blue",
                                    highlightbackground='blue', highlightthickness=20, highlightcolor='blue')
        left_label = Label(self.title_search_sn,bg="light sky blue",text="Kazuar\nProduction DataBases",
                           font=LARGE_FONT_button_title)
        left_label.pack(fill="x")
        Label(self.log_f_search_sn,text='Search\nSerial Number\n(Select K.B or SOM)\n____________________ ',font=FONT,
              bg='light sky blue'). \
            grid(row=0,column=0,columnspan=2,ipady=10,pady=50,ipadx=50,padx=950)
        self.var1 = IntVar()
        self.kb_button = Checkbutton(self.log_f_next_search_sn,text="K.B",variable=self.var1,font=FONT,
                                     bg='light sky blue',bd=10,onvalue=1,offvalue=0,width=5,
                                     highlightcolor='light sky blue',highlightbackground='light sky blue',
                                     highlightthickness=3,command=self.search_var,indicatoron=OFF)
        self.kb_button.grid(row=1,column=0,pady=10, padx=20)
        self.var2 = IntVar()
        self.som_button = Checkbutton(self.log_f_next_search_sn,text="SOM",variable=self.var2,font=FONT,
                                      bg='light sky blue',bd=10,onvalue=1,offvalue=0,width=5,
                                      highlightcolor='light sky blue',highlightbackground='light sky blue',
                                      highlightthickness=3,command=self.search_var,indicatoron=OFF)
        self.som_button.grid(row=1,column=1,pady=10)
        Entry(self.log_f_next_search_sn,textvariable=self.board_sn_search,bd=10,
              font=LARGE_FONT_button).grid(row=2,column=0,columnspan=2,pady=50, padx=850)
        self.board_sn_search.set('NS-KB31-R01-XXXXXXXX')
        Entry(self.log_f_next_search_sn,textvariable=self.som_sn_sec_out_search,bd=10,
              font=LARGE_FONT_button,width=13).grid(row=3,column=0,columnspan=2,pady=30, padx=850)
        self.som_sn_sec_out_search.set('F8DC7AXXXXXX')

        self.search_button = Button(self.next_log_f_search_sn,text='Search',bd=10,font=LARGE_FONT_button,
                                    command=self.search_serial_number)
        self.search_button.grid(row=4,column=0,ipady=30,ipadx=130, padx=150)

        Button(self.next_log_f_search_sn,text="Menu",bg="red",fg="white",font=FONT,
               command=self.go_back1,bd=12).grid(row=4,column=1,ipady=30,ipadx=130, padx=180)

        self.search_button = Button(self.next_log_f_search_sn,text='Reset',bd=10,font=LARGE_FONT_button,
                                    command=self.reset_search)
        self.search_button.grid(row=4,column=2,ipady=30,ipadx=130, padx=150)
        # page search serial number
        ################################################################################################



        self.si_butt.bind("<Enter>", self.on_enter)
        self.so_butt.bind("<Enter>", self.on_enter)
        self.at_butt.bind("<Enter>", self.on_enter)
        self.aut_but.bind("<Enter>", self.on_enter)

        self.si_butt.bind("<Leave>", self.on_leave)
        self.so_butt.bind("<Leave>", self.on_leave)
        self.at_butt.bind("<Leave>", self.on_leave)
        self.aut_but.bind("<Leave>", self.on_leave)


    def search_root_page(self, event):
        self.title.pack_forget()
        self.log_f_left.pack_forget()
        self.log_f_right.pack_forget()
        self.next_log_f.pack_forget()
        self.log_f_center.pack_forget()
        self.title_menu_db.pack(ipadx=500)
        self.log_f_menu_db.pack(ipadx=500, ipady=140)
        self.next_log_f_menu_db.pack(ipadx=1000)

    def search_sn_page(self, event):
        self.title_menu_db.pack_forget()
        self.log_f_menu_db.pack_forget()
        self.next_log_f_menu_db.pack_forget()
        self.title_search_sn.pack(ipadx=500)
        self.log_f_search_sn.pack(ipadx=500)
        self.log_f_next_search_sn.pack(ipadx=500, ipady=50)
        self.next_log_f_search_sn.pack(ipadx=1000)

    def reset_search(self, event):
        self.var1.set(0)
        self.var2.set(0)
        self.som_button['state'] = NORMAL
        self.som_button['background'] = 'light sky blue'
        self.som_button['highlightbackground'] = 'light sky blue'

        self.kb_button['state'] = NORMAL
        self.kb_button['background'] = 'light sky blue'
        self.kb_button['highlightbackground'] = 'light sky blue'


    def search_var(self):
        if self.var1.get() == 0 and self.var2.get() == 0:
            messagebox.showerror('error', 'must to select SOM or KB!\nPlease select..')
        elif self.var1.get() == 1:
            self.som_button['state'] = DISABLED
            self.som_button['highlightbackground'] = 'light sky blue'
            self.kb_button['bg'] = 'green'
            print('var 1')

        elif self.var2.get() == 1:
            self.kb_button['state'] = DISABLED
            self.kb_button['highlightbackground'] = 'light sky blue'

            self.som_button['bg'] = 'green'
            print('var 2')
        else:
            pass
    def search_serial_number(self, event):
        if self.var1.get() == 0 and self.var2.get() == 0:
            messagebox.showerror('error', 'Must to select SOM or K.B!\nPlease select..')
        elif self.var1.get() == 1:
            if self.board_sn_search.get() == '':
                messagebox.showerror('error','please enter\nKB serial number')
            elif self.board_sn_search.get():
                with sqlite3.connect('Kazuar_tester_PC.db') as self.db:
                    self.c = self.db.cursor()
                    self.c1 = self.db.cursor()
                find_data = 'SELECT * FROM sec_out_input_user_db WHERE SN_Kazuar_Board = ?'
                self.c.execute(find_data,[(self.board_sn_search.get())])
                # complete process si and so
                find_data1 = 'SELECT * FROM sec_in_input_user_db WHERE SN = ?'
                self.c1.execute(find_data1,[(self.board_sn_search.get())])
                self.records = self.c1.fetchall()

                if self.c.fetchall():
                    messagebox.showinfo('Board info!',
                                         f'Kazuar Board-{self.board_sn_search.get()}\n'
                                         f'Completed process:\nSecure Input\nAnti-tamper\nSecure Output ')
                elif self.records:

                    for self.record in self.records:
                        if self.record[3] == 'NO':
                            print('status fail')
                            messagebox.showerror('Error',
                                                 f'{self.board_sn_search.get()}\nFailed in Secure Input burning!\n'
                                                 f'Try a different one ')
                        else:
                            messagebox.showinfo('Board info!',
                                                f'Kazuar Board- {self.board_sn_search.get()}\nAlready burned!\nTry a '
                                                f'different one.')
                else:
                    messagebox.showinfo('Board info!',
                                        f'Kazuar Board- {self.board_sn_search.get()}\nNot burned yet!\nTry a '
                                        f'different one.')

        elif self.var2.get() == 1:
            if self.som_sn_sec_out_search == '':
                messagebox.showerror('error','please enter\nSOM serial number')
            elif self.som_sn_sec_out_search.get():
                with sqlite3.connect('Kazuar_tester_PC.db') as self.db:
                    self.c2 = self.db.cursor()
                find_data = 'SELECT * FROM sec_out_input_user_db WHERE SN_SOM_Board = ?'
                self.c2.execute(find_data,[(self.som_sn_sec_out_search.get())])
                if self.c2.fetchall():
                    messagebox.showinfo('Board info!',
                                             f'SOM- {self.som_sn_sec_out_search.get()}\nAlready burnt!\nTry a different one.')
                else:
                    messagebox.showinfo('Board info!',
                                            f'Kazuar Board- {self.som_sn_sec_out_search.get()}\nNot burned yet!\nTry a '
                                            f'different one.')
            else:
                pass


    def on_enter (self, e):
        self.si_butt['background'] = 'blue'
        self.so_butt['background'] = 'blue'
        self.at_butt['background'] = 'blue'
        self.aut_but['background'] = 'blue'

    def on_leave (self, e):
        self.si_butt['background'] = 'white'
        self.so_butt['background'] = 'white'
        self.at_butt['background'] = 'white'
        self.aut_but['background'] = 'white'

    def permission_for_database(self):
        self.conn = sqlite3.connect('Kazuar.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user')
        self.user_enter = self.c.fetchall()[0][1]
        print('User:' + str(self.user_enter))
        if self.user_enter == 'kazuarblue1':
            self.all_databases()
            print('permission_for_database')

        else:
            msg_box = tk.messagebox.showerror('Error!!',
                                              'No permission for you to databases! ')
            if msg_box == 'ok':
                pass
            print("No permission for you to databases")

    def all_databases(self):
        self.title.pack_forget()
        self.log_f_left.pack_forget()
        self.log_f_right.pack_forget()
        self.next_log_f.pack_forget()
        self.log_f_center.pack_forget()
        self.title_menu_db.pack_forget()
        self.log_f_menu_db.pack_forget()
        self.next_log_f_menu_db.pack_forget()

        self.title_db.pack(ipadx=1000)
        self.log_f_left_db.pack(side=TOP, ipadx=1000)


    def menu_page (self):
        self.frame_app.pack()

    def secin_page (self):
        self.secin = secin(master=self.root, app_sec_in=self)
        self.frame_app.pack_forget()
        self.secin.start_page_secin()

    def sec_out_page (self):
        self.sec_out = sec_out(master=self.root, app_sec_out=self)
        self.frame_app.pack_forget()
        self.sec_out.start_page_sec_out()

    def anti_tamper_page (self):
        self.anti_tamper = anti_tamper(master=self.root, app_anti_tamper=self)
        self.frame_app.pack_forget()
        self.anti_tamper.start_page_ant_tamper()

    def tester_page (self):
        self.frame_app.pack_forget()
        self.Console = Console(master=self.root, app_console=self)

    def test_for_automation(self):
        self.automation_test = automation_test(master=self.root, app_automation_test=self)
        self.frame_app.pack_forget()
        self.automation_test.start_page_automation_test()

    def database_secin_page (self):
        self.database_secin = database_secin(master=self.root, app_data_base_sec_in=self)
        self.frame_app.pack_forget()
        self.database_secin.start_database_secin()
    def database_sec_out_page(self):
        self.database_sec_out = database_sec_out(master=self.root, app_data_base_sec_out=self)
        self.frame_app.pack_forget()
        self.database_sec_out.start_database_sec_out()

    def database_anti_tamper_page(self):
        self.database_anti_tamper = database_anti_tamper(master=self.root, app_data_base_anti_tamper=self)
        self.frame_app.pack_forget()
        self.database_anti_tamper.start_database_anti_tamper()

    def database_automation_test_page(self):
        self.database_automation_test = database_automation_test(master=self.root, app_data_base_automation_test=self)
        self.frame_app.pack_forget()
        self.database_automation_test.start_database_automation()
    def start_page(self):
        self.frame_app.pack()

    def go_back(self):
        self.frame_app.pack_forget()
        self.app.main_page()
    def go_back1(self):
        self.title_db.pack_forget()
        self.log_f_left_db.pack_forget()
        self.title_menu_db.pack_forget()
        self.log_f_menu_db.pack_forget()
        self.next_log_f_menu_db.pack_forget()
        self.title_search_sn.pack_forget()
        self.log_f_search_sn.pack_forget()
        self.next_log_f_search_sn.pack_forget()
        self.log_f_next_search_sn.pack_forget()
        self.title.pack()
        self.log_f_left.pack(side=LEFT)
        self.log_f_right.pack(side=RIGHT)
        self.next_log_f.pack(side=BOTTOM, ipadx=20)
        self.log_f_center.pack(side=BOTTOM, pady=100)

    def check_password_for_all_database (self):
            self.root_all_database_query=Tk()

            def test_database_query ():
                password_1="*"
                entered_pswrd=password_entry.get()
                if entered_pswrd == password_1:

                    button_example=Button(self.root_all_database_query,
                                         text="Databases",
                                         command=self.all_databases, bg="#0059b3", fg="white",
                                         font=FONT,
                                         width=15, borderwidth=10)
                    button_example.pack()
                    password_entry.delete(0, END)

                else:
                    answer_failed=Label(self.root_all_database_query,
                                        text="Login failed:\nInvalid username or password",
                                        bg="#0059b3", fg="white", font=2)
                    answer_failed.pack()

            password_frame=Frame(self.root_all_database_query, bg="sky blue")
            password_frame.pack()

            Label(password_frame, text="Password", bg="sky blue", font=1, fg="black").pack(side='left', padx=7)
            password_entry=Entry(password_frame, bd=3, show="*")
            password_entry.pack(side='right')

            go_button=Button(self.root_all_database_query, text="login!", command=test_database_query, bg="#0059b3",
                             fg="white", width=15,
                             font=1, bd=12)
            go_button.pack(pady=20)

            bottom_frame=Frame(self.root_all_database_query, bg="sky blue")
            bottom_frame.pack()

            answer_login=Label(self.root_all_database_query, text="")
            answer_login.pack()
            self.root_all_database_query.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title( 'Production System' )
    root.protocol( 'WM_DELETE_WINDOW', (lambda: 'pass')() )
    root.config( bg='black' )
    root.attributes( "-fullscreen", True )
    app = App(root)
    root.mainloop()

