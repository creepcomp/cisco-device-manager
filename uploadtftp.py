import sqlite3
import os
from settings import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import ttk, scrolledtext
import shutil
from netmiko import (
    ConnectHandler,
    NetMikoTimeoutException,
    NetMikoAuthenticationException,
)
from connecttodb import getdevicefromid
from PIL import ImageTk, Image
import regex as re
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException


def configuploadtftp(self):
    devicesdetails = []
    self.tftpselectedid = StringVar()
    self.setbackuptypevar = StringVar()
    self.setfileidtypevar = StringVar()
    self.filename = StringVar()
    self.filedest = StringVar()
    self.filesrc = StringVar()
    self.tftprootdir = StringVar()
    self.tftprootdir.set(tftprootdir)

    self.checkboxcopy_var = ctk.StringVar(value="on")
    self.checkboxrepl_var = ctk.StringVar(value="off")
    self.checkboxcrs_var = ctk.StringVar(value="off")
    self.chkbxrunningcfg_var = ctk.StringVar(value="on")
    self.chkbxstartupcfg_var = ctk.StringVar(value="off")
    self.checkboxcstrn_var = ctk.StringVar(value="off")

    self.tftpuploadcmd = ctk.StringVar()

    self.running_startup_var = StringVar()

    self.returnedid = IntVar(self)
    self.returnedname = StringVar()
    self.returnedip = StringVar()
    self.returnedusername = StringVar()
    self.returnedpassword = StringVar()
    self.returneddescription = StringVar()
    self.returnedtype = StringVar()
    self.returnedgolden = StringVar()

    sqliteConnection = sqlite3.connect(dbfile)
    cursor = sqliteConnection.cursor()

    query = f"SELECT * FROM devices"
    cursor.execute(query)
    record = cursor.fetchall()
    for row in record:
        self.returnedid.set(row[0])
        self.returnedname.set(row[1])
        self.returnedip.set(row[2])
        self.returnedusername.set(row[3])
        self.returnedpassword.set(row[4])
        self.returneddescription.set(row[5])
        self.returnedtype.set(row[6])
        self.returnedgolden.set(row[7])

        devicesdetails.append(
            f"id:{str(self.returnedid.get())}"
            + " "
            + f"{self.returnedname.get()}"
            + " "
            + f"({self.returnedip.get()})"
        )

        self.tftpselectedid.set(str(self.returnedid.get()))

    def tftptorouter(self):
        self.progstatus.set(0.3)
        self.btnupload.configure(state="disabled", fg_color="gray", border_color="gray")
        self.checkboxcopy.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )
        self.checkboxrepl.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )
        self.checkboxcrs.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )
        self.chkbxrunningcfg.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )
        self.chkbxstartupcfg.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )
        self.checkboxcstrn.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )
        self.update_idletasks()

        os.chdir(self.tftprootdir.get())

        self.grpdesetry.insert(
            INSERT,
            f"2) Looking for file in the TFTP staging area:\n{self.filename.get()}\n",
        )

        if self.chkbxstartupcfg_var.get() == "on":
            self.running_startup_var.set("startup-config")

        elif self.chkbxrunningcfg_var.get() == "on":
            self.running_startup_var.set("running-config")

        else:
            pass

        if os.path.isfile(self.filename.get()):

            self.statuslbl.configure(
                font=("arial", 12, "bold"), text="Starting to run task"
            )
            self.update_idletasks()

            cisco_device = {
                "device_type": f"{self.returnedtype.get()}",
                "host": f"{self.returnedip.get()}",
                "username": f"{self.returnedusername.get()}",
                "password": f"{self.returnedpassword.get()}",
                "port": 22,
                "secret": f"{self.returnedpassword.get()}",
                "verbose": True,
            }

            self.grpdesetry.insert(
                INSERT, f"3) Initiating Connection to : {self.returnedname.get()}\n"
            )

            conn = ConnectHandler(**cisco_device)
            conn_prompt = conn.find_prompt()
            if ">" in conn_prompt:
                conn.enable()
            output = conn.send_command(f"\n")

            self.grpdesetry.insert(
                INSERT,
                f"4) The config mode on the device is: {conn.check_config_mode()}\n",
            )

            self.progstatus.set(0.4)
            self.update_idletasks()

            try:
                f"device{str(1)}"
                net_connect = ConnectHandler(**cisco_device)

                net_connect.enable()
                hostname = net_connect.find_prompt()[:-1]

                self.grpdesetry.insert(
                    INSERT, f"5) The hostname on the device is: {hostname}\n"
                )

                self.statuslbl.configure(
                    font=("arial", 12, "bold"), text="Task in progress"
                )
                self.progstatus.set(0.5)
                self.update_idletasks()

                if self.checkboxcopy_var.get() == "on":

                    self.tftpuploadcmd.set(
                        f"copy tftp://{tftpserver}{tftprootdir}/{self.filename.get()} {self.running_startup_var.get()}"
                    )
                    self.grpdesetry.insert(
                        INSERT, f"6) Sending the command: {self.tftpuploadcmd.get()}\n"
                    )

                    output = net_connect.send_command_timing(self.tftpuploadcmd.get())
                    if "Address or name" in output:
                        output += net_connect.send_command_timing(f"{tftpserver}\n")

                    if "Source filename" in output:
                        output += net_connect.send_command_timing(
                            f"{self.filename.get()}\n"
                        )

                        net_connect.disconnect
                    if "Destination filename" in output:
                        output += net_connect.send_command_timing(f"\n")

                        self.grpdesetry.insert(
                            INSERT, f"7) Running the command on the device.\n"
                        )

                    self.progstatus.set(0.7)
                    self.update_idletasks()

                    if (
                        self.chkbxrunningcfg_var.get() == "on"
                        and self.checkboxcrs_var.get() == "on"
                    ):

                        copy_command1 = "copy running-config startup-config"
                        output1 = net_connect.send_command_timing(copy_command1)
                        self.grpdesetry.insert(INSERT, f"Output1:\n{output1}\n")

                        if "Destination filename" in output1:
                            output1 += net_connect.send_command_timing("\n")
                            self.grpdesetry.insert(
                                INSERT,
                                f"running-config > startup-config output:\n{output1}\n",
                            )
                            self.grpdesetry.insert(
                                INSERT,
                                "------------------------------------------------\n",
                            )
                            self.grpdesetry.insert(
                                INSERT,
                                f"Request completed: running-config has been copied to the startup-config\n",
                            )
                            self.grpdesetry.insert(
                                INSERT,
                                "------------------------------------------------\n",
                            )
                        else:
                            pass

                        self.progstatus.set(0.8)
                        self.update_idletasks()

                    if (
                        self.chkbxstartupcfg_var.get() == "on"
                        and self.checkboxcstrn_var.get() == "on"
                    ):

                        copy_command1 = "copy startup-config running-config "
                        output1 = net_connect.send_command_timing(copy_command1)
                        self.grpdesetry.insert(INSERT, f"Output1:\n{output1}\n")

                        if "Destination filename" in output1:
                            output1 += net_connect.send_command_timing("\n")
                            self.grpdesetry.insert(
                                INSERT,
                                f"copy startup-config running-config: COMPLETED\n{output1}\n",
                            )
                        else:
                            pass

                        self.progstatus.set(0.8)
                        self.update_idletasks()

                    if (
                        self.chkbxstartupcfg_var.get() == "on"
                        and self.checkboxcstrn_var.get() == "on"
                    ):

                        copy_command1 = "copy startup-config running-config"
                        output1 = net_connect.send_command_timing(copy_command1)
                        self.grpdesetry.insert(INSERT, f"Output1:\n{output1}\n")

                        if "Destination filename" in output1:
                            output1 += net_connect.send_command_timing("\n")
                            self.grpdesetry.insert(
                                INSERT,
                                f"startup-config > running-config output:\n{output1}\n",
                            )
                            self.grpdesetry.insert(
                                INSERT,
                                "------------------------------------------------\n",
                            )
                            self.grpdesetry.insert(
                                INSERT,
                                f"Request completed: startup-config has been copied to the running-config.\n",
                            )
                            self.grpdesetry.insert(
                                INSERT,
                                "------------------------------------------------\n",
                            )

                        else:
                            pass

                        self.progstatus.set(0.8)
                        self.update_idletasks()

                elif self.checkboxrepl_var.get() == "on":

                    self.tftpuploadcmd.set(
                        f"configure replace tftp://{tftpserver}{tftprootdir}/{self.filename.get()} force"
                    )
                    self.grpdesetry.insert(
                        INSERT, f"6) Sending the command: {self.tftpuploadcmd.get()}\n"
                    )

                    output = net_connect.send_command_timing(self.tftpuploadcmd.get())
                    self.grpdesetry.insert(INSERT, f"7) Output:\n{output}\n")

                    if self.checkboxcrs_var.get() == "on":

                        copy_command1 = "copy running-config startup-config"
                        output1 = net_connect.send_command_timing(copy_command1)
                        self.grpdesetry.insert(INSERT, f"8) Output1:\n{output1}\n")

                        if "Destination filename" in output1:
                            output1 += net_connect.send_command_timing("\n")
                            self.grpdesetry.insert(
                                INSERT,
                                f"8a) Capturing running-config > startup-config output:\n{output1}\n",
                            )
                            self.grpdesetry.insert(INSERT, "------------------------\n")
                            self.grpdesetry.insert(
                                INSERT,
                                f"Request completed: running-config has been copied to the startup-config\n",
                            )
                            self.grpdesetry.insert(INSERT, "------------------------")
                        else:
                            pass

                    else:
                        pass

                    self.progstatus.set(0.8)
                    self.update_idletasks()

            except NetMikoAuthenticationException as AuthException:

                self.grpdesetry.insert(
                    INSERT,
                    f"***--- {self.returnedname.get()} ({self.returnedip.get()}) ---*** \n Authentication Error \n {AuthException}",
                )
            except NetMikoTimeoutException as TimeoutException:

                self.grpdesetry.insert(
                    INSERT,
                    f"Timeout Exception Error ***--- {self.returnedname.get()} ({self.returnedip.get()}) ---*** \n {TimeoutException}",
                )
            except SSHException as sshexception:

                self.grpdesetry.insert(
                    INSERT,
                    f"SSHException Error ***--- {self.returnedname.get()} ({self.returnedip.get()}) ---*** \n {sshexception}",
                )
            except Exception as unknown_error:

                self.grpdesetry.insert(
                    INSERT,
                    f"Unknown Error ***--- {self.returnedname.get()} ({self.returnedip.get()}) ---*** \n  \n {unknown_error}",
                )
            except:

                self.grpdesetry.insert(
                    INSERT,
                    f"5) An undefined error occured in the try block on: {self.returnedname.get()},{self.returnedip.get()}\n",
                )

            finally:

                net_connect.disconnect
                self.grpdesetry.insert(
                    INSERT, "------------------------------------------------\n"
                )
                self.grpdesetry.insert(
                    INSERT,
                    f"Request completed: {self.returnedname.get()} has a new {self.running_startup_var.get()}\n",
                )
                self.grpdesetry.insert(
                    INSERT, "------------------------------------------------"
                )

                if os.path.exists(f"{tftprootdir}/{self.filename.get()}"):
                    os.remove(f"{tftprootdir}/{self.filename.get()}")

                else:
                    pass

                self.statuslbl.configure(text="Task Completed")
                self.grpdesetry.see("end")
                self.progstatus.set(1)
                self.update_idletasks()

        else:

            self.grpdesetry.insert(INSERT, f"File or Location ERROR")
            self.grpdesetry.insert(
                INSERT, f"1) Expected file:\n {self.filename.get()}\n"
            )
            self.grpdesetry.insert(
                INSERT, f"2) Expected location:\n {self.tftprootdir.get()}\n"
            )

    def capturefile(self):

        if self.lbxcontenttop.curselection() == ():

            tk.messagebox.showinfo(
                title="Selection error",
                message="Please select a valid file option.",
                icon="error",
                parent=self.tftpuploadwindow,
            )
        else:

            try:

                self.filename.set(
                    self.lbxcontenttop.get(self.lbxcontenttop.curselection())
                )

                self.filedest.set(f"{tftprootdir}/{self.filename.get()}")

                self.filesrc.set(
                    f"{devicesaveddata}/{self.returnedname.get()}/{self.filename.get()}"
                )

                try:

                    self.selectdevicecbx.configure(
                        fg_color="gray64",
                        border_color="gray40",
                        button_color="gray40",
                        button_hover_color="gray40",
                        state="disabled",
                        text_color_disabled="white",
                    )
                    self.lbxcontenttop.configure(
                        selectbackground="gray40", background="gray64"
                    )
                    self.lbxcontenttop.bindtags((self, "all"))
                    self.btnselect.configure(
                        text="Accepted",
                        state="disabled",
                        fg_color="gray",
                        text_color_disabled="white",
                    )
                    self.grpdesetry.config(state=NORMAL)
                    self.grpdesetry.config(background="light yellow")
                    self.btnupload.configure(
                        state="normal", fg_color="green", border_color="dark green"
                    )

                    shutil.copy(self.filesrc.get(), self.filedest.get())
                    self.grpdesetry.insert(
                        INSERT,
                        f"1) The file has been copied to the TFTP staging area: \n {self.filename.get()} \n",
                    )

                    self.progstatus.set(0.2)

                    self.statuslbl.configure(text=f"Ready for uploading")

                except:

                    self.grpdesetry.insert(
                        INSERT,
                        f"Problem copying file to staging area: \n {self.filename.get()} \n",
                    )
                    self.grpdesetry.insert(
                        INSERT, f"File source: \n {self.filesrc.get()} \n"
                    )
                    self.grpdesetry.insert(
                        INSERT, f"File Destination: \n {self.filedest.get()} \n"
                    )

            except:
                pass

    def selectdevicecbxcallback(self):

        self.lbxcontenttop.delete(0, "end")

        self.btnselect.configure(fg_color="green", state="normal")
        self.lbxcontenttop.configure(state="normal", background="pale green")

        cbxid = re.findall(r"^\D*(\d+)", self.selectdevicecbx.get())
        cbxidstr = str(cbxid[0])

        retid1 = 0
        retname1 = ""
        retip1 = ""
        retusername1 = ""
        retpassword1 = ""
        retdescription1 = ""
        rettype1 = ""
        retgolden1 = ""

        (
            retid1,
            retname1,
            retip1,
            retusername1,
            retpassword1,
            retdescription1,
            rettype1,
            retgolden1,
        ) = getdevicefromid(cbxidstr)

        self.returnedid.set(retid1)
        self.returnedname.set(retname1)
        self.returnedip.set(retip1)
        self.returnedusername.set(retusername1)
        self.returnedpassword.set(retpassword1)
        self.returneddescription.set(retdescription1)
        self.returnedtype.set(rettype1)
        self.returnedgolden.set(retgolden1)

        try:

            devicedir = os.path.join(devicesaveddata, retname1)
            os.chdir(devicedir)

            filesindir = [f for f in os.listdir(".") if os.path.isfile(f)]
            for f in filesindir:

                self.lbxcontenttop.insert("end", f)
        except:

            self.lbxcontenttop.insert("end", "A problem exists")
            self.lbxcontenttop.insert("end", "The device directory could not be found")
            self.lbxcontenttop.insert("end", f"{devicedir}")

        self.progstatus.set(0.1)
        self.statuslbl.configure(text=f"{self.returnedname.get()} selected")

    def checkboxcopy_event(self):
        if self.checkboxcopy.get() == "on":

            self.checkboxrepl.deselect()

            self.chkbxrunningcfg.configure(
                border_color="dark slate gray", state="normal"
            )

            self.chkbxstartupcfg.configure(
                border_color="dark slate gray", state="normal"
            )

            self.checkboxcstrn.configure(border_color="dark slate gray", state="normal")
            self.checkboxcrs.deselect()
            self.checkboxcrs.configure(border_color="dark slate gray", state="normal")
            self.checkboxcstrn.deselect()
            self.checkboxcstrn.configure(border_color="gray", state="disabled")

            self.chkbxrunningcfg.select()

        else:

            self.checkboxrepl.select()

            self.chkbxrunningcfg.deselect()
            self.chkbxrunningcfg.configure(border_color="gray", state="disabled")

            self.chkbxstartupcfg.deselect()
            self.chkbxstartupcfg.configure(border_color="gray", state="disabled")

            self.checkboxcstrn.deselect()
            self.checkboxcstrn.configure(border_color="gray", state="disabled")
            self.checkboxcrs.deselect()
            self.checkboxcrs.configure(border_color="dark slate gray", state="normal")

    def checkboxrepl_event(self):
        self.checkboxcopy.deselect()

        if self.checkboxrepl.get() == "on":

            self.checkboxcrs.deselect()
            self.checkboxcrs.configure(border_color="dark slate gray", state="normal")
            self.checkboxcstrn.deselect()
            self.checkboxcstrn.configure(border_color="gray", state="disabled")

            self.chkbxrunningcfg.deselect()
            self.chkbxrunningcfg.configure(border_color="gray", state="disabled")

            self.chkbxstartupcfg.deselect()
            self.chkbxstartupcfg.configure(border_color="gray", state="disabled")

            self.running_startup_var.set("running-config")

        else:

            self.checkboxcopy.select()

            self.chkbxrunningcfg.configure(
                border_color="dark slate gray", state="normal"
            )
            self.chkbxrunningcfg.select()

            self.chkbxstartupcfg.deselect()
            self.chkbxstartupcfg.configure(
                border_color="dark slate gray", state="normal"
            )

            self.checkboxcrs.deselect()

    def chkbxrunningcfg_event(self):

        if self.chkbxrunningcfg_var.get() == "on":

            self.chkbxstartupcfg.deselect()
            self.checkboxcrs.configure(border_color="dark slate gray", state="normal")
            self.checkboxcstrn.deselect()
            self.checkboxcstrn.configure(border_color="gray", state="disabled")

        else:

            self.chkbxstartupcfg.select()

            self.checkboxcrs.deselect()
            self.checkboxcrs.configure(border_color="gray", state="disabled")

            self.checkboxcstrn.deselect()
            self.checkboxcstrn.configure(border_color="dark slate gray", state="normal")

    def chkbxstartupcfg_event(self):
        self.checkboxcstrn.deselect()

        if self.chkbxrunningcfg_var.get() == "on":

            self.chkbxrunningcfg.deselect()
            self.checkboxcrs.deselect()
            self.checkboxcstrn.configure(border_color="dark slate gray", state="normal")
            self.checkboxcrs.configure(border_color="gray", state="disabled")

        else:

            self.chkbxrunningcfg.select()

            self.checkboxcrs.deselect()
            self.checkboxcrs.configure(border_color="dark slate gray", state="normal")
            self.checkboxcstrn.configure(border_color="gray", state="disabled")

    def checkboxcrs_event(self):
        pass

    def checkboxcstrn_event(self):
        pass

    self.tftpuploadwindow = tk.Toplevel()
    self.tftpuploadwindow.geometry("600x790+200+200")
    self.tftpuploadwindow.title("TFTP Upload to device")
    self.tftpuploadwindow.configure(background="powder blue")
    self.tftpuploadwindow.resizable(False, False)
    self.tftpuploadwindow.wm_iconphoto(
        False, (ImageTk.PhotoImage(Image.open(pythonicon)))
    )

    self.tftpuploadwindow.attributes("-topmost", "true")
    self.tftpuploadwindow.transient(self)
    self.tftpuploadwindow.update_idletasks()
    self.tftpuploadwindow.grab_set()

    self.tftpuploadwindow.grid_columnconfigure(0, weight=1)

    self.lbltopa = ctk.CTkLabel(
        self.tftpuploadwindow,
        text="TFTP Upload config to device",
        font=("arial", 22, "bold"),
    )
    self.lbltopa.grid(row=0, column=0, sticky=EW, columnspan=3, pady=(15, 10))

    self.separator1 = ttk.Separator(self.tftpuploadwindow, orient="horizontal")
    self.separator1.grid(row=1, sticky=EW, columnspan=3, padx=20, pady=8)

    self.devname = Label(
        self.tftpuploadwindow,
        text="Device selection",
        font=("arial", 14, "bold"),
        bg="powder blue",
        fg="black",
    )
    self.devname.grid(row=2, column=0, sticky=W, padx=(25, 5), pady=(10))
    self.selectdevicecbx = ctk.CTkComboBox(
        self.tftpuploadwindow,
        width=350,
        font=("arial", 14, "bold"),
        fg_color="pale green",
        border_color="dark slate gray",
        button_color="dark slate gray",
        button_hover_color="green4",
        dropdown_fg_color="pale green",
        dropdown_hover_color="PaleGreen3",
        values=devicesdetails,
        command=lambda v: selectdevicecbxcallback(self),
    )
    self.selectdevicecbx.set(value="select a device")
    self.selectdevicecbx.grid(
        row=2, column=1, sticky=E, padx=(10, 30), pady=10, columnspan=2
    )

    self.lbxcontenttop = Listbox(
        self.tftpuploadwindow,
        height=12,
        width=180,
        selectbackground="green4",
        background="gray70",
        activestyle=NONE,
        selectmode=SINGLE,
        state="disabled",
    )
    self.lbxcontenttop.grid(
        row=3, column=0, padx=(25, 0), pady=(10), sticky=EW, columnspan=2
    )

    self.btnselect = ctk.CTkButton(
        self.tftpuploadwindow,
        text="Select",
        command=lambda: capturefile(self),
        width=80,
        fg_color="gray",
        hover_color="green4",
        state="disabled",
    )
    self.btnselect.grid(row=3, column=2, padx=(0, 30), pady=10, sticky=SE)
    self.horizspr1 = ttk.Separator(self.tftpuploadwindow, orient="horizontal")
    self.horizspr1.grid(row=5, column=0, sticky=EW, columnspan=3, padx=20, pady=10)
    self.grpdesetry = scrolledtext.ScrolledText(
        self.tftpuploadwindow,
        font="arial 12",
        height=10,
        width=10,
        bg="gray70",
        wrap=WORD,
        state=DISABLED,
    )
    self.grpdesetry.grid(
        row=6, column=0, sticky=EW, padx=(25, 30), pady=10, columnspan=3
    )

    self.checkboxcopy = ctk.CTkCheckBox(
        self.tftpuploadwindow,
        text="Copy(merge) config",
        command=lambda: checkboxcopy_event(self),
        variable=self.checkboxcopy_var,
        onvalue="on",
        offvalue="off",
        fg_color="green4",
        hover_color="dark slate gray",
        border_color="dark slate gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.checkboxcopy.grid(row=7, column=0, pady=10, sticky=W, padx=(25, 0))
    self.checkboxrepl = ctk.CTkCheckBox(
        self.tftpuploadwindow,
        text="Replace running config",
        command=lambda: checkboxrepl_event(self),
        variable=self.checkboxrepl_var,
        onvalue="on",
        offvalue="off",
        fg_color="green4",
        hover_color="dark slate gray",
        border_color="dark slate gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.checkboxrepl.grid(row=7, column=1, pady=10, sticky=W)
    self.checkboxcrs = ctk.CTkCheckBox(
        self.tftpuploadwindow,
        text="copy runnning > startup",
        command=lambda: checkboxcrs_event(self),
        variable=self.checkboxcrs_var,
        onvalue="on",
        offvalue="off",
        fg_color="green4",
        hover_color="dark slate gray",
        border_color="dark slate gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.checkboxcrs.grid(row=7, column=2, pady=10, padx=(0, 35))
    self.chkbxrunningcfg = ctk.CTkCheckBox(
        self.tftpuploadwindow,
        text="running-config",
        command=lambda: chkbxrunningcfg_event(self),
        variable=self.chkbxrunningcfg_var,
        onvalue="on",
        offvalue="off",
        fg_color="green4",
        hover_color="dark slate gray",
        border_color="dark slate gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.chkbxrunningcfg.grid(row=8, column=0, pady=10, sticky=W, padx=(25, 0))
    self.chkbxstartupcfg = ctk.CTkCheckBox(
        self.tftpuploadwindow,
        text="startup-config",
        command=lambda: chkbxstartupcfg_event(self),
        variable=self.chkbxstartupcfg_var,
        onvalue="on",
        offvalue="off",
        fg_color="green4",
        hover_color="dark slate gray",
        border_color="dark slate gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.chkbxstartupcfg.grid(row=8, column=1, pady=10, sticky=W)
    self.checkboxcstrn = ctk.CTkCheckBox(
        self.tftpuploadwindow,
        text="copy startup > runnning",
        command=lambda: checkboxcstrn_event(self),
        variable=self.checkboxcstrn_var,
        state="disabled",
        onvalue="on",
        offvalue="off",
        fg_color="green4",
        hover_color="dark slate gray",
        border_color="gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.checkboxcstrn.grid(row=8, column=2, pady=10, padx=(0, 35))
    self.virtspr1 = ttk.Separator(self.tftpuploadwindow, orient="vertical")
    self.virtspr1.grid(
        row=7, column=1, sticky="nsw", rowspan=2, pady=(10, 5), padx=(180, 1)
    )

    self.horizspr2 = ttk.Separator(self.tftpuploadwindow, orient="horizontal")
    self.horizspr2.grid(row=9, column=0, sticky=EW, columnspan=3, padx=(20), pady=(10))

    self.btnupload = ctk.CTkButton(
        self.tftpuploadwindow,
        text="Upload",
        command=lambda: tftptorouter(self),
        state="disabled",
        width=240,
        fg_color="gray",
        font=("arial", 12, "bold"),
        hover_color="green4",
        border_width=2,
        border_color="gray",
    )
    self.btnupload.grid(row=11, column=0, padx=30, pady=10, sticky=W)
    self.btnclose = ctk.CTkButton(
        self.tftpuploadwindow,
        text="Exit",
        width=140,
        fg_color="red3",
        font=("arial", 12, "bold"),
        hover_color="red4",
        border_width=2,
        border_color="red4",
        command=self.tftpuploadwindow.destroy,
    )
    self.btnclose.grid(row=11, column=2, pady=10, sticky=E, padx=(10, 30))
    self.statuslbl = tk.Label(
        self.tftpuploadwindow,
        text="Select a device",
        font=("arial", 12, "bold"),
        bg="powder blue",
        fg="OrangeRed2",
    )
    self.statuslbl.grid(row=11, column=1)

    self.progstatus = ctk.CTkProgressBar(
        self.tftpuploadwindow,
        progress_color="green4",
        border_width=1,
        border_color="dark slate gray",
    )
    self.progstatus.grid(row=12, column=0, sticky=EW, padx=30, pady=5, columnspan=3)
    self.progstatus.set(0)
