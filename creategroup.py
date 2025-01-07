from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
from tkinter import scrolledtext
import customtkinter as ctk
import sqlite3
from settings import *
import os
import shutil
import json
from checklistcombobox import *
from PIL import ImageTk, Image


def createnewgroup(self, *args, **kwargs):
    rwindow = tkinter.Toplevel()
    rwindow.title("Register")
    rwindow.geometry("600x790+200+200")
    rwindow.resizable(False, False)
    rwindow.configure(background="powder blue")
    rwindow.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))

    groupname = StringVar(value="Your Group Name")

    configmethodvar = StringVar()

    global memselecchkbxvar
    self.memselecchkbxvar = []

    memvaluesdb = []

    global cmdenryvar
    cmdenryvar = []

    def changegroupfile(self, *args, **kwargs):

        groudevicepath = os.path.join(devicegroups, groupname.get())

        dest_path = os.path.join(groudevicepath, groupname.get() + ".json")
        filetoread = open(dest_path)
        inputjsondata = json.load(filetoread)

        inputjsondata["members"] = self.memselecchkbxvar

        inputjsondata["method"].append(configmethodvar.get())

        inputjsondata["commands"] = cmdenryvar

        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(inputjsondata, f, ensure_ascii=False, indent=4)

        filetoread.close()

        memselecchkbx.configure(state="disabled")
        memselecbtn.configure(state="disabled")

        confmethodselec.configure(state="disabled")
        confbtn.configure(state="disabled")

        grpdesetry.configure(state="disabled", bg="gray")
        grpdesbtn.configure(state="disabled")

        btnadd.configure(state="disabled")

        creategrpstatuslbl.configure(
            text=f"New Group ({groupname.get()}) has been created"
        )

    def populatemembx():

        try:
            sqliteConnection = sqlite3.connect(dbfile)
            cursor = sqliteConnection.cursor()
            query = f"SELECT id FROM devices"
            cursor.execute(query)
            record = cursor.fetchall()
            result_list = [row[0] for row in record]
            result_list = list(map(str, result_list))

            memvaluesdb = result_list

            memselecchkbx.config(values=memvaluesdb)

        except sqlite3.Error as error:
            pass

    def grpprofilename():

        populatemembx()

        grpnameetry.configure(state=DISABLED)
        grpnameetry.configure(fg_color="gray64")

        groudevicepath = os.path.join(devicegroups, groupname.get())

        if os.path.exists(groudevicepath):

            grpnameetry.configure(state=NORMAL, fg_color="yellow2")
            messagebox.showinfo(
                title="Create Group",
                message=f"Group already exists: {groupname.get()}",
                icon="warning",
                parent=rwindow,
            )

        else:

            src_path = os.path.join(devicegroups, "jsonTemplate.json")
            dest_path = os.path.join(groudevicepath, groupname.get() + ".json")

            if not os.path.exists(groudevicepath):
                os.mkdir(groudevicepath)

            try:
                shutil.copy(src_path, dest_path)

            except:
                pass

            filetoread = open(dest_path)
            inputjsondata = json.load(filetoread)
            inputjsondata["devicegroup"]["groupname"] = groupname.get()

            with open(dest_path, "w", encoding="utf-8") as f:
                json.dump(inputjsondata, f, ensure_ascii=False, indent=4)

            filetoread.close()

            cgouttxtbx.configure(state=NORMAL)
            cgouttxtbx.insert(INSERT, f"1) Group Created: {grpnameetry.get()}\n")
            cgouttxtbx.configure(state=DISABLED)
            grpnameetry.configure(state=DISABLED)
            grpnamebtn.configure(state=DISABLED, fg_color="gray", text="Accepted")
            memselecbtn.configure(state=NORMAL, fg_color="green")
            memselecchkbx.configure(state="readonly")
            memselectlbl.configure(state=NORMAL)
            conflbl.configure(state=NORMAL)
            confbtn.configure(state=NORMAL, fg_color="green")
            confmethodselec.configure(
                state="readonly",
                fg_color="PaleGreen2",
                border_color="dark slate gray",
                button_color="dark slate gray",
            )
            grpdesbtn.configure(state=NORMAL, fg_color="green")
            grpdesetry.configure(state=NORMAL)
            grpdesclbl.configure(state=NORMAL)
            grpdesetry.configure(background="light yellow")

            btnadd.configure(state=NORMAL, fg_color="green")

    def memselectfun():
        global memselecchkbxvar

        cgouttxtbx.configure(state=NORMAL)
        cgouttxtbx.insert(INSERT, f"2) Members selected: {memselecchkbx.get()}\n")
        cgouttxtbx.configure(state=DISABLED)

        self.memselecchkbxvar = memselecchkbx.get()

    def confmethodselect():

        cgouttxtbx.configure(state=NORMAL)
        cgouttxtbx.insert(INSERT, f"3) Config Method: {confmethodselec.get()}\n")
        cgouttxtbx.configure(state=DISABLED)
        configmethodvar.set(confmethodselec.get())

    def grpcmdstxtbx():
        global cmdenryvar

        inp = grpdesetry.get(1.0, "end-1c")
        cgouttxtbx.configure(state=NORMAL)
        cgouttxtbx.insert(INSERT, "4) Notes/Commands: " + "\n" + inp)
        cgouttxtbx.configure(state=DISABLED)
        cmdenryvar = inp.splitlines()

    rwindow.grid_columnconfigure(0, weight=1)

    createlabel = ctk.CTkLabel(
        rwindow, text="Create a new Device Group", font=("arial", 22, "bold")
    )
    createlabel.grid(row=0, column=0, sticky=EW, columnspan=3, pady=(20, 16))
    separator1 = ttk.Separator(rwindow, orient="horizontal")
    separator1.grid(row=1, sticky=EW, columnspan=3, padx=20, pady=10)

    grpname = ctk.CTkLabel(rwindow, text="Group name", font=("arial", 18, "bold"))
    grpname.grid(row=2, column=0, sticky=W, padx=25, pady=10)
    grpnameetry = ctk.CTkEntry(
        rwindow,
        font=("arial", 14, "bold"),
        fg_color="yellow2",
        justify="center",
        textvariable=groupname,
    )
    grpnameetry.grid(row=2, column=1, sticky=EW, padx=10, pady=10)
    grpnamebtn = ctk.CTkButton(
        rwindow,
        text="Set",
        command=grpprofilename,
        width=100,
        fg_color="green",
        hover_color="green4",
        font=("arial", 12, "bold"),
    )
    grpnamebtn.grid(row=2, column=2, padx=30, pady=10)
    grpnameetry.configure({"background": "PaleGreen2"})

    memselectlbl = ctk.CTkLabel(
        rwindow, text="Member Selection", font=("arial", 18, "bold"), state=DISABLED
    )
    memselectlbl.grid(row=3, column=0, sticky=W, padx=25, pady=10)
    memselecchkbx = ChecklistCombobox(
        rwindow,
        values=memvaluesdb,
        font=("arial 12 bold"),
        state="disabled",
        checkbutton_height=3,
        height=12,
        style="TCombobox",
    )
    memselecchkbx.grid(row=3, column=1, sticky=EW, padx=10, pady=10)
    memselecbtn = ctk.CTkButton(
        rwindow,
        text="Set",
        command=memselectfun,
        state=DISABLED,
        width=100,
        fg_color="gray",
        hover_color="green4",
        font=("arial", 12, "bold"),
    )
    memselecbtn.grid(row=3, column=2)

    conflbl = ctk.CTkLabel(
        rwindow, text="Config Method", font=("arial", 18, "bold"), state=DISABLED
    )
    conflbl.grid(row=4, column=0, sticky=W, padx=25, pady=10)
    confmethodselec = ctk.CTkComboBox(
        rwindow,
        values=self.cmdcomboboxoptions,
        state="disabled",
        font=("arial", 14, "bold"),
        dropdown_fg_color="PaleGreen2",
        dropdown_hover_color="PaleGreen3",
    )
    confmethodselec.grid(row=4, column=1, sticky=EW, padx=10, pady=10)
    confbtn = ctk.CTkButton(
        rwindow,
        text="Set",
        command=confmethodselect,
        state=DISABLED,
        width=100,
        fg_color="gray",
        hover_color="green4",
        font=("arial", 12, "bold"),
    )
    confbtn.grid(row=4, column=2)

    grpdesclbl = ctk.CTkLabel(
        rwindow, text="Notes", font=("arial", 18, "bold"), state=DISABLED
    )
    grpdesclbl.grid(row=5, column=0, sticky=NW, padx=25, pady=10)

    grpdesetry = scrolledtext.ScrolledText(
        rwindow,
        font="arial 12",
        height=10,
        width=25,
        bg="gray70",
        wrap=WORD,
        state=DISABLED,
    )
    grpdesetry.grid(row=6, column=0, sticky=EW, padx=(25, 10), pady=10, columnspan=2)
    grpdesbtn = ctk.CTkButton(
        rwindow,
        text="Set",
        command=grpcmdstxtbx,
        state=DISABLED,
        width=100,
        fg_color="gray",
        hover_color="green4",
        font=("arial", 12, "bold"),
    )
    grpdesbtn.grid(row=6, column=2, sticky=S, padx=10, pady=10)

    separator2 = ttk.Separator(rwindow, orient="horizontal")
    separator2.grid(row=7, sticky=EW, columnspan=3, padx=20, pady=10)
    btnadd = ctk.CTkButton(
        rwindow,
        text="Add",
        state=DISABLED,
        command=lambda: changegroupfile(self, *args, **kwargs),
        fg_color="gray",
        hover_color="green4",
        font=("arial", 12, "bold"),
    )
    btnadd.grid(column=0, row=8, pady=10)
    btnexit = ctk.CTkButton(
        rwindow,
        text="EXIT",
        command=rwindow.destroy,
        fg_color="red2",
        hover_color="red3",
        font=("arial", 12, "bold"),
    )
    btnexit.grid(column=1, row=8, pady=10, padx=25)
    cgouttxtbx = scrolledtext.ScrolledText(
        rwindow,
        font="arial 10",
        height=10,
        width=25,
        bg="PaleGreen2",
        wrap=WORD,
        state=DISABLED,
    )
    cgouttxtbx.grid(row=9, column=0, sticky=EW, padx=(25, 25), pady=10, columnspan=3)

    creategrpstatuslbl = Label(
        rwindow, text="", font=("arial", 14, "bold"), bg="powder blue", fg="OrangeRed2"
    )
    creategrpstatuslbl.grid(
        row=10, column=0, sticky=W, padx=(30, 20), pady=10, columnspan=3
    )
