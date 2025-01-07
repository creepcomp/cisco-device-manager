from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
from tkinter import scrolledtext
import customtkinter as ctk
import sqlite3
from settings import *
import os
import json
from checklistcombobox import *
from PIL import ImageTk, Image


def editthisgroup(self, *args, **kwargs):
    ewindow = tkinter.Toplevel()
    ewindow.title("Register")
    ewindow.geometry("600x820+200+200")
    ewindow.configure(background="powder blue")
    ewindow.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))

    groupname = StringVar(value="Your Group Name")

    configmethodvar = StringVar()

    global memseleccbxvar
    memseleccbxvar = []

    global memidchkbxvar
    memidchkbxvar = []
    global fvmemselec
    fvmemselec = []

    global methseleccbxvar
    methseleccbxvar = StringVar()

    memvaluesdb = []

    global cmdenryvar
    cmdenryvar = []

    os.chdir(devicegroups)
    items = os.listdir(devicegroups)
    for item in items:
        if os.path.isdir(item):
            memseleccbxvar.append(item)

    def onexitcleanup():

        ewindow.destroy()

    def callchangegroupfile(self, *args, **kwargs):
        if (
            grpnamebtn.cget("state") == DISABLED
            and memselecbtn.cget("state") == DISABLED
            and confbtn.cget("state") == DISABLED
            and grpdesbtn.cget("state") == DISABLED
        ):

            changegroupfile(self, *args, **kwargs)
        else:

            messagebox.showinfo(
                "Please Set changes",
                "Please 'Set' changes to confirm details",
                parent=ewindow,
            )

    def changegroupfile(self, *args, **kwargs):

        groudevicepath = os.path.join(devicegroups, groupname.get())

        dest_path = os.path.join(groudevicepath, groupname.get() + ".json")
        filetoread = open(dest_path)
        inputjsondata = json.load(filetoread)

        inputjsondata["members"] = fvmemselec

        try:

            inputjsondata["method"][0] = confmethodselec.get()

        except:

            try:

                inputjsondata["method"] = confmethodselec.get()
            except Exception as e:
                pass

        else:
            pass

        inputjsondata["commands"] = cmdenryvar

        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(inputjsondata, f, ensure_ascii=False, indent=4)

        filetoread.close()

        btnadd.configure(state="disabled", fg_color="gray")

        editgrpstatuslbl.configure(text="Group Saved")

    def populatemembx(self, *args, **kwargs):

        try:
            sqliteConnection = sqlite3.connect(dbfile)
            cursor = sqliteConnection.cursor()
            query = f"SELECT id FROM devices"
            cursor.execute(query)
            record = cursor.fetchall()
            result_list = [row[0] for row in record]
            result_list = list(map(str, result_list))

            memvaluesdb = result_list

            memselecchkbx.configure(values=memvaluesdb)

        except sqlite3.Error as error:
            pass

    def grpcbxselc():
        global memselecchkbxvar
        global memseleccbxvar

        groupname.set(grpnamecbx.get())

        groudevicepath = os.path.join(devicegroups, groupname.get())

        grpfilepath = os.path.join(groudevicepath, groupname.get() + ".json")

        grpfiletoread = open(grpfilepath)
        grpjsondata = json.load(grpfiletoread)

        memseleccbxvar = grpjsondata["members"]

        cgouttxtbx.configure(state=NORMAL)
        cgouttxtbx.insert(INSERT, f"1) Current Group is : {groupname.get()}\n")
        cgouttxtbx.insert(
            INSERT, f"2) Current Members (memseleccbxvar) are: {memseleccbxvar}\n"
        )

        memselecchkbx.set(memseleccbxvar)

        populatemembx(self, *args, **kwargs)

        methseleccbxvar = grpjsondata["method"]

        cgouttxtbx.insert(INSERT, f"3) Current Method is : {methseleccbxvar}\n")
        confmethodselec.configure(state="normal")
        confmethodselec.set(methseleccbxvar)
        confmethodselec.configure(state="readonly")

        cmdenryvar = grpjsondata["commands"]

        grpdesetry.config(state=NORMAL)
        cmdenryvar1 = "\n".join(cmdenryvar)
        grpdesetry.insert(INSERT, cmdenryvar1)
        cgouttxtbx.insert(INSERT, f"4) Notes : {cmdenryvar}\n")

        grpnamecbx.configure(
            state=DISABLED, fg_color="gray70", text_color_disabled="gray26"
        )
        grpnamebtn.configure(text="Accepted", fg_color="gray", state=DISABLED)

        grpfiletoread.close()

        memselecbtn.configure(state=NORMAL, fg_color="green")
        memselecchkbx.configure(state="readonly")
        memselectlbl.configure(state=NORMAL)
        conflbl.configure(state=NORMAL)
        confbtn.configure(state=NORMAL, fg_color="green")
        confmethodselec.configure(state="readonly", fg_color="pale green")
        grpdesbtn.configure(state=NORMAL, fg_color="green")
        grpdesetry.configure(state=NORMAL)
        grpdesclbl.configure(state=NORMAL)
        grpdesetry.configure(background="light yellow")

        btnadd.configure(state=NORMAL, fg_color="green")

    def memselectfun():
        global memidchkbxvar
        global fvmemselec
        memidchkbxvar = memselecchkbx.get()
        fvmemselec = []

        if memselecchkbx.get() == "":

            cgouttxtbx.insert(
                INSERT, f"2) Remaines Unchanged Current Members: {memseleccbxvar}\n"
            )
            fvmemselec = memseleccbxvar
        else:

            cgouttxtbx.insert(
                INSERT, f"2) Changing Group Current Members to: {memselecchkbx.get()}\n"
            )
            fvmemselec = memselecchkbx.get()

        memselectlbl.configure(state=DISABLED)
        memselecchkbx.configure(state=DISABLED)
        memselecbtn.configure(state=DISABLED, fg_color="gray", text="Accepted")

    def confmethodselect():

        cgouttxtbx.configure(state=NORMAL)
        cgouttxtbx.insert(INSERT, f"3) Config Method: {confmethodselec.get()}\n")
        cgouttxtbx.configure(state=DISABLED)
        configmethodvar.set(confmethodselec.get())

        conflbl.configure(state=DISABLED)
        confmethodselec.configure(
            state=DISABLED, fg_color="gray70", text_color_disabled="gray26"
        )
        confbtn.configure(state=DISABLED, text="Accepted", fg_color="gray")

    def grpcmdstxtbx():
        global cmdenryvar

        inp = grpdesetry.get(1.0, "end-1c")
        cgouttxtbx.config(state=NORMAL)
        cgouttxtbx.insert(INSERT, "4) Commands: " + "\n" + inp)
        cgouttxtbx.config(state=DISABLED)
        cmdenryvar = inp.splitlines()

        grpdesetry.configure(bg="gray70")
        grpdesclbl.configure(state=DISABLED)
        grpdesetry.configure(state=DISABLED)
        grpdesbtn.configure(state=DISABLED, fg_color="gray", text="Accepted")

    style = ttk.Style()
    style.theme_use("clam")
    self.option_add("*TCombobox*Listbox*Background", "pale green")
    self.option_add("*TCombobox*Listbox*Foreground", "black")
    self.option_add("*TCombobox*Listbox*selectBackground", "PaleGreen4")
    self.option_add("*TCombobox*Listbox*selectForeground", "white")
    self.option_add("*TCombobox*Listbox*Font", "Helvetica 10 bold")

    style.map("TCombobox", fieldbackground=[("readonly", "PaleGreen2")])
    style.map("TCombobox", selectbackground=[("readonly", "PaleGreen2")])
    style.map("TCombobox", selectforeground=[("readonly", "black")])
    style.map("TCombobox", selectbackground=[("disabled", "gray20")])

    ewindow.grid_columnconfigure(0, weight=1)

    createlabel = ctk.CTkLabel(
        ewindow, text="Edit a device group", font=("arial", 22, "bold")
    )
    createlabel.grid(row=0, column=0, sticky=EW, columnspan=3, pady=(20, 16))
    separator1 = ttk.Separator(ewindow, orient="horizontal")
    separator1.grid(row=1, sticky=EW, columnspan=3, padx=20, pady=10)

    grpname = ctk.CTkLabel(ewindow, text="Group name", font=("arial", 18, "bold"))
    grpname.grid(row=2, column=0, sticky=W, padx=25, pady=10)
    grpnamecbx = ctk.CTkComboBox(
        ewindow,
        values=memseleccbxvar,
        font=("arial", 14, "bold"),
        fg_color="pale green",
    )
    grpnamecbx.grid(row=2, column=1, sticky=EW, padx=10, pady=10)
    grpnamecbx.set("select Group to edit")
    grpnamebtn = ctk.CTkButton(
        ewindow,
        text="Set",
        command=grpcbxselc,
        width=100,
        fg_color="green",
        hover_color="green4",
    )
    grpnamebtn.grid(row=2, column=2, padx=30, pady=10)

    memselectlbl = Label(
        ewindow,
        text="Member Selection",
        font="arial 14 bold",
        bg="powder blue",
        fg="black",
        state=DISABLED,
    )
    memselectlbl.grid(row=3, column=0, sticky=W, padx=25, pady=10)
    memselecchkbx = ChecklistCombobox(
        ewindow,
        values=memvaluesdb,
        font=("arial 12 bold"),
        state="disabled",
        checkbutton_height=3,
        height=12,
        style="TCombobox",
    )
    memselecchkbx.grid(row=3, column=1, sticky=EW, padx=10, pady=10)
    memselecbtn = ctk.CTkButton(
        ewindow,
        text="Set",
        command=memselectfun,
        state=DISABLED,
        width=100,
        fg_color="gray",
        hover_color="green4",
    )
    memselecbtn.grid(row=3, column=2, padx=30, pady=10)

    conflbl = Label(
        ewindow,
        text="Config Method",
        font="arial 14 bold",
        bg="powder blue",
        fg="black",
        state=DISABLED,
    )
    conflbl.grid(row=4, column=0, sticky=W, padx=25, pady=10)

    confmethodselec = ctk.CTkComboBox(
        ewindow,
        values=self.cmdcomboboxoptions,
        state="disabled",
        font=("arial", 14, "bold"),
    )
    confmethodselec.grid(row=4, column=1, sticky=EW, padx=10, pady=10)
    confbtn = ctk.CTkButton(
        ewindow,
        text="Set",
        command=confmethodselect,
        state=DISABLED,
        width=100,
        fg_color="gray",
        hover_color="green4",
        font=("arial", 12, "bold"),
    )
    confbtn.grid(row=4, column=2, padx=30, pady=10)

    grpdesclbl = Label(
        ewindow,
        text="Notes",
        font="arial 14 bold",
        bg="powder blue",
        fg="black",
        state=DISABLED,
    )
    grpdesclbl.grid(row=5, column=0, sticky=NW, padx=25, pady=10)

    grpdesetry = scrolledtext.ScrolledText(
        ewindow,
        font="arial 12",
        height=10,
        width=25,
        bg="gray70",
        wrap=WORD,
        state=DISABLED,
    )
    grpdesetry.grid(row=6, column=0, sticky=EW, padx=(25, 10), pady=10, columnspan=2)
    grpdesbtn = ctk.CTkButton(
        ewindow,
        text="Set",
        command=grpcmdstxtbx,
        state=DISABLED,
        width=100,
        fg_color="gray",
        hover_color="green4",
        font=("arial", 12, "bold"),
    )
    grpdesbtn.grid(row=6, column=2, sticky=S, padx=30, pady=10)

    separator2 = ttk.Separator(ewindow, orient="horizontal")
    separator2.grid(row=7, sticky=EW, columnspan=3, padx=20, pady=10)
    btnadd = ctk.CTkButton(
        ewindow,
        text="Set changes",
        state=DISABLED,
        width=100,
        fg_color="gray",
        hover_color="green4",
        font=("arial", 12, "bold"),
        command=lambda: callchangegroupfile(self, *args, **kwargs),
    )
    btnadd.grid(column=0, row=8, pady=10)
    btnexit = ctk.CTkButton(
        ewindow,
        text="EXIT",
        width=100,
        fg_color="red2",
        hover_color="red3",
        font=("arial", 12, "bold"),
        command=onexitcleanup,
    )
    btnexit.grid(column=1, row=8, pady=10, padx=25)
    cgouttxtbx = scrolledtext.ScrolledText(
        ewindow,
        font="arial 10",
        height=10,
        width=25,
        bg="PaleGreen2",
        wrap=WORD,
        state=DISABLED,
    )
    cgouttxtbx.grid(row=9, column=0, sticky=EW, padx=(25, 25), pady=10, columnspan=3)

    editgrpstatuslbl = Label(
        ewindow, text="", font=("arial", 14, "bold"), bg="powder blue", fg="OrangeRed2"
    )
    editgrpstatuslbl.grid(
        row=10, column=0, sticky=W, padx=(30, 20), pady=10, columnspan=3
    )

    if grpnamebtn.cget("state") == DISABLED:
        pass
