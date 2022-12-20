from tkinter import messagebox
import tkinter as tk
import time
import os

time_date = time.asctime()
user = ("Calibri", 10, 'bold')
FONT = ("Calibri", 19, 'bold')
LARGE_FONT = ("Calibri", 19, 'bold')
LARGE_FONT_button_title = ("Calibri", 50, 'bold')
LARGE_FONT_button = ("Calibri", 22, 'bold')
LARGE_FONT_button1 = ("Calibri", 25, 'bold')
LARGE_FONT_button_next = ("Calibri", 15, 'bold')


# function before system log-out #
def exit_application ():
    restart_msg = tk.messagebox.askquestion('Exit Application', 'Are you sure do you want to LogOut? ',
                                            icon='warning')
    if restart_msg == 'no':
        pass
        # tk.messagebox.showinfo('Return', 'You will now return to the application screen')
    else:
        exit()


def restart ():
    msg_box = tk.messagebox.askquestion('Exit Application', 'Are you sure do you want to LogOut? ',
                                        icon='warning')
    if msg_box == 'no':
        tk.messagebox.showinfo('Return', 'You will now return to the application screen')
    else:
        import sys
        """Restarts the current program.
                    Note: this function does not return. Any cleanup action (like
                    saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, *sys.argv)


# functions read from secin page #
def terminal_for_sec_in ():
    import subprocess
    import os

    cmd = "gnome-terminal --geometry=100x5+182+300 --working-directory=/home/tester/SecIn -- bash -c \"echo " \
          f"12345 | sudo -S ./write_si_emmc.sh empty |& tee -a output_flash_secin.txt; exec bash\" "
    subprocess.Popen(args=[cmd], shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)


# functions read from sec-out page #
def terminal_sec_out ():
    import subprocess
    import os
    cmd_sec_out = "gnome-terminal --geometry=100x5+182+300 --working-directory=/home/tester/SecIn -- bash -c \"echo " \
          f"12345 | sudo -S ./write_si_emmc.sh empty |& tee -a output_flash_sec_out.txt; exec bash\" "
    subprocess.Popen(args=[cmd_sec_out], shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)


    # with open("stdout.txt", "wb") as out, open("stderr.txt", "wb") as err:
    #     subprocess.Popen(cmd, shell=True, stdout=out, stderr=err, preexec_fn=os.setsid)


def terminal_reset_sec_out ():
    import subprocess
    import os
    cmd = "gnome-terminal --geometry=500x500+100+200 " \
          "--working-directory=/home/tester/sec_out/0.1.14" \
          " -- bash -c \"echo 12345 | sudo -S ./flash_so_uuu.sh kazuar-sec_out-*.img.gz; exec bash\" "
    subprocess.Popen(args=[cmd], shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)


def check_password_for_reset ():
    root = Tk()

    def test_reset ():
        password_1 = "12345"
        entered_pswrd = password_entry.get()
        if entered_pswrd == password_1:

            buttonexample = Button(root,
                                   text="Reset SOM",
                                   command=terminal_reset_sec_out, bg="#0059b3", fg="white",
                                    font=LARGE_FONT_button_next,
                                   width=15, borderwidth=10)
            buttonexample.pack()
            password_entry.delete(0, END)
        else:
            anser_failed = Label(root, text="Login failed:\nInvalid username or password",
                                 bg="#0059b3", fg="white", font=2)
            anser_failed.pack()

    password_frame = Frame(root, bg="sky blue")
    password_frame.pack()

    Label(password_frame, text="Password", bg="sky blue", font=1, fg="black").pack(side='left', padx=7)
    password_entry = Entry(password_frame, bd=3, show="*")
    password_entry.pack(side='right')

    go_button = Button(root, text="login!", command=test_reset, bg="#0059b3", fg="white", width=15,
                       font=1)
    go_button.pack(pady=15)

    bottom_frame = Frame(root, bg="sky blue")
    bottom_frame.pack()

    answer_login = Label(root, text="")
    answer_login.pack()
    root.mainloop()


def terminal_for_anti_tamper():
    import subprocess
    import os
    cmd = "gnome-terminal --geometry=100x5+182+300 " \
          "--working-directory=/home/tester/Downloads/opt/SEGGER/JLink/JFlashLiteExe -- bash -c \"echo " \
          "12345 | sudo -S /opt/SEGGER/JLink/JFlashLiteExe\""
    subprocess.Popen(args=[cmd], shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)


def terminal_for_anti_tamper_status ():
    import subprocess
    import os
    cmd = "gnome-terminal --geometry=100x5+182+300 " \
          "--working-directory=/home/tester -- bash -c \"echo " \
          "12345 | sudo -S gtkterm\""
    subprocess.Popen(args=[cmd], shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
from tkinter import *
import sqlite3

def query ():
    from tkinter import ttk

    # global record
    conn = sqlite3.connect('Kazuar_tester_PC.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM sec_in_input_user_db")
    records = c.fetchall()

    root = Tk()
    root.attributes('-zoomed', True)
    root.title('Secin database')

    root.config(bg='#0059b3')

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
    tree_frame = Frame(root, bg="#0059b3")
    tree_frame.pack()
    my_canvas = Canvas(tree_frame, relief=FLAT,
                       highlightthickness=0, highlightbackground="#0059b3")
    my_canvas.pack(side=LEFT, fill=BOTH, expand=3, ipady=100)

    second_canvas = Canvas(tree_frame, bg='#0059b3', relief=FLAT,
                           highlightthickness=0, highlightbackground="#0059b3")
    second_canvas.pack(side=LEFT, fill=BOTH, expand=0, padx=20)

    # Treeview Scrollbar
    tree_scroll = Scrollbar(my_canvas)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create Treeview
    my_tree = ttk.Treeview(my_canvas, yscrollcommand=tree_scroll.set,
                           selectmode="extended", show='headings', height=20)
    # Pack to the screen
    my_tree.pack(ipady=100)

    # Configure the scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Our Columns
    my_tree['columns'] = ("ID", "Date", "User", "SN", "Pass", "Description")

    # Formate Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=CENTER, width=50)
    my_tree.column("Date", anchor=CENTER, width=400)
    my_tree.column("User", anchor=CENTER, width=100)
    my_tree.column("SN", anchor=CENTER, width=500)
    my_tree.column("Pass", anchor=CENTER, width=200)
    my_tree.column("Description", anchor=CENTER, width=800)

    # Create Headings
    my_tree.heading("#0", text="", anchor=CENTER)
    my_tree.heading("ID", text="ID", anchor=CENTER)
    my_tree.heading("Date", text="Date", anchor=CENTER)
    my_tree.heading("User", text="User", anchor=CENTER)
    my_tree.heading("SN", text="SN", anchor=CENTER)
    my_tree.heading("Pass", text="Pass", anchor=CENTER)
    my_tree.heading("Description", text="Description", anchor=CENTER)
    # Create striped row tags
    my_tree.tag_configure('oddrow', background="white", font=15)
    my_tree.tag_configure('failrow', background="red", font=15)
    # global count
    count = 0
    for record in records:
        if record[3] == 'NO':
            my_tree.insert(parent='', index='end', text="", values=(record[5], record[0],
                                                                    record[1], record[2],
                                                                    record[3], record[4]), tags=('failrow',), )
        else:
            my_tree.insert(parent='', index='end', text="", values=(record[5], record[0],
                                                                    record[1], record[2],
                                                                    record[3], record[4]), tags=('oddrow',), )

    count += 1

    ########
    Button(second_canvas, text='Back', bg='blue', fg='white',
           command="", bd=12).grid(row=0, column=0, padx=20,
                                         ipadx=20, ipady=20, pady=100)
    Button(second_canvas, text='Excel', bg='green', fg='white',
           command="", bd=12).grid(row=1, column=0, padx=20, ipadx=20,
                                                                     ipady=20, pady=200)

    Button(second_canvas, text='Delete\n(select ID)', bg='red', fg='white',
           command="", bd=12).grid(row=2, column=0, padx=20, pady=20)

    delete_box_sec_in = Entry(second_canvas, width=2)
    delete_box_sec_in.config(font=FONT, relief='flat')
    delete_box_sec_in.insert(0, 'ID')
    delete_box_sec_in.grid(row=3, column=0)
    root.mainloop()

    conn.commit()
    conn.close()


# query()
