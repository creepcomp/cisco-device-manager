import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
from settings import *
from PIL import ImageTk, Image


import os


def fetchalldb(self, devtblframea, iam_selecteddevice):
    self.devtblframea

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "db.Treeview", background="pale green", relief="flat", rowheight="25"
    )
    style.configure(
        "db.Treeview.Heading",
        background="PaleGreen3",
        foreground="black",
        font=("Helvetica 10 bold"),
    )
    style.configure(
        "dbgray.Treeview", background="gray60", relief="flat", rowheight="25"
    )
    style.configure(
        "dbgray.Treeview.Heading",
        background="gray50",
        foreground="black",
        font=("Helvetica 10 bold"),
    )
    ttk.Style().map("dbgray.Treeview.Heading", background=[("active", "gray40")])
    ttk.Style().map(
        "Treeview.Heading",
        background=[
            ("pressed", "!focus", "SlateGray3"),
            ("active", "chartreuse3"),
            ("disabled", "#ffffff"),
        ],
    )
    style.map("Treeview", background=[("selected", "PaleGreen4")])

    self.my_canvas = Canvas(self.devtblframea)
    self.my_canvas.pack(side="left", fill=BOTH, expand=1, padx=2, pady=2)
    self.tree = ttk.Treeview(self.my_canvas, selectmode="browse", style="db.Treeview")
    self.tree.pack(side="bottom", fill=BOTH, expand=1)

    self.vsb = ttk.Scrollbar(
        self.devtblframea, orient="vertical", command=self.tree.yview
    )
    self.vsb.pack(side="right", expand=FALSE, fill=BOTH, anchor=NW)

    self.tree.configure(yscrollcommand=self.vsb.set)

    con = sqlite3.connect(dbfile)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM devices")
    rows = cursor.fetchall()
    self.tree["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8")
    self.tree["show"] = "headings"
    self.tree.column("1", width=5, anchor="c")
    self.tree.column("2", width=10, anchor="c")
    self.tree.column("3", width=10, anchor="c")
    self.tree.column("4", width=10, anchor="c")
    self.tree.column("5", width=10, anchor="c")
    self.tree.column("6", width=20, anchor="c")
    self.tree.column("7", width=20, anchor="c")
    self.tree.column("8", width=20, anchor="c")
    self.tree.heading("1", text="id")
    self.tree.heading("2", text="name")
    self.tree.heading("3", text="ip")
    self.tree.heading("4", text="username")
    self.tree.heading("5", text="password")
    self.tree.heading("6", text="description")
    self.tree.heading("7", text="type")
    self.tree.heading("8", text="golden")

    for item in self.tree.get_children():
        self.tree.delete(item)

    for record in rows:
        self.tree.insert(
            "",
            "end",
            iid=record[0],
            values=(
                record[0],
                record[1],
                record[2],
                record[3],
                record[4],
                record[5][:22],
                record[6],
                record[7],
            ),
        )

    firstselec = self.tree.get_children()[0]

    self.tree.selection_set(firstselec)
    cursor.close()
    con.close()

    def selectItem(a):

        try:
            selected_item = self.tree.selection()
            treeview_id = self.tree.item(selected_item)["values"][0]

            self.iam_selecteddevice.set(value=treeview_id)

            self.statusvargrp.set(str(self.iam_selecteddevice.get()))

        except:
            pass

    def rightClickMenu(event):

        def helloedit():

            self.rdwindow = ctk.CTkToplevel()
            self.rdwindow.grab_set()
            changedbdevice(self, self.rdwindow, self.iam_selecteddevice.get())

        def hellodelete():

            deletedbdevice(self, self.iam_selecteddevice.get())

        def hellocreate():

            self.cdwindow = ctk.CTkToplevel()
            self.cdwindow.grab_set()
            createdevice(self, self.cdwindow)

        def hellocreatedir():

            getdevicename = []
            thisdevicename = ""
            getdevicename = self.tree.item(self.tree.focus())
            thisdevicename = getdevicename["values"][1]

            devicepath = os.path.join(devicesaveddata, thisdevicename)

            if not os.path.exists(devicepath):
                os.mkdir(devicepath)

                messagebox.showinfo(
                    parent=self.my_canvas,
                    title="Directory creation",
                    message=f"A directory was created.\n{devicepath}",
                )
                return

            if os.path.exists(devicepath):
                messagebox.showinfo(
                    parent=self.my_canvas,
                    title="Directory creation",
                    message=f"Directory already exists.\n(no creation necessary)\n{devicepath}",
                )
                return

        rowID = self.tree.identify("item", event.x, event.y)
        self.tree.identify_row(event.y)
        getdevicename = self.tree.item(self.tree.focus())
        thisdevicename = getdevicename["values"][1]

        if rowID:
            menu = Menu(self.devtblframea, tearoff=0)
            menu.add_separator()
            menu.add_command(
                label=f"Edit id:{rowID} ({thisdevicename})", command=helloedit
            )
            menu.add_command(
                label=f"Delete id:{rowID} ({thisdevicename})", command=hellodelete
            )
            menu.add_separator()
            menu.add_command(
                label=f"Create directory id:{rowID} ({thisdevicename})",
                command=hellocreatedir,
            )
            menu.add_separator()
            menu.add_command(label=f"Create new device", command=hellocreate)

            self.tree.selection_set(rowID)
            self.tree.focus_set()
            self.tree.focus(rowID)

            menu.tk_popup(event.x_root, event.y_root)
            self.vsb.update()
        else:
            pass

    self.treebind = self.tree.bind("<<TreeviewSelect>>", selectItem)
    self.tree.bind("<Button-3>", rightClickMenu)


def clear_all(self):

    try:
        for item in self.tree.get_children():
            self.tree.delete(item)
            self.tree.forget()
            self.vsb.forget()
            self.my_canvas.forget()
    except:
        pass

    finally:

        fetchalldb(self, self.devtblframea, self.iam_selecteddevice)


def createdevice(self, cdwindow):
    self.rname = StringVar(self)
    self.rip = StringVar(self)
    self.rusername = StringVar(self)
    self.rpassword = StringVar(self)
    self.rdescription = StringVar(self)
    self.rtype = StringVar(self)
    self.rgfilename = StringVar(self)

    self.cdwindow.title("Register (createdevice)")
    self.cdwindow.geometry("500x720+200+200")
    self.cdwindow.attributes("-topmost", "true")
    self.cdwindow.configure(fg_color="light blue")

    self.cdwindow.after(
        250,
        lambda: self.cdwindow.wm_iconphoto(
            False, (ImageTk.PhotoImage(Image.open(pythonicon)))
        ),
    )
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self.createlabel = ctk.CTkLabel(
        self.cdwindow, text="Create a new device", font=("arial", 22, "bold")
    )
    self.createlabel.grid(row=0, column=0, sticky="ew", columnspan=3, pady=15)
    self.separator1 = ttk.Separator(self.cdwindow, orient="horizontal")
    self.separator1.grid(row=1, sticky="ew", columnspan=3, padx=(30, 30), pady=10)

    self.dbname = ctk.CTkLabel(
        self.cdwindow, text="Device name", font=("arial", 18, "bold"), justify="left"
    )
    self.dbname.grid(row=2, column=0, sticky="w", padx=(30, 10), pady=10)
    self.ebdbname = ctk.CTkEntry(
        self.cdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.rname,
    )
    self.ebdbname.grid(row=2, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbip = ctk.CTkLabel(
        self.cdwindow, text="IP Address", font=("arial", 18, "bold"), justify="left"
    )
    self.dbip.grid(row=3, column=0, sticky="w", padx=(30, 10), pady=10)
    self.ebdbip = ctk.CTkEntry(
        self.cdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.rip,
    )
    self.ebdbip.grid(row=3, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbusername = ctk.CTkLabel(
        self.cdwindow, text="Username", font=("arial", 18, "bold"), justify="left"
    )
    self.dbusername.grid(row=4, column=0, sticky="w", padx=(30, 10), pady=10)
    self.ebdbusername = ctk.CTkEntry(
        self.cdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.rusername,
    )
    self.ebdbusername.grid(row=4, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbpassword = ctk.CTkLabel(
        self.cdwindow, text="Password", font=("arial", 18, "bold"), justify="left"
    )
    self.dbpassword.grid(row=5, column=0, sticky="w", padx=(30, 10), pady=10)
    self.ebdbpassword = ctk.CTkEntry(
        self.cdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.rpassword,
    )
    self.ebdbpassword.grid(row=5, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbdescription = ctk.CTkLabel(
        self.cdwindow, text="Description", font=("arial", 18, "bold"), justify="left"
    )
    self.dbdescription.grid(row=6, column=0, sticky="nw", padx=(30, 10), pady=10)
    self.ebdbdescription = ctk.CTkTextbox(
        self.cdwindow,
        font=("arial", 14),
        height=200,
        width=230,
        fg_color="light yellow",
        border_width=2,
        wrap="word",
    )
    self.ebdbdescription.grid(row=6, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbtype = ctk.CTkLabel(
        self.cdwindow, text="Type", font=("arial", 18, "bold"), justify="left"
    )
    self.dbtype.grid(row=7, column=0, sticky="w", padx=(30, 10), pady=10)
    self.ebdbtype = ctk.CTkEntry(
        self.cdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.rtype,
    )
    self.ebdbtype.grid(row=7, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbgfilename = ctk.CTkLabel(
        self.cdwindow,
        text="Goldern filename",
        font=("arial", 18, "bold"),
        justify="left",
        text_color="gray",
    )
    self.dbgfilename.grid(row=8, column=0, sticky="w", padx=(30, 10), pady=10)
    self.btnfile = ctk.CTkButton(
        self.cdwindow,
        state="disabled",
        text="File select",
        font=("arial", 14),
        fg_color="gray",
        text_color="black",
    )
    self.btnfile.grid(row=8, column=1, pady=10, padx=(30, 30))
    self.ebdbgfilename = ctk.CTkEntry(
        self.cdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.rgfilename,
    )
    self.ebdbgfilename.grid(
        row=9, column=0, sticky="ew", padx=(30, 30), pady=10, columnspan=2
    )

    self.rgfilename.set(value="'Edit' device after creation")
    self.ebdbgfilename.configure(state="disabled", fg_color="gray70")

    self.separator2 = ttk.Separator(self.cdwindow, orient="horizontal")
    self.separator2.grid(row=10, sticky="ew", columnspan=3, padx=(30, 30), pady=10)
    self.btngo = ctk.CTkButton(
        self.cdwindow,
        text="Create",
        font=("arial", 14, "bold"),
        fg_color="green3",
        hover_color="green4",
        border_color="green4",
        border_width=2,
        text_color="black",
        command=lambda: insertdevice(self),
    )
    self.btngo.grid(row=11, column=0, pady=10, padx=30, sticky="w")
    self.btnexit = ctk.CTkButton(
        self.cdwindow,
        text="EXIT",
        font=("arial", 14, "bold"),
        fg_color="orange red",
        hover_color="OrangeRed3",
        text_color="black",
        border_width=2,
        border_color="OrangeRed3",
        command=self.cdwindow.destroy,
    )
    self.btnexit.grid(row=11, column=1, pady=10, padx=30, sticky="e")
    self.lblcds = ctk.CTkLabel(
        self.cdwindow, text="", font=("arial", 18, "bold"), justify="left"
    )
    self.lblcds.grid(row=12, column=0, pady=10, padx=(30, 10), columnspan=2)

    def insertdevice(self):

        self.btngo.configure(state="disabled", fg_color="gray", border_color="gray")

        try:
            sqliteConnection = sqlite3.connect(dbfile)
            cursor = sqliteConnection.cursor()

            query = "INSERT INTO devices (id,name,ip,username,password,description,type,golden) VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(
                query,
                (
                    str(self.ebdbname.get()),
                    str(self.ebdbip.get()),
                    str(self.ebdbusername.get()),
                    str(self.ebdbpassword.get()),
                    str(self.ebdbdescription.get("1.0", "end-1c")),
                    str(self.ebdbtype.get()),
                    str(self.ebdbgfilename.get()),
                ),
            )
            sqliteConnection.commit()
        except sqlite3.Error as error:
            self.lblcds.configure(text_color="red")
            self.lblcds.configure(text=f"Creation error: {error}")

        finally:

            if sqliteConnection:
                sqliteConnection.close()

            self.ebdbname.configure(state="disabled", fg_color="light gray")
            self.ebdbip.configure(state="disabled", fg_color="light gray")
            self.ebdbusername.configure(state="disabled", fg_color="light gray")
            self.ebdbpassword.configure(state="disabled", fg_color="light gray")
            self.ebdbdescription.configure(state="disabled", fg_color="light gray")
            self.ebdbtype.configure(state="disabled", fg_color="light gray")
            self.ebdbgfilename.configure(state="disabled", fg_color="light gray")
            self.dbname.configure(text_color="gray40")
            self.dbip.configure(text_color="gray40")
            self.dbusername.configure(text_color="gray40")
            self.dbpassword.configure(text_color="gray40")
            self.dbdescription.configure(text_color="gray40")
            self.dbtype.configure(text_color="gray40")
            self.dbgfilename.configure(text_color="gray40")

            self.lblcds.configure(
                text=" Device has been created. ",
                text_color="green4",
                bg_color="yellow2",
            )

            clear_all(self)

        try:

            devicepath = os.path.join(devicesaveddata, self.rname.get())
            if not os.path.exists(devicepath):
                os.mkdir(devicepath)

        except Exception as error:
            pass

        finally:
            pass


def changedbdevice(self, rdwindow, iam_selecteddevice):

    self.rdwindow.title("Update device details")
    self.rdwindow.geometry("500x740+200+200")
    self.rdwindow.attributes("-topmost", "true")
    self.rdwindow.configure(fg_color="light blue")
    self.rdwindow.after(
        250,
        lambda: self.rdwindow.wm_iconphoto(
            False, (ImageTk.PhotoImage(Image.open(pythonicon)))
        ),
    )
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self.result_id = 0

    self.changername = StringVar(self)

    self.changerip = StringVar(self)

    self.changerusername = StringVar(self)
    self.changerpassword = StringVar(self)
    self.changerdescription = StringVar(self)
    self.changertype = StringVar(self)

    self.rgfilename = tk.StringVar(self)

    self.createlabel = ctk.CTkLabel(
        self.rdwindow, text="Change device (id:", font=("arial", 22, "bold")
    )
    self.createlabel.grid(row=0, column=0, sticky="ew", columnspan=3, pady=(18, 8))
    self.separator1 = ttk.Separator(self.rdwindow, orient="horizontal")
    self.separator1.grid(row=1, sticky="ew", columnspan=3, padx=(30, 30), pady=10)
    self.createlabel.configure(
        text=self.createlabel.cget("text") + str(iam_selecteddevice) + ")"
    )

    self.dbname = ctk.CTkLabel(
        self.rdwindow, text="Device name", font=("arial", 18, "bold"), justify="left"
    )
    self.dbname.grid(row=2, column=0, sticky="w", padx=(30, 10), pady=10)
    self.ebdbname = ctk.CTkEntry(
        self.rdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.changername,
    )
    self.ebdbname.grid(row=2, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbip = ctk.CTkLabel(
        self.rdwindow, text="IP Address", font=("arial", 18, "bold"), justify="left"
    )
    self.dbip.grid(row=3, column=0, sticky="w", padx=(30, 10), pady=10)
    self.ebdbip = ctk.CTkEntry(
        self.rdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.changerip,
    )
    self.ebdbip.grid(row=3, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbusername = ctk.CTkLabel(
        self.rdwindow, text="Username", font=("arial", 18, "bold"), justify="left"
    )
    self.dbusername.grid(row=4, column=0, sticky="w", padx=(30, 10), pady=10)
    self.ebdbusername = ctk.CTkEntry(
        self.rdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.changerusername,
    )
    self.ebdbusername.grid(row=4, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbpassword = ctk.CTkLabel(
        self.rdwindow, text="Password", font=("arial", 18, "bold"), justify="left"
    )
    self.dbpassword.grid(row=5, column=0, sticky="w", padx=(30, 10), pady=10)
    self.ebdbpassword = ctk.CTkEntry(
        self.rdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.changerpassword,
    )
    self.ebdbpassword.grid(row=5, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbdescription = ctk.CTkLabel(
        self.rdwindow, text="Description", font=("arial", 18, "bold"), justify="left"
    )
    self.dbdescription.grid(row=6, column=0, sticky="nw", padx=(30, 10), pady=10)
    self.ebdbdescription = ctk.CTkTextbox(
        self.rdwindow,
        font=("arial", 14),
        height=200,
        width=230,
        fg_color="light yellow",
        border_width=2,
        wrap="word",
    )
    self.ebdbdescription.grid(row=6, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbtype = ctk.CTkLabel(
        self.rdwindow, text="Type", font=("arial", 18, "bold"), justify="left"
    )
    self.dbtype.grid(row=7, column=0, sticky="w", padx=(30, 10), pady=10)
    self.ebdbtype = ctk.CTkEntry(
        self.rdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.changertype,
    )
    self.ebdbtype.grid(row=7, column=1, sticky="w", padx=(30, 30), pady=10)

    self.dbgfilename = ctk.CTkLabel(
        self.rdwindow,
        text="Golden config file",
        font=("arial", 18, "bold"),
        justify="left",
    )
    self.dbgfilename.grid(row=8, column=0, sticky="ew", padx=(30, 10), pady=10)
    self.btnfile = ctk.CTkButton(
        self.rdwindow,
        text="File select",
        font=("arial", 14),
        text_color="white",
        fg_color="purple3",
        hover_color="purple4",
        border_color="purple4",
        border_width=2,
        command=lambda: filedialogopen(self),
    )
    self.btnfile.grid(row=8, column=1, pady=10, padx=40)
    self.ebdbgfilename = ctk.CTkEntry(
        self.rdwindow,
        font=("arial", 14),
        justify="center",
        width=230,
        fg_color="light yellow",
        textvariable=self.rgfilename,
    )
    self.ebdbgfilename.grid(
        row=9, column=0, sticky="ew", padx=(30, 30), pady=10, columnspan=2
    )
    self.ebdbgfilename.configure(state="disabled")

    self.separator2 = ttk.Separator(self.rdwindow, orient="horizontal")
    self.separator2.grid(row=10, sticky="ew", columnspan=3, padx=(30, 30), pady=10)
    self.btngo = ctk.CTkButton(
        self.rdwindow,
        text="Change",
        font=("arial", 14, "bold"),
        fg_color="green3",
        hover_color="green4",
        border_color="green4",
        border_width=2,
        text_color="black",
        command=lambda: dbconnectRegister(self, iam_selecteddevice),
    )
    self.btngo.grid(row=11, column=0, pady=10, padx=(30, 10))
    self.btnexit = ctk.CTkButton(
        self.rdwindow,
        text="EXIT",
        font=("arial", 14, "bold"),
        fg_color="orange red",
        hover_color="OrangeRed3",
        text_color="black",
        border_width=2,
        border_color="OrangeRed3",
        command=self.rdwindow.destroy,
    )
    self.btnexit.grid(row=11, column=1, pady=10, padx=(30, 10))
    self.lblcds = ctk.CTkLabel(
        self.rdwindow, text="", font=("arial", 18, "bold"), justify="left"
    )
    self.lblcds.grid(row=12, column=0, pady=10, padx=(30, 10), columnspan=2)

    def filedialogopen(self):

        basefiledirectory = f"{devicesaveddata}" + f"{self.changername.get()}"

        getfile = askopenfilename(
            parent=self.rdwindow,
            title="Base File selection",
            initialdir=basefiledirectory,
        )

        if len(getfile) == 0:

            return

        filebase = os.path.basename(getfile)

        self.rgfilename.set(filebase)

    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()

        query = "SELECT * FROM devices WHERE id = '%s'" % (iam_selecteddevice)
        cursor.execute(query)
        results = cursor.fetchall()

        self.result_id = results[0][0]

        self.changername.set(str(results[0][1]))

        self.changerip.set(str(results[0][2]))
        self.changerusername.set(str(results[0][3]))
        self.changerpassword.set(str(results[0][4]))
        self.changerdescription.set(str(results[0][5]))
        self.changertype.set(str(results[0][6]))
        self.rgfilename.set(str(results[0][7]))

    except sqlite3.Error as error:
        self.lblcds.configure(text_color="red")
        self.lblcds.configure(text=f"Change request error: {error}")

    self.ebdbdescription.insert("1.0", self.changerdescription.get())


def dbconnectRegister(self, iam_selecteddevice):

    self.btngo.configure(state="disabled", fg_color="gray", border_color="gray")

    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        cursor.fetchall()

        query = "UPDATE devices SET name = ?, ip = ?, username = ?, password = ?, description = ?, type = ?, golden = ? WHERE id = ?"
        inputs = (
            self.ebdbname.get(),
            self.ebdbip.get(),
            self.ebdbusername.get(),
            self.ebdbpassword.get(),
            self.ebdbdescription.get("1.0", "end-1c"),
            self.ebdbtype.get(),
            self.ebdbgfilename.get(),
            self.result_id,
        )
        cursor.execute(query, inputs)
        sqliteConnection.commit()

    except sqlite3.Error as error:
        pass

    finally:
        if sqliteConnection:
            sqliteConnection.close()

            self.ebdbname.configure(state="disabled", fg_color="light gray")
            self.ebdbip.configure(state="disabled", fg_color="light gray")
            self.ebdbusername.configure(state="disabled", fg_color="light gray")
            self.ebdbpassword.configure(state="disabled", fg_color="light gray")
            self.ebdbdescription.configure(state="disabled", fg_color="light gray")
            self.ebdbtype.configure(state="disabled", fg_color="light gray")
            self.ebdbgfilename.configure(state="disabled", fg_color="light gray")
            self.dbname.configure(text_color="gray40")
            self.dbip.configure(text_color="gray40")
            self.dbusername.configure(text_color="gray40")
            self.dbpassword.configure(text_color="gray40")
            self.dbdescription.configure(text_color="gray40")
            self.dbtype.configure(text_color="gray40")
            self.dbgfilename.configure(text_color="gray40")
            self.btnfile.configure(
                state="disabled", fg_color="gray", border_color="gray"
            )

            self.lblcds.configure(
                text=f" Device (id:{iam_selecteddevice}) has been changed. ",
                text_color="green4",
                bg_color="yellow2",
            )

            clear_all(self)


def deletedbdevice(self, iam_selecteddevice):

    self.deletemsgbox = messagebox.askquestion(
        title=f"Delete ? (id:{iam_selecteddevice})",
        message=f"Please confirm that you want to delete entry id:{iam_selecteddevice}",
        icon="warning",
    )
    if self.deletemsgbox == "yes":
        try:

            sqliteConnection = sqlite3.connect(dbfile)
            cursor = sqliteConnection.cursor()

            query = ("DELETE FROM devices WHERE id = '%s'") % (iam_selecteddevice)
            cursor.execute(query)
            sqliteConnection.commit()

            messagebox.showinfo(
                title="Return",
                message=f"The record with id:{iam_selecteddevice} was deleted.",
            )
        except sqlite3.Error as error:
            messagebox.showinfo(title="Return", message=f"Problem occured: {error}")

        finally:
            if sqliteConnection:
                sqliteConnection.close()

            clear_all(self)

    else:
        messagebox.showinfo(
            title="Request Canceled",
            message=f"You canceled the request.\n id:{iam_selecteddevice} remains in the list.",
        )
