from settings import *
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import *
from PIL import ImageTk, Image
from devicecrud import fetchalldb, createdevice, changedbdevice, deletedbdevice
from cmdframebox import showcmdframe
from filesdb import saveframeoutput
from sshservices import (
    runcmdparamiko,
    runcmdnetmiko,
    runcmdnetmiko_ch,
    runcmdnetmiko_ch_config,
)
from sshservicesgrp import runcmdparamikogrp, runcmdnetmikogrp, runcmdnetmikogrp_ch
from creategroup import createnewgroup
import os
from editgroups import editthisgroup
from deletegroup import delgroup
from backuptftp import tftpdevicebackup
from backuptftpgrp import backupgrouptftp
from uploadtftp import configuploadtftp
from uploadtftpgroup import configuploadtftpgroup


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Cisco Manager (Developed by: Parsa Rostamzadeh)")
        self.geometry("1400x750+50+50")
        self.resizable(True, True)
        self.minsize(1100, 550)
        self.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))

        self.iam_selecteddevice = tk.IntVar(self)

        self.devicestatus = tk.StringVar(self, value=f"Device ID: ")

        self.statusvargrp = tk.StringVar(self)

        self.groupswitch_var = tk.StringVar(value="on")
        self.statusvarcmd = tk.StringVar(self, value="(Unselected)")
        self.statusvarcmd2 = tk.StringVar(self, value="(Unselected)")

        self.groupcomboboxoptions = []
        self.groupoptionselected = tk.StringVar(self)

        self.cmdcomboboxoptions = [
            "Paramiko",
            "Netmiko",
            "Netmiko_ch",
            "Netmiko_ch_config",
            "Another ?",
        ]
        self.cmdmethodselected = tk.StringVar(self)

        self.cmdvarselected = tk.StringVar(self)

        self.returnedname = tk.StringVar(self)

        def createnewdevice(self):
            self.cdwindow = ctk.CTkToplevel()

            createdevice(self, self.cdwindow)

        def changethisdevice(self):

            self.rdwindow = ctk.CTkToplevel()

            changedbdevice(self, self.rdwindow, self.iam_selecteddevice.get())

        def deletethisdevice(self):

            deletedbdevice(self, self.iam_selecteddevice.get())

        def groupswitch_event(self):

            self.groupcomboboxoptions = []
            listgroupnames(self)

            if self.groupswitch_var.get() == "on":
                self.devicestatus.set("Selected Group : ")
                self.statusvargrp.set(self.grpcombobox.get())
                self.iam_selecteddevice.set(0)

                self.grpcombobox.configure(state="readonly")
                self.grpcombobox.configure(fg_color="yellow2")
                self.grpcombobox.configure(values=self.groupcomboboxoptions)
                self.groupoptionselected.set(self.grpcombobox.get())
                self.createa.configure(state="disabled")
                self.updatea.configure(state="disabled")
                self.deletea.configure(state="disabled")

                self.tree.bind("<Button-1>", "break")
                self.tree.bind("<MouseWheel>", "break")
                self.vsb.config(command="")
                style = ttk.Style()
                style.configure(
                    "db.Treeview", background="gray64", relief="flat", rowheight="25"
                )
                style.configure(
                    "db.Treeview.Heading",
                    background="gray64",
                    foreground="black",
                    font=("Helvetica 10 bold"),
                )
                style.map("Treeview", background=[("selected", "gray45")])
                self.tree.bind("<Button-3>", "break")

            else:

                self.devicestatus.set(f"Device ID: ")
                self.grpcombobox.configure(state="disabled")
                self.grpcombobox.configure(fg_color="light goldenrod yellow")

                self.iam_selecteddevice.set(
                    self.tree.item(self.tree.selection())["values"][0]
                )

                self.createa.configure(state="normal")
                self.updatea.configure(state="normal")
                self.deletea.configure(state="normal")

                self.tree.unbind("<Button-1>")
                self.tree.unbind("<MouseWheel>")
                self.vsb.config(command=self.tree.yview)

                style = ttk.Style()
                style.theme_use("clam")
                style.configure(
                    "db.Treeview",
                    background="pale green",
                    relief="flat",
                    rowheight="25",
                )
                style.configure(
                    "db.Treeview.Heading",
                    background="PaleGreen3",
                    foreground="black",
                    font=("Helvetica 10 bold"),
                )
                style.map("Treeview", background=[("selected", "PaleGreen4")])

                self.option_add("*TCombobox*Listbox*Background", "pale green")
                self.option_add("*TCombobox*Listbox*Foreground", "black")
                self.option_add("*TCombobox*Listbox*selectBackground", "PaleGreen4")
                self.option_add("*TCombobox*Listbox*selectForeground", "white")
                self.option_add("*TCombobox*Listbox*Font", "Helvetica 10 bold")

                style.map("TCombobox", fieldbackground=[("readonly", "PaleGreen2")])
                style.map("TCombobox", selectbackground=[("readonly", "PaleGreen2")])
                style.map("TCombobox", selectforeground=[("readonly", "black")])

                style.map("TCombobox", selectbackground=[("disabled", "gray20")])

        def runcmdselection(self):

            if self.groupswitch_var.get() == "off":

                if self.cmdmethodselected.get() == "Paramiko":

                    runcmdparamiko(self, self.iam_selecteddevice.get())
                if self.cmdmethodselected.get() == "Netmiko":

                    runcmdnetmiko(self, self.iam_selecteddevice.get())
                if self.cmdmethodselected.get() == "Netmiko_ch":

                    runcmdnetmiko_ch(self, self.iam_selecteddevice.get())
                if self.cmdmethodselected.get() == "Netmiko_ch_config":

                    runcmdnetmiko_ch_config(self, self.iam_selecteddevice.get())

            elif self.groupswitch_var.get() == "on":

                if self.cmdmethodselected.get() == "Paramiko":

                    runcmdparamikogrp(
                        self, self.groupoptionselected.get(), self.cmdvarselected.get()
                    )
                if self.cmdmethodselected.get() == "Netmiko":

                    runcmdnetmikogrp(
                        self, self.groupoptionselected.get(), self.cmdvarselected.get()
                    )
                if self.cmdmethodselected.get() == "Netmiko_ch":

                    runcmdnetmikogrp_ch(
                        self, self.groupoptionselected.get(), self.cmdvarselected.get()
                    )
                if self.cmdmethodselected.get() == "Netmiko_ch_config":

                    runcmdnetmikogrp_ch(self, self.groupoptionselected.get())

            else:
                pass

        def newgroup():

            createnewgroup(self, *args, **kwargs)

        def editgroup():

            editthisgroup(self, *args, **kwargs)

        def deletegroup():

            delgroup(self)

        def listgroupnames(self):
            os.chdir(directorypathroot)

            os.chdir(devicegroups)

            items = os.listdir(devicegroups)
            for item in items:
                if os.path.isdir(item):
                    self.groupcomboboxoptions.append(item)

        def groupcombobox_callback(choice):

            self.groupoptionselected.set(choice)
            self.statusvargrp.set(choice)

        def cmdcombobox_callback(choice):

            self.cmdmethodselected.set(choice)
            self.statusvarcmd.set(choice)
            showcmdframe(self, choice, *args, **kwargs)

        def tftpconfig():

            tftpdevicebackup(self)

        def tftpconfiggrp():

            backupgrouptftp(self)

        def tftupload():

            configuploadtftp(self)

        def tftprestoregroup():

            configuploadtftpgroup(self)

        listgroupnames(self)

        myMenu1 = Menu(self)
        self.config(menu=myMenu1)

        fileMenu = Menu(myMenu1, tearoff=0)
        myMenu1.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)

        deviceMenu = Menu(myMenu1, tearoff=0)
        myMenu1.add_cascade(label="Devices", menu=deviceMenu)
        deviceMenu.add_command(
            label="Create a new Device", command=lambda: createnewdevice(self)
        )
        deviceMenu.add_separator()
        deviceMenu.add_command(
            label="Edit an exsisting Device", command=lambda: changethisdevice(self)
        )
        deviceMenu.add_command(
            label="Delete selected Device", command=lambda: deletethisdevice(self)
        )

        grpMenu = Menu(myMenu1, tearoff=0)
        myMenu1.add_cascade(label="Device Groups", menu=grpMenu)
        grpMenu.add_command(label="Create a new Group", command=newgroup)
        grpMenu.add_separator()
        grpMenu.add_command(label="Edit an exsisting Group", command=editgroup)
        grpMenu.add_command(label="Delete a Group", command=deletegroup)

        tftpMenu = Menu(myMenu1, tearoff=0)
        myMenu1.add_cascade(label="TFTP Backup & Restore", menu=tftpMenu)
        tftpMenu.add_command(label="Backup Device (TFTP)", command=tftpconfig)
        tftpMenu.add_command(label="Restore Device (TFTP)", command=tftupload)
        tftpMenu.add_separator()
        tftpMenu.add_command(label="Backup Group (TFTP)", command=tftpconfiggrp)
        tftpMenu.add_command(label="Restore Group (TFTP)", command=tftprestoregroup)

        def topFrame(self):
            self.topframemain = ctk.CTkFrame(self, height=40)
            self.topframemain.pack(fill="x", side="top")
            self.topframemain.pack_propagate(False)

            self.topframea = ctk.CTkFrame(
                self.topframemain, height=40, fg_color="PaleGreen3"
            )
            self.topframea.pack(fill="x", expand=True, side="left")
            self.topframea.pack_propagate(False)

            self.topframeb = ctk.CTkFrame(
                self.topframemain, height=40, fg_color="lightblue"
            )
            self.topframeb.pack(fill="x", expand=True, side="left")
            self.topframeb.pack_propagate(False)

            self.createa = ctk.CTkButton(
                self.topframea,
                text="Create",
                width=75,
                command=lambda: createnewdevice(self),
                fg_color="dark slate gray",
                font=("arial", 12, "bold"),
                hover_color="Gray24",
                border_width=3,
                border_color="dark slate gray",
            )
            self.createa.pack(side="left", padx=5)
            self.updatea = ctk.CTkButton(
                self.topframea,
                text="Update",
                width=75,
                command=lambda: changethisdevice(self),
                fg_color="dark slate gray",
                font=("arial", 12, "bold"),
                hover_color="Gray24",
                border_width=3,
                border_color="dark slate gray",
            )
            self.updatea.pack(side="left", padx=5)
            self.deletea = ctk.CTkButton(
                self.topframea,
                text="Delete",
                width=75,
                command=lambda: deletethisdevice(self),
                fg_color="dark slate gray",
                font=("arial", 12, "bold"),
                hover_color="Gray24",
                border_width=3,
                border_color="dark slate gray",
            )
            self.deletea.pack(side="left", padx=5)

            self.grpcombobox = ctk.CTkComboBox(
                self.topframea,
                width=170,
                height=20,
                font=("arial", 14, "bold"),
                command=groupcombobox_callback,
                dropdown_fg_color="khaki",
                dropdown_hover_color="khaki3",
                border_color="dark slate gray",
                button_color="dark slate gray",
            )
            self.grpcombobox.pack(side="right", pady=5, padx=10)
            self.grpcombobox.set("Group Selection")
            self.grpcombobox.configure(state="disabled")

            self.groupswitch = ctk.CTkSwitch(
                self.topframea,
                text="Group Switch",
                command=lambda: groupswitch_event(self),
                variable=self.groupswitch_var,
                onvalue="on",
                offvalue="off",
                switch_width=40,
                switch_height=20,
                fg_color="khaki2",
                button_color="dark slate gray",
                border_width=2,
                border_color="dark slate gray",
                progress_color="yellow",
            )
            self.groupswitch.pack(side="right", pady=10, padx=(10, 10))

            self.lblcmd = ctk.CTkLabel(self.topframeb, text=" CMD select: ").pack(
                side="left", padx=10
            )

            self.cmdcombobox = ctk.CTkComboBox(
                self.topframeb,
                width=170,
                height=20,
                values=self.cmdcomboboxoptions,
                font=("arial", 14, "bold"),
                fg_color="yellow2",
                command=cmdcombobox_callback,
                dropdown_fg_color="khaki",
                dropdown_hover_color="khaki3",
                border_color="dark slate gray",
                button_color="dark slate gray",
                button_hover_color="dark green",
            )
            self.cmdcombobox.pack(side="left", pady=5, padx=10)
            self.cmdcombobox.set("Method Selection")

            def copy_select():
                global cmddata
                if self.cmdtxtbox.selection_get():
                    cmddata = self.cmdtxtbox.selection_get()

                    self.clipboard_clear()
                    self.clipboard_append(cmddata)

            def paste_select():
                global data
                self.cmdtxtbox.insert(tk.END, self.clipboard_get())

            self.btncopy = ctk.CTkButton(
                self.topframeb, text="Paste", width=30, command=lambda: paste_select()
            )
            self.btncopy.pack(side="right", padx=5)
            self.btnpaste = ctk.CTkButton(
                self.topframeb, text="Copy", width=30, command=lambda: copy_select()
            )
            self.btnpaste.pack(side="right", padx=5)

            self.btncopy.configure(state="disabled")
            self.btnpaste.configure(state="disabled")

            self.btnrun = ctk.CTkButton(
                self.topframeb,
                text="Run",
                width=130,
                fg_color="green4",
                hover_color="green",
                text_color="white",
                font=("arial", 14, "bold"),
                border_width=2,
                border_color="dark green",
                command=lambda: runcmdselection(self),
            )
            self.btnrun.pack(pady=7)

        def dataframe(self):
            self.dataframemain = ctk.CTkFrame(
                master=self, height=259, fg_color="gray64"
            )
            self.dataframemain.pack(fill="x", side="top")
            self.dataframemain.pack_propagate(False)

            self.devtblframea = ctk.CTkFrame(self.dataframemain, fg_color="green4")
            self.devtblframea.pack(fill="both", expand=True, side="left")
            self.devtblframea.pack_propagate(False)

            self.cmdframea = ctk.CTkFrame(
                self.dataframemain, height=100, fg_color="gray64"
            )
            self.cmdframea.pack(fill="both", expand=True, side="left")
            self.cmdframea.pack_propagate(False)

            self.lblcmdframea = ctk.CTkLabel(self.cmdframea, text="cmdframea").pack()

        def dataoutput(self):
            self.dataoutputa = ctk.CTkFrame(master=self, height=565, fg_color="gray64")
            self.dataoutputa.pack(fill="both", expand=True, side="bottom")
            self.dataoutputa.pack_propagate(False)

            self.dataoutputb = ctk.CTkFrame(
                self.dataoutputa, height=40, fg_color="gray64"
            )
            self.dataoutputb.pack(fill="x", expand=False, side="bottom")
            self.dataoutputb.pack_propagate(False)

            self.txtcontent = scrolledtext.ScrolledText(
                self.dataoutputa, wrap=WORD, background="light goldenrod yellow"
            )
            self.txtcontent.pack(expand=TRUE, fill="both", padx=2, pady=2)
            self.txtcontent.pack_propagate(0)

            self.btnsaveoutput = ctk.CTkButton(
                self.dataoutputb,
                text="Save output",
                width=135,
                fg_color="dark slate gray",
                command=lambda: saveframeoutput(self),
                font=("arial", 12, "bold"),
                hover_color="Gray24",
                border_width=3,
                border_color="dark slate gray",
            )
            self.btnsaveoutput.pack(side="left", padx=5)
            self.btnclearoutput = ctk.CTkButton(
                self.dataoutputb,
                text="Clear",
                width=105,
                fg_color="dark slate gray",
                command=lambda: self.txtcontent.delete("1.0", END),
                font=("arial", 12, "bold"),
                hover_color="Gray24",
                border_width=3,
                border_color="dark slate gray",
            )
            self.btnclearoutput.pack(side="left", padx=5)

            self.lbldevicestatus = ctk.CTkLabel(
                self.dataoutputb, textvariable=self.devicestatus
            ).pack(side="left", padx=(20, 5))
            self.lblstatusoutputgrp = ctk.CTkLabel(
                self.dataoutputb, textvariable=self.statusvargrp
            ).pack(side="left", padx=(5, 5))
            self.lblstatuscmd = ctk.CTkLabel(
                self.dataoutputb, text=" | Run Method: "
            ).pack(side="left", padx=(5, 5))
            self.lblstatusoutputcmd = ctk.CTkLabel(
                self.dataoutputb, textvariable=self.statusvarcmd
            ).pack(side="left", padx=(5, 20))
            self.lblstatuscmd2 = ctk.CTkLabel(
                self.dataoutputb, text=" | Run Command: "
            ).pack(side="left", padx=(5, 20))
            self.lblstatusoutputcmd2 = ctk.CTkLabel(
                self.dataoutputb, textvariable=self.statusvarcmd2
            ).pack(side="left")

            self.btnexit = ctk.CTkButton(
                self.dataoutputb,
                text="Exit",
                width=85,
                fg_color="red3",
                command=self.destroy,
                font=("arial", 12, "bold"),
                hover_color="red4",
                border_width=2,
                border_color="red4",
            )
            self.btnexit.pack(side="right", padx=5)

        topFrame(self)
        dataframe(self)

        dataoutput(self)

        try:
            fetchalldb(self, self.devtblframea, self.iam_selecteddevice)
        except:
            pass

        groupswitch_event(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
