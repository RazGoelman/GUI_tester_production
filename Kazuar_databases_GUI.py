from tkinter import *
import tkinter as tk
from tkinter import ttk
import os
import webbrowser
import csv
from tkinter import messagebox
import sqlite3
FONT = ("Calibri", 19, 'bold')
LARGE_FONT = ("Calibri", 19, 'bold')
LARGE_FONT_button_title = ("Calibri", 50, 'bold')
LARGE_FONT_button = ("Calibri", 22, 'bold')
LARGE_FONT_button1 = ("Calibri", 25, 'bold')
LARGE_FONT_button_next = ("Calibri", 15, 'bold')

class database_secin:

    def __init__ (self, master=None, app_data_base_sec_in=None):
        self.delete_data_si = None
        self.my_tree = None
        self.root_to_csv = None
        self.columns = None
        self.column = None
        self.rowcount = None
        self.root_for_export_excel_file = None
        self.record = None
        self.conn = None
        self.c = None
        self.master = master
        self.app_data_base_sec_in = app_data_base_sec_in
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT *, oid FROM sec_in_input_user_db")
        records = self.c.fetchall()

        # Add some style
        style = ttk.Style()
        # Pick a theme
        style.theme_use("clam")
        # ('clam', 'alt', 'default', 'classic')
        # Configure our treeview colors

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=100,
                        )

        # Create Treeview Frame
        self.tree_frame = Frame(self.master, bg="#0059b3")
        self.tree_frame.pack()
        my_canvas = Canvas(self.tree_frame, relief=FLAT,
                           highlightthickness=0, highlightbackground="#0059b3")
        my_canvas.pack(side=LEFT, fill=BOTH, expand=3, ipady=100)

        second_canvas = Canvas(self.tree_frame, bg='#0059b3', relief=FLAT,
                               highlightthickness=0, highlightbackground="#0059b3")
        second_canvas.pack(side=LEFT, fill=BOTH, expand=0, padx=20)

        # Treeview Scrollbar
        tree_scroll = Scrollbar(my_canvas)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview
        self.my_tree = ttk.Treeview(my_canvas, yscrollcommand=tree_scroll.set,
                               selectmode="extended", height=100)
        # Pack to the screen
        self.my_tree.pack(ipadx=80)

        # Configure the scrollbar
        tree_scroll.config(command=self.my_tree.yview)

        # Define Our Columns
        self.my_tree['columns'] = ("ID", "Date", "User", "SN", "Pass", "Description")

        # Formate Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("ID", anchor=CENTER, width=100)
        self.my_tree.column("Date", anchor=CENTER, width=400)
        self.my_tree.column("User", anchor=CENTER, width=200)
        self.my_tree.column("SN", anchor=CENTER, width=500)
        self.my_tree.column("Pass", anchor=CENTER, width=200)
        self.my_tree.column("Description", anchor=CENTER, width=700)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=CENTER)
        self.my_tree.heading("ID", text="ID", anchor=CENTER)
        self.my_tree.heading("Date", text="Date", anchor=CENTER)
        self.my_tree.heading("User", text="User", anchor=CENTER)
        self.my_tree.heading("SN", text="SN", anchor=CENTER)
        self.my_tree.heading("Pass", text="Pass", anchor=CENTER)
        self.my_tree.heading("Description", text="Description", anchor=CENTER)
        # Create striped row tags

        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('failrow', background="red")

        # global count
        count = 0
        for self.record in records:
            if self.record[3] == "NO":
                self.my_tree.insert(parent='', index='end', text="", values=(self.record[5], self.record[0],
                                                                        self.record[1], self.record[2],
                                                                        self.record[3], self.record[4]), tags=('failrow',), )
            else:
                self.my_tree.insert(parent='', index='end', text="", values=(self.record[5], self.record[0],
                                                                        self.record[1], self.record[2],
                                                                        self.record[3], self.record[4]), tags=('oddrow',), )

            count += 1

            ########
        Button(second_canvas, text='Back', bg='blue', fg='white',
               command=self.go_back_db_si, bd=12).grid(row=0, column=0, padx=20,
                                             ipadx=20, ipady=20, pady=100)
        Button(second_canvas, text='Excel', bg='green', fg='white',
               command=self.check_password_for_export_excel_file, bd=12).grid(row=1, column=0, padx=20, ipadx=20,
                                                                         ipady=20, pady=200)

        Button(second_canvas, text='Delete\n(select ID)', bg='red', fg='white',
               command=self.check_password_for_delete_data_si, bd=12).grid(row=2, column=0, padx=20, pady=20)

    def start_database_secin (self):
        self.tree_frame.pack()

    def go_back_db_si (self):
        self.tree_frame.pack_forget()
        # self.delete_data_si.pack_forget()
        self.app_data_base_sec_in.menu_page()

    def check_password_for_delete_data_si (self):
        self.delete_data_si = Tk()
        self.delete_data_si.title('permission for database')

        def test_database_query ():
            password_1 = "12345"
            entered_pswrd = password_entry.get()
            if entered_pswrd == password_1:

                button_example = Button(self.delete_data_si,
                                        text="Delete data",
                                        command=self.delete_sec_in, bg="#0059b3", fg="white",
                                        font=FONT,
                                        width=15, borderwidth=10)
                button_example.pack()
                password_entry.delete(0, END)

            else:
                answer_failed = Label(self.delete_data_si,
                                      text="Login failed:\nInvalid username or password",
                                      bg="#0059b3", fg="white", font=2)
                answer_failed.pack()

        password_frame = Frame(self.delete_data_si, bg="sky blue")
        password_frame.pack()

        Label(password_frame, text="Password", bg="sky blue", font=1, fg="black").pack(side='left', padx=7)
        password_entry = Entry(password_frame, bd=3, show="*")
        password_entry.pack(side='right')

        go_button = Button(self.delete_data_si, text="login!", command=test_database_query, bg="#0059b3",
                           fg="white", width=15,
                           font=1, bd=12)
        go_button.pack(pady=20)

        bottom_frame = Frame(self.delete_data_si, bg="sky blue")
        bottom_frame.pack()

        answer_login = Label(self.delete_data_si, text="")
        answer_login.pack()
        self.delete_data_si.mainloop()

    def delete_sec_in (self):
        self.delete_data_si.destroy()
        response = messagebox.askyesno("permission for database", "This will delete all the data!\nAre you sure? ")
        if response == 1:
            for self.record in self.my_tree.get_children():
                self.my_tree.delete(self.record)
            self.conn = sqlite3.connect('Kazuar_tester_PC.db')
            self.c = self.conn.cursor()
            self.c.execute("DELETE from sec_in_input_user_db")

            self.conn.commit()
            self.conn.close()
            self.go_back_db_si()


    def close_export_excel (self):
        root_to_csv.destroy()
        root_for_export_excel_file.destroy()
        root_sec_in_database_query.destroy()
        self.go_back_db_si()


    def check_password_for_export_excel_file (self):
        self.root_for_export_excel_file = Tk()

        def test_export_excel_file ():
            password_1 = "12345"
            entered_pswrd = password_entry.get()
            if entered_pswrd == password_1:

                button_example = Button(self.root_for_export_excel_file,
                                       text="Export\nto Excel",
                                       command=self.export_to_csv_sec_in, bg="#0059b3", fg="white",
                                       font=FONT,
                                       width=15, borderwidth=10)
                button_example.pack()
                password_entry.delete(0, END)
            else:
                answer_failed = Label(self.root_for_export_excel_file,
                                      text="Login failed:\nInvalid username or password",
                                      bg="#0059b3", fg="white", font=2)
                answer_failed.pack()

        password_frame = Frame(self.root_for_export_excel_file, bg="sky blue")
        password_frame.pack()

        Label(password_frame, text="Password", bg="sky blue", font=1, fg="black").pack(side='left', padx=7)
        password_entry = Entry(password_frame, bd=3, show="*")
        password_entry.pack(side='right')

        go_button = Button(self.root_for_export_excel_file, text="login!", command=test_export_excel_file,
                           bg="#0059b3",
                           fg="white", width=15,
                           font=1, bd=12)
        go_button.pack(pady=20)

        bottom_frame = Frame(self.root_for_export_excel_file, bg="sky blue")
        bottom_frame.pack()

        answer_login = Label(self.root_for_export_excel_file, text="")
        answer_login.pack()
        self.root_for_export_excel_file.mainloop()

    @staticmethod
    def callback_for_sec_in_excel_file (url):
        webbrowser.open_new(url)

        # function to export db to excel file

    def export_to_csv_sec_in (self):
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        self.c.execute('''SELECT * FROM sec_in_input_user_db''')
        self.columns = self.c.fetchall()
        for self.column in self.columns:
            print(self.column)
        print("Exporting data into CSV............")
        cursor = self.conn.cursor()
        cursor.execute("select * from sec_in_input_user_db")

        with open("flash_sec_in_data.csv", "a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)

        self.root_to_csv = Tk()
        self.root_to_csv.title('Export db to Excel')
        self.root_to_csv.configure(bg='#c7d5e0')
        self.root_to_csv.attributes('-zoomed', True)

        label_export = Label( self.root_to_csv, text="Export\nto Excel",
                             bg='#c7d5e0', fg="black", font=('calibri', 30, 'bold'))
        label_export.pack(pady=50)

        Label( self.root_to_csv, text="File Location\n________________",
              font=('calibri', 12, 'bold'), bg='#c7d5e0', relief='flat').pack()

        button_path = Label( self.root_to_csv, fg="red", font=('calibri', 12, 'bold'),
                            text=os.getcwd() + "\n" + "/Sec_in_data.csv", bg='#c7d5e0')
        button_path.pack(pady=10)
        button_path.bind("<Button-1>",
                         lambda e: callback_for_sec_in_excel_file(os.getcwd() + "/Kazuar_tester_PC.csv"))

        Label( self.root_to_csv, text='We have coped' + str(self.c.self.rowcount) + 'rows from the database_pc.',
              bg='#c7d5e0', fg="black", font=('calibri', 12, 'bold')).pack(pady=10)

        Button( self.root_to_csv, text='LogOut', bg="red", fg="white",
               font=('calibri', 15, 'bold'), bd=12, command=self.close_export_excel).pack(pady=100, ipadx=50)
        self.root_to_csv.mainloop()
##################################################################################################################
class database_sec_out:
    def __init__ (self, master=None, app_data_base_sec_out=None):
        self.delete_data_so = None
        self.my_tree = None
        self.root_to_csv = None
        self.columns = None
        self.column = None
        self.rowcount = None
        self.root_for_export_excel_file = None
        self.record = None
        self.conn = None
        self.c = None
        self.master = master
        self.app_data_base_sec_out = app_data_base_sec_out
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT *, oid FROM sec_out_input_user_db")
        records = self.c.fetchall()

        # Add some style
        style = ttk.Style()
        # Pick a theme
        style.theme_use("clam")
        # ('clam', 'alt', 'default', 'classic')
        # Configure our treeview colors

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=100,
                        )

        # Create Treeview Frame
        self.tree_frame_sec_out = Frame(self.master, bg="#0059b3")
        self.tree_frame_sec_out.pack()
        my_canvas = Canvas(self.tree_frame_sec_out, relief=FLAT,
                           highlightthickness=0, highlightbackground="#0059b3")
        my_canvas.pack(side=LEFT, fill=BOTH, expand=3, ipady=100)

        second_canvas = Canvas(self.tree_frame_sec_out, bg='#0059b3', relief=FLAT,
                               highlightthickness=0, highlightbackground="#0059b3")
        second_canvas.pack(side=LEFT, fill=BOTH, expand=0, padx=20)

        # Treeview Scrollbar
        tree_scroll = Scrollbar(my_canvas)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview
        self.my_tree = ttk.Treeview(my_canvas, yscrollcommand=tree_scroll.set,
                               selectmode="extended", height=100)
        # Pack to the screen
        self.my_tree.pack(ipadx=80)

        # Configure the scrollbar
        tree_scroll.config(command=self.my_tree.yview)

        # Define Our Columns
        self.my_tree['columns'] = ("ID", "Date", "User", "Kazuar Board SN", "SOM SN", "SOM Revision")

        # Formate Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("ID", anchor=CENTER, width=100)
        self.my_tree.column("Date", anchor=CENTER, width=400)
        self.my_tree.column("User", anchor=CENTER, width=200)
        self.my_tree.column("Kazuar Board SN", anchor=CENTER, width=500)
        self.my_tree.column("SOM SN", anchor=CENTER, width=500)
        self.my_tree.column("SOM Revision", anchor=CENTER, width=400)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=CENTER)
        self.my_tree.heading("ID", text="ID", anchor=CENTER)
        self.my_tree.heading("Date", text="Date", anchor=CENTER)
        self.my_tree.heading("User", text="User", anchor=CENTER)
        self.my_tree.heading("Kazuar Board SN", text="Kazuar Board SN", anchor=CENTER)
        self.my_tree.heading("SOM SN", text="SOM SN", anchor=CENTER)
        self.my_tree.heading("SOM Revision", text="SOM Revision", anchor=CENTER)
        # Create striped row tags

        self.my_tree.tag_configure('oddrow', background="white")

        # global count
        count = 0
        for self.record in records:
            self.my_tree.insert(parent='', index='end', text="", values=(self.record[5], self.record[0],
                                                                    self.record[1], self.record[2],
                                                                    self.record[3], self.record[4]), tags=('addrow',), )

        count += 1

            ########
        Button(second_canvas, text='Back', bg='blue', fg='white',
               command=self.go_back_db_sec_out, bd=12).grid(row=0, column=0, padx=20,
                                             ipadx=20, ipady=20, pady=100)
        Button(second_canvas, text='Excel', bg='green', fg='white',
               command=self.check_password_for_export_excel_file_sec_out, bd=12).grid(row=1, column=0, padx=20, ipadx=20,
                                                                         ipady=20, pady=200)

        Button(second_canvas, text='Delete\n(select ID)', bg='red', fg='white',
               command=self.check_password_for_delete_data_so, bd=12).grid(row=2, column=0, padx=20, pady=20)

    def start_database_sec_out (self):
        self.tree_frame_sec_out.pack()

    def go_back_db_sec_out (self):
        self.tree_frame_sec_out.pack_forget()
        self.app_data_base_sec_out.menu_page()


    def check_password_for_delete_data_so (self):
        self.delete_data_so = Tk()

        def test_database_query ():
            password_1 = "12345"
            entered_pswrd = password_entry.get()
            if entered_pswrd == password_1:

                button_example = Button(self.delete_data_so,
                                        text="Delete data",
                                        command=self.delete_sec_out, bg="#0059b3", fg="white",
                                        font=FONT,
                                        width=15, borderwidth=10)
                button_example.pack()
                password_entry.delete(0, END)

            else:
                answer_failed = Label(self.delete_data_so,
                                      text="Login failed:\nInvalid username or password",
                                      bg="#0059b3", fg="white", font=2)
                answer_failed.pack()

        password_frame = Frame(self.delete_data_so, bg="sky blue")
        password_frame.pack()

        Label(password_frame, text="Password", bg="sky blue", font=1, fg="black").pack(side='left', padx=7)
        password_entry = Entry(password_frame, bd=3, show="*")
        password_entry.pack(side='right')

        go_button = Button(self.delete_data_so, text="login!", command=test_database_query, bg="#0059b3",
                           fg="white", width=15,
                           font=1, bd=12)
        go_button.pack(pady=20)

        bottom_frame = Frame(self.delete_data_so, bg="sky blue")
        bottom_frame.pack()

        answer_login = Label(self.delete_data_so, text="")
        answer_login.pack()
        self.delete_data_so.mainloop()

    def delete_sec_out (self):
        self.delete_data_so.destroy()
        response = messagebox.askyesno("permission for database", "This will delete all the data!\nAre you sure? ")
        if response == 1:
            for self.record in self.my_tree.get_children():
                self.my_tree.delete(self.record)
            self.conn = sqlite3.connect('Kazuar_tester_PC.db')
            self.c = self.conn.cursor()
            self.c.execute("DELETE from sec_out_input_user_db")

            self.conn.commit()
            self.conn.close()
            self.go_back_db_sec_out()

    def close_export_excel (self):
        root_to_csv.destroy()
        root_for_export_excel_file.destroy()
        root_sec_out_database_query.destroy()
        self.go_back_db_si()


    def check_password_for_export_excel_file_sec_out (self):
        self.root_for_export_excel_file = Tk()

        def test_export_excel_file ():
            password_1 = "12345"
            entered_pswrd = password_entry.get()
            if entered_pswrd == password_1:

                button_example = Button(self.root_for_export_excel_file,
                                       text="Export\nto Excel",
                                       command=self.export_to_csv_sec_out, bg="#0059b3", fg="white",
                                       font=FONT,
                                       width=15, borderwidth=10)
                button_example.pack()
                password_entry.delete(0, END)
            else:
                answer_failed = Label(self.root_for_export_excel_file,
                                      text="Login failed:\nInvalid username or password",
                                      bg="#0059b3", fg="white", font=2)
                answer_failed.pack()

        password_frame = Frame(self.root_for_export_excel_file, bg="sky blue")
        password_frame.pack()

        Label(password_frame, text="Password", bg="sky blue", font=1, fg="black").pack(side='left', padx=7)
        password_entry = Entry(password_frame, bd=3, show="*")
        password_entry.pack(side='right')

        go_button = Button(self.root_for_export_excel_file, text="login!", command=test_export_excel_file,
                           bg="#0059b3",
                           fg="white", width=15,
                           font=1, bd=12)
        go_button.pack(pady=20)

        bottom_frame = Frame(self.root_for_export_excel_file, bg="sky blue")
        bottom_frame.pack()

        answer_login = Label(self.root_for_export_excel_file, text="")
        answer_login.pack()
        self.root_for_export_excel_file.mainloop()

    @staticmethod
    def callback_for_sec_out_excel_file (url):
        webbrowser.open_new(url)

        # function to export db to excel file

    def export_to_csv_sec_out (self):
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        self.c.execute('''SELECT * FROM sec_out_input_user_db''')
        self.columns = self.c.fetchall()
        for self.column in self.columns:
            print(self.column)
        print("Exporting data into CSV............")
        cursor = self.conn.cursor()
        cursor.execute("select * from sec_out_input_user_db")

        with open("flash_sec_out_data.csv", "a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)

        self.root_to_csv = Tk()
        self.root_to_csv.title('Export db to Excel')
        self.root_to_csv.configure(bg='#c7d5e0')
        self.root_to_csv.attributes('-zoomed', True)

        label_export = Label( self.root_to_csv, text="Export\nto Excel",
                             bg='#c7d5e0', fg="black", font=('calibri', 30, 'bold'))
        label_export.pack(pady=50)

        Label( self.root_to_csv, text="File Location\n________________",
              font=('calibri', 12, 'bold'), bg='#c7d5e0', relief='flat').pack()

        button_path = Label( self.root_to_csv, fg="red", font=('calibri', 12, 'bold'),
                            text=os.getcwd() + "\n" + "/flash_sec_out_data.csv", bg='#c7d5e0')
        button_path.pack(pady=10)
        button_path.bind("<Button-1>",
                         lambda e: callback_for_sec_out_excel_file(os.getcwd() + "/Kazuar_tester_PC.csv"))

        Label( self.root_to_csv, text='We have coped' + str(self.c.self.rowcount) + 'rows from the database_pc.',
              bg='#c7d5e0', fg="black", font=('calibri', 12, 'bold')).pack(pady=10)

        Button( self.root_to_csv, text='LogOut', bg="red", fg="white",
               font=('calibri', 15, 'bold'), bd=12, command=self.close_export_excel).pack(pady=100, ipadx=50)
        self.root_to_csv.mainloop()


class database_anti_tamper:
    def __init__ (self, master=None, app_data_base_anti_tamper=None):
        self.delete_data_anti_tamper = None
        self.root_to_csv = None
        self.columns = None
        self.column = None
        self.rowcount = None
        self.root_for_export_excel_file = None
        self.record = None
        self.conn = None
        self.c = None
        self.master = master
        self.app_data_base_anti_tamper = app_data_base_anti_tamper
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT *, oid FROM AT_input_user_db")
        records = self.c.fetchall()

        # Add some style
        style = ttk.Style()
        # Pick a theme
        style.theme_use("clam")
        # ('clam', 'alt', 'default', 'classic')
        # Configure our treeview colors

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=100,
                        )

        # Create Treeview Frame
        self.tree_frame_anti_tamper = Frame(self.master, bg="#0059b3")
        self.tree_frame_anti_tamper.pack()
        my_canvas = Canvas(self.tree_frame_anti_tamper, relief=FLAT,
                           highlightthickness=0, highlightbackground="#0059b3")
        my_canvas.pack(side=LEFT, fill=BOTH, expand=3, ipady=100)

        second_canvas = Canvas(self.tree_frame_anti_tamper, bg='#0059b3', relief=FLAT,
                               highlightthickness=0, highlightbackground="#0059b3")
        second_canvas.pack(side=LEFT, fill=BOTH, expand=0, padx=20)

        # Treeview Scrollbar
        tree_scroll = Scrollbar(my_canvas)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview
        self.my_tree = ttk.Treeview(my_canvas, yscrollcommand=tree_scroll.set,
                                    selectmode="extended", height=100)
        # Pack to the screen
        self.my_tree.pack(ipadx=80)

        # Configure the scrollbar
        tree_scroll.config(command=self.my_tree.yview)

        # Define Our Columns
        self.my_tree['columns'] = ("ID", "Date", "User", "Kazuar Board SN", "AT Version", "Burning Result")

        # Formate Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("ID", anchor=CENTER, width=100)
        self.my_tree.column("Date", anchor=CENTER, width=400)
        self.my_tree.column("User", anchor=CENTER, width=200)
        self.my_tree.column("Kazuar Board SN", anchor=CENTER, width=500)
        self.my_tree.column("AT Version", anchor=CENTER, width=500)
        self.my_tree.column("Burning Result", anchor=CENTER, width=400)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=CENTER)
        self.my_tree.heading("ID", text="ID", anchor=CENTER)
        self.my_tree.heading("Date", text="Date", anchor=CENTER)
        self.my_tree.heading("User", text="User", anchor=CENTER)
        self.my_tree.heading("Kazuar Board SN", text="Kazuar Board SN", anchor=CENTER)
        self.my_tree.heading("AT Version", text="AT Version", anchor=CENTER)
        self.my_tree.heading("Burning Result", text="Burning Result", anchor=CENTER)
        # Create striped row tags

        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('failrow', background="red")


        # global count
        count = 0
        for self.record in records:
            if self.record[4] == 'fail':
                self.my_tree.insert(parent='', index='end', text="", values=(self.record[5], self.record[0],
                                                                             self.record[1], self.record[2],
                                                                             self.record[3], self.record[4]),
                                    tags=('failrow',), )
            else:
                self.my_tree.insert(parent='', index='end', text="", values=(self.record[5], self.record[0],
                                                                             self.record[1], self.record[2],
                                                                             self.record[3], self.record[4]),
                                    tags=('addrow',), )

        count += 1

        ########
        Button(second_canvas, text='Back', bg='blue', fg='white',
               command=self.go_back_db_anti_tamper, bd=12).grid(row=0, column=0, padx=20,
                                                                ipadx=20, ipady=20, pady=100)
        Button(second_canvas, text='Excel', bg='green', fg='white',
               command='check_password_for_export_excel_file', bd=12).grid(row=1, column=0, padx=20, ipadx=20,
                                                                           ipady=20, pady=200)

        Button(second_canvas, text='Delete\n(select ID)', bg='red', fg='white',
               command=self.check_password_for_delete_data_anti_tamper, bd=12).grid(row=2, column=0, padx=20, pady=20)

    def start_database_anti_tamper (self):
        self.tree_frame_anti_tamper.pack()

    def go_back_db_anti_tamper (self):
        self.tree_frame_anti_tamper.pack_forget()
        self.app_data_base_anti_tamper.menu_page()

    def check_password_for_delete_data_anti_tamper (self):
        self.delete_data_anti_tamper = Tk()

        def test_database_query ():
            password_1 = "12345"
            entered_pswrd = password_entry.get()
            if entered_pswrd == password_1:

                button_example = Button(self.delete_data_anti_tamper,
                                        text="Delete data",
                                        command=self.delete_data_at, bg="#0059b3", fg="white",
                                        font=FONT,
                                        width=15, borderwidth=10)
                button_example.pack()
                password_entry.delete(0, END)

            else:
                answer_failed = Label(self.delete_data_anti_tamper,
                                      text="Login failed:\nInvalid username or password",
                                      bg="#0059b3", fg="white", font=2)
                answer_failed.pack()

        password_frame = Frame(self.delete_data_anti_tamper, bg="sky blue")
        password_frame.pack()

        Label(password_frame, text="Password", bg="sky blue", font=1, fg="black").pack(side='left', padx=7)
        password_entry = Entry(password_frame, bd=3, show="*")
        password_entry.pack(side='right')

        go_button = Button(self.delete_data_anti_tamper, text="login!", command=test_database_query, bg="#0059b3",
                           fg="white", width=15,
                           font=1, bd=12)
        go_button.pack(pady=20)

        bottom_frame = Frame(self.delete_data_anti_tamper, bg="sky blue")
        bottom_frame.pack()

        answer_login = Label(self.delete_data_anti_tamper, text="")
        answer_login.pack()
        self.delete_data_anti_tamper.mainloop()

    def delete_data_at (self):
        self.delete_data_anti_tamper.destroy()
        response = messagebox.askyesno("Stop!", "This will delete all the data!\nAre you sure? ")
        if response == 1:
            for self.record in self.my_tree.get_children():
                self.my_tree.delete(self.record)
            self.conn = sqlite3.connect('Kazuar_tester_PC.db')
            self.c = self.conn.cursor()
            self.c.execute("DELETE from AT_input_user_db")

            self.conn.commit()
            self.conn.close()
            self.go_back_db_anti_tamper()

        # self.conn.commit()
        # self.conn.close()

    @staticmethod
    def close_export_excel ():
        root_to_csv.destroy()
        root_for_export_excel_file.destroy()
        root_sec_in_database_query.destroy()

    def check_password_for_export_excel_file (self):
        self.root_for_export_excel_file = Tk()

        def test_export_excel_file ():
            password_1 = "12345"
            entered_pswrd = password_entry.get()
            if entered_pswrd == password_1:

                button_example = Button(self.root_for_export_excel_file,
                                        text="Export\nto Excel",
                                        command=export_to_csv_anti_tamper, bg="#0059b3", fg="white",
                                        font=FONT,
                                        width=15, borderwidth=10)
                button_example.pack()
                password_entry.delete(0, END)
            else:
                answer_failed = Label(self.root_for_export_excel_file,
                                      text="Login failed:\nInvalid username or password",
                                      bg="#0059b3", fg="white", font=2)
                answer_failed.pack()

        password_frame = Frame(self.root_for_export_excel_file, bg="sky blue")
        password_frame.pack()

        Label(password_frame, text="Password", bg="sky blue", font=1, fg="black").pack(side='left', padx=7)
        password_entry = Entry(password_frame, bd=3, show="*")
        password_entry.pack(side='right')

        go_button = Button(self.root_for_export_excel_file, text="login!", command=test_export_excel_file,
                           bg="#0059b3",
                           fg="white", width=15,
                           font=1, bd=12)
        go_button.pack(pady=20)

        bottom_frame = Frame(self.root_for_export_excel_file, bg="sky blue")
        bottom_frame.pack()

        answer_login = Label(self.root_for_export_excel_file, text="")
        answer_login.pack()
        self.root_for_export_excel_file.mainloop()

    @staticmethod
    def callback_for_anti_tamper_excel_file (url):
        webbrowser.open_new(url)

        # function to export db to excel file

    def export_to_csv_anti_tamper (self):
        # global rowcount
        # Create a database or connect to one
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        self.c.execute('''SELECT * FROM AT_input_user_db''')
        self.columns = self.c.fetchall()
        for self.column in self.columns:
            print(self.column)
        print("Exporting data into CSV............")
        cursor = self.conn.cursor()
        cursor.execute("select * from AT_input_user_db")

        with open("flash_AT_data.csv", "a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)

        self.root_to_csv = Tk()
        self.root_to_csv.title('Export db to Excel')
        self.root_to_csv.configure(bg='#c7d5e0')
        self.root_to_csv.attributes('-zoomed', True)

        label_export = Label(self.root_to_csv, text="Export\nto Excel",
                             bg='#c7d5e0', fg="black", font=('calibri', 30, 'bold'))
        label_export.pack(pady=50)

        Label(self.root_to_csv, text="File Location\n________________",
              font=('calibri', 12, 'bold'), bg='#c7d5e0', relief='flat').pack()

        button_path = Label(self.root_to_csv, fg="red", font=('calibri', 12, 'bold'),
                            text=os.getcwd() + "\n" + "/Sec_in_data.csv", bg='#c7d5e0')
        button_path.pack(pady=10)
        button_path.bind("<Button-1>",
                         lambda e: callback_for_anti_tamper_excel_file(os.getcwd() + "/Kazuar_tester_PC.csv"))

        Label(self.root_to_csv, text='We have coped' + str(self.c.self.self.rowcount) + 'rows from the database_pc.',
              bg='#c7d5e0', fg="black", font=('calibri', 12, 'bold')).pack(pady=10)

        Button(self.root_to_csv, text='LogOut', bg="red", fg="white",
               font=('calibri', 15, 'bold'), bd=12, command=self.close_export_excel).pack(pady=100, ipadx=50)
        self.root_to_csv.mainloop()


class database_automation_test:
    def __init__ (self, master=None, app_data_base_automation_test=None):
        self.delete_data_database_automation = None
        self.tree_frame_database_automation = None
        self.root_to_csv = None
        self.columns = None
        self.column = None
        self.rowcount = None
        self.root_for_export_excel_file = None
        self.record = None
        self.conn = None
        self.c = None
        self.master = master
        self.app_data_base_automation_test = app_data_base_automation_test
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT *, oid FROM database_automation")
        records = self.c.fetchall()

        # Add some style
        style = ttk.Style()
        # Pick a theme
        style.theme_use("clam")
        # ('clam', 'alt', 'default', 'classic')
        # Configure our treeview colors

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=100,
                        )

        # Create Treeview Frame
        self.tree_frame_database_automation = Frame(self.master, bg="#0059b3")
        self.tree_frame_database_automation.pack()
        my_canvas = Canvas(self.tree_frame_database_automation, relief=FLAT,
                           highlightthickness=0, highlightbackground="#0059b3")
        my_canvas.pack(side=TOP, fill=X, expand=0)

        second_canvas = Canvas(self.tree_frame_database_automation, bg='#0059b3', relief=FLAT,
                               highlightthickness=0, highlightbackground="#0059b3")
        second_canvas.pack(side=TOP, fill=X, expand=0, pady=40)

        # Treeview Scrollbar
        tree_scroll = Scrollbar(my_canvas)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview
        self.my_tree = ttk.Treeview(my_canvas, yscrollcommand=tree_scroll.set,
                               selectmode="extended", height=12)
        # Pack to the screen
        self.my_tree.pack()

        # Configure the scrollbar
        tree_scroll.config(command=self.my_tree.yview)

        # Define Our Columns
        self.my_tree['columns'] = ("ID", "Date", "User", "EMS", "SN", "Platform Model", "Processor GEN", "Processor",
                              "DDR Size", "Screen Model", "Keyboard Configuration", "SWB", "KB",
                              "SOM", "Kazuar Laptop Model", "Kazuar Laptop sn", "SecIn Version", "SecOut Version",
                              "AT Version")

        # Formate Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("ID", anchor=CENTER, width=50)
        self.my_tree.column("Date", anchor=CENTER, width=400)
        self.my_tree.column("User", anchor=CENTER, width=150)
        self.my_tree.column("EMS", anchor=CENTER, width=200)
        self.my_tree.column("SN", anchor=CENTER, width=300)
        self.my_tree.column("Platform Model", anchor=CENTER, width=300)
        self.my_tree.column("Processor GEN", anchor=CENTER, width=300)
        self.my_tree.column("Processor", anchor=CENTER, width=300)
        self.my_tree.column("DDR Size", anchor=CENTER, width=300)
        self.my_tree.column("Screen Model", anchor=CENTER, width=300)
        self.my_tree.column('Keyboard Configuration', anchor=CENTER, width=400)
        self.my_tree.column("SWB", anchor=CENTER, width=100)
        self.my_tree.column("KB", anchor=CENTER, width=100)
        self.my_tree.column("SOM", anchor=CENTER, width=100)
        self.my_tree.column("Kazuar Laptop Model", anchor=CENTER, width=400)
        self.my_tree.column("Kazuar Laptop sn", anchor=CENTER, width=400)
        self.my_tree.column("SecIn Version", anchor=CENTER, width=300)
        self.my_tree.column("SecOut Version", anchor=CENTER, width=300)
        self.my_tree.column("AT Version", anchor=CENTER, width=300)

        ###
        # Create Headings

        self.my_tree.heading("#0", text="", anchor=CENTER)
        self.my_tree.heading("ID", text="ID", anchor=CENTER)
        self.my_tree.heading("Date", text="Date", anchor=CENTER)
        self.my_tree.heading("User", text="User", anchor=CENTER)
        self.my_tree.heading("EMS", text="EMS", anchor=CENTER)
        self.my_tree.heading("SN", text="SN", anchor=CENTER)
        self.my_tree.heading("Platform Model", text="Platform Model", anchor=CENTER)
        self.my_tree.heading("Processor GEN", text="Processor GEN", anchor=CENTER)
        self.my_tree.heading("Processor", text="Processor", anchor=CENTER)
        self.my_tree.heading("DDR Size", text="DDR Size", anchor=CENTER)
        self.my_tree.heading("Screen Model", text="Screen Model", anchor=CENTER)
        self.my_tree.heading("Keyboard Configuration", text="Keyboard Configuration", anchor=CENTER)
        self.my_tree.heading("SWB", text="SWB", anchor=CENTER)
        self.my_tree.heading("KB", text="KB", anchor=CENTER)
        self.my_tree.heading("SOM", text="SOM", anchor=CENTER)
        self.my_tree.heading("Kazuar Laptop Model", text="Kazuar Laptop Model", anchor=CENTER)
        self.my_tree.heading("Kazuar Laptop sn", text="Kazuar Laptop sn", anchor=CENTER)
        self.my_tree.heading("SecIn Version", text="SecIn Version", anchor=CENTER)
        self.my_tree.heading("SecOut Version", text="SecOut Version", anchor=CENTER)
        self.my_tree.heading("AT Version", text="AT Version", anchor=CENTER)

        # Create striped row tags

        self.my_tree.tag_configure('oddrow', background="white")

        # global count
        count = 0
        for self.record in records:
            self.my_tree.insert(parent='', index='end', text="", values=(self.record[18], self.record[0],
                                                                    self.record[1], self.record[2],
                                                                    self.record[3], self.record[4], self.record[5],
                                                                    self.record[6],
                                                                    self.record[7], self.record[8], self.record[9],
                                                                    self.record[10],
                                                                    self.record[11], self.record[12], self.record[13],
                                                                    self.record[14],
                                                                    self.record[15], self.record[16], self.record[17]),
                           tags=('addrow',), )

        count += 1

            ########
        Button(second_canvas, text='Back', bg='blue', fg='white',
               command=self.go_back_db_database_automation, bd=12).grid(row=0, column=0, padx=300,
                                                       ipadx=30, ipady=20)
        Button(second_canvas, text='Excel', bg='green', fg='white',
               command='check_password_for_export_excel_file', bd=12).grid(row=0, column=1, padx=300, ipadx=30,
                                                                           ipady=20)

        Button(second_canvas, text='Delete\n(select ID)', bg='red', fg='white',
               command=self.check_password_for_delete_database_automation, bd=12).grid(row=0,
                                                                                       column=2, padx=300)

    def start_database_automation (self):
        self.tree_frame_database_automation.pack()

    def go_back_db_database_automation (self):
        self.tree_frame_database_automation.pack_forget()
        self.app_data_base_automation_test.menu_page()

    def check_password_for_delete_database_automation (self):
        self.delete_data_database_automation = Tk()

        def test_database_query ():
            password_1 = "12345"
            entered_pswrd = password_entry.get()
            if entered_pswrd == password_1:

                button_example = Button(self.delete_data_database_automation,
                                        text="Delete data",
                                        command=self.delete_database_automation, bg="#0059b3", fg="white",
                                        font=FONT,
                                        width=15, borderwidth=10)
                button_example.pack()
                password_entry.delete(0, END)

            else:
                answer_failed = Label(self.delete_data_database_automation,
                                      text="Login failed:\nInvalid username or password",
                                      bg="#0059b3", fg="white", font=2)
                answer_failed.pack()

        password_frame = Frame(self.delete_data_database_automation, bg="sky blue")
        password_frame.pack()

        Label(password_frame, text="Password", bg="sky blue", font=1, fg="black").pack(side='left', padx=7)
        password_entry = Entry(password_frame, bd=3, show="*")
        password_entry.pack(side='right')

        go_button = Button(self.delete_data_database_automation, text="login!", command=test_database_query, bg="#0059b3",
                           fg="white", width=15,
                           font=1, bd=12)
        go_button.pack(pady=20)

        bottom_frame = Frame(self.delete_data_database_automation, bg="sky blue")
        bottom_frame.pack()

        answer_login = Label(self.delete_data_database_automation, text="")
        answer_login.pack()
        self.delete_data_database_automation.mainloop()

    def delete_database_automation (self):
        self.delete_data_database_automation.destroy()
        response = messagebox.askyesno("Stop!", "This will delete all the data!\nAre you sure? ")
        if response == 1:
            for self.record in self.my_tree.get_children():
                self.my_tree.delete(self.record)
            self.conn = sqlite3.connect('Kazuar_tester_PC.db')
            self.c = self.conn.cursor()
            self.c.execute("DELETE from database_automation")

            self.conn.commit()
            self.conn.close()
            self.go_back_db_database_automation()

        self.conn.commit()
        self.conn.close()

    @staticmethod
    def close_export_excel ():
        root_to_csv.destroy()
        root_for_export_excel_file.destroy()
        root_sec_in_database_query.destroy()

    def check_password_for_export_excel_file (self):
        self.root_for_export_excel_file = Tk()

        def test_export_excel_file ():
            password_1 = "12345"
            entered_pswrd = password_entry.get()
            if entered_pswrd == password_1:

                button_example = Button(self.root_for_export_excel_file,
                                        text="Export\nto Excel",
                                        command=self.export_to_csv_automation, bg="#0059b3", fg="white",
                                        font=FONT,
                                        width=15, borderwidth=10)
                button_example.pack()
                password_entry.delete(0, END)
            else:
                answer_failed = Label(self.root_for_export_excel_file,
                                      text="Login failed:\nInvalid username or password",
                                      bg="#0059b3", fg="white", font=2)
                answer_failed.pack()

        password_frame = Frame(self.root_for_export_excel_file, bg="sky blue")
        password_frame.pack()

        Label(password_frame, text="Password", bg="sky blue", font=1, fg="black").pack(side='left', padx=7)
        password_entry = Entry(password_frame, bd=3, show="*")
        password_entry.pack(side='right')

        go_button = Button(self.root_for_export_excel_file, text="login!", command=self.test_export_excel_file,
                           bg="#0059b3",
                           fg="white", width=15,
                           font=1, bd=12)
        go_button.pack(pady=20)

        bottom_frame = Frame(self.root_for_export_excel_file, bg="sky blue")
        bottom_frame.pack()

        answer_login = Label(self.root_for_export_excel_file, text="")
        answer_login.pack()
        self.root_for_export_excel_file.mainloop()

    @staticmethod
    def callback_for_anti_tamper_excel_file (url):
        webbrowser.open_new(url)

        # function to export db to excel file

    def export_to_csv_automation (self):
        global records
        # Create a database or connect to one
        self.conn = sqlite3.connect('Kazuar_tester_PC.db')
        self.c = self.conn.cursor()
        self.c.execute('''SELECT * FROM database_automation''')
        columns = self.c.fetchall()
        for self.column in columns:
            print(self.column)
        print("Exporting data into CSV............")
        cursor = self.conn.cursor()
        cursor.execute("select * from database_automation")

        with open("automation test.csv", "a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)

        self.root_to_csv = Tk()
        self.root_to_csv.title('Export db to Excel')
        self.root_to_csv.configure(bg='#c7d5e0')
        self.root_to_csv.attributes('-zoomed', True)

        label_export = Label(self.root_to_csv, text="Export\nto Excel",
                             bg='#c7d5e0', fg="black", font=('calibri', 30, 'bold'))
        label_export.pack(pady=50)

        Label(root_to_csv, text="File Location\n________________",
              font=('calibri', 12, 'bold'), bg='#c7d5e0', relief='flat').pack()

        button_path = Label(self.root_to_csv, fg="red", font=('calibri', 12, 'bold'),
                            text=os.getcwd() + "\n" + "/automation test.csv", bg='#c7d5e0')
        button_path.pack(pady=10)
        button_path.bind("<Button-1>",
                         lambda e: self.callback_for_automation_excel_file(os.getcwd() + "/Kazuar_tester_PC.csv"))

        Label(self.root_to_csv, text='We have coped' + str(self.c.self.rowcount) + 'rows from the database_pc.',
              bg='#c7d5e0', fg="black", font=('calibri', 12, 'bold')).pack(pady=10)

        Button(self.root_to_csv, text='LogOut', bg="red", fg="white",
               font=('calibri', 15, 'bold'), bd=12, command=self.close_export_excel).pack(pady=100, ipadx=50)
        self.root_to_csv.mainloop()


