import sqlite3
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import *
from PIL import ImageTk, Image
from netmiko import ConnectHandler
import time
import os
import shutil
from settings import *
from connecttodb import getdevicefromid
import regex as re
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException


def tftpbtngo(self, selectedid):

    self.btnbackup.configure(state="disabled", fg_color="gray", border_color="gray")

    self.progstatus.set(0.5)
    self.editgrpstatuslbl.configure(text=f"Starting process on id: {selectedid}")
    self.update_idletasks()

    self.cgouttxtbx.configure(state="normal")

    retid = 0
    retname = ""
    retip = ""
    retusername = ""
    retpassword = ""
    retdescription = ""
    rettype = ""
    retgolden = ""

    (
        retid,
        retname,
        retip,
        retusername,
        retpassword,
        retdescription,
        rettype,
        retgolden,
    ) = getdevicefromid(selectedid)

    hostname = ""
    filedatetime = str(time.strftime("%Y-%m-%d-%H-%M-%S"))
    hostname = retname

    device = {
        "device_type": f"{rettype}",
        "host": f"{retip}",
        "username": f"{retusername}",
        "password": f"{retpassword}",
        "secret": f"{retpassword}",
    }
    self.cgouttxtbx.insert(
        INSERT,
        f"1) connecting to device id:{selectedid}" + " " + f"{device['host']}" + "\n",
    )

    self.progstatus.set(0.6)
    self.editgrpstatuslbl.configure(text=f"Backup process running")
    self.update_idletasks()

    try:
        f"device{str(1)}"
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        hostname = net_connect.find_prompt()[:-1]

        copy_command = f"copy {self.setbackuptypevar.get()} tftp://{tftpserver}"
        output = net_connect.send_command_timing(copy_command)
        self.cgouttxtbx.insert(
            INSERT, f"2) connection hostname from device is :{hostname}" + "\n"
        )

        self.progstatus.set(0.7)
        self.editgrpstatuslbl.configure(text=f"Hostname found: {hostname}")
        self.update_idletasks()

        if "Address or name" in output:
            output += net_connect.send_command_timing("\n")
            self.cgouttxtbx.insert(
                INSERT, f"3) Accepting the tftp server ip address: {tftpserver}" + "\n"
            )
        if "Destination filename" in output:
            output += net_connect.send_command_timing(
                f"{hostname}_"
                + f"{filedatetime}_"
                + f"{self.setbackuptypevar.get()}"
                + f"_{self.setfileidtypevar.get()}"
                + "\n"
            )

            self.cgouttxtbx.insert(
                INSERT,
                f"4) The TFTP temporary save directory will be: {directorylocation}"
                + "\n",
            )
            self.cgouttxtbx.insert(
                INSERT,
                f"5) The filename will be:\n{hostname}_"
                + f"{filedatetime}_"
                + f"{self.setbackuptypevar.get()}"
                + f"_{self.setfileidtypevar.get()}"
                + "\n",
            )

            net_connect.disconnect

    except NetMikoAuthenticationException as AuthException:
        self.cgouttxtbx.insert(
            INSERT,
            f"***--- {hostname} ({retip}) ---*** \n Authentication Error \n {AuthException}",
        )
    except NetMikoTimeoutException as TimeoutException:
        self.cgouttxtbx.insert(
            INSERT,
            f"Timeout Exception Error ***--- {hostname} ({retip}) ---*** \n {TimeoutException}",
        )
    except SSHException as sshexception:
        self.cgouttxtbx.insert(
            INSERT,
            f"SSHException Error ***--- {hostname} ({retip}) ---*** \n {sshexception}",
        )
    except Exception as unknown_error:
        self.cgouttxtbx.insert(
            INSERT,
            f"Unknown Error ***--- {hostname} ({retip}) ---*** \n  \n {unknown_error}",
        )
    except:
        self.cgouttxtbx.insert(
            INSERT, f"6) A netmiko connection exception occurred: {device['host']}\n"
        )

    finally:
        try:
            self.cgouttxtbx.insert(
                INSERT,
                f"6) File was sucessfully transfered: {output[output.rindex('!')+1:]}\n",
            )
        except:
            self.cgouttxtbx.insert(INSERT, f"6) Could not print the output\n")

    os.chdir(changetoDEVICEDATAdirectory)

    if hostname == retname:
        try:
            for file_name in os.listdir(filesource):
                source = filesource + file_name
                destination = filedestination + "/" + hostname + "/" + file_name
                if os.path.isfile(source):
                    shutil.copy(source, destination)
        except OSError as error:
            pass

        finally:
            if len(os.listdir(filesource)) > 0:

                for f in os.listdir(filesource):
                    os.remove(os.path.join(filesource, f))
            else:
                pass

    else:
        pass

    self.progstatus.set(1)
    self.editgrpstatuslbl.configure(text=f"Process complete")
    self.cgouttxtbx.insert(INSERT, f"7) Backup process complete")
    self.cgouttxtbx.configure(state="disabled")


def tftpdevicebackup(self):

    devicesdetails = []
    self.tftpselectedid = StringVar()
    self.setbackuptypevar = StringVar()
    self.setfileidtypevar = StringVar()

    sqliteConnection = sqlite3.connect(dbfile)
    cursor = sqliteConnection.cursor()
    query = f"SELECT * FROM devices"
    cursor.execute(query)
    record = cursor.fetchall()
    for row in record:
        retid = row[0]
        retname = row[1]
        retip = row[2]
        row[3]
        row[4]
        row[5]
        row[6]
        row[7]
        devicesdetails.append(f"id:{retid}" + " " + f"{retname}" + " " + f"({retip})")
        self.tftpselectedid.set(str(retid))

    def activatebackupbtn(self):
        if (
            self.bktpeselecchkbx.get() != "Select"
            and self.fileidselec.get() != "Select"
        ):

            self.btnbackup.configure(
                state="normal",
                fg_color="green",
                hover_color="green4",
                border_width=2,
                border_color="dark green",
            )
        else:
            pass

    def setbackuptype(self):
        self.setbackuptypevar.set(self.bktpeselecchkbx.get())
        if self.bktpeselecchkbx.get() == "Select":
            tk.messagebox.showinfo(
                title="Backup type selection error",
                message="Please select a valid backup type option.",
                icon="error",
                parent=self.tftpbackupwindow,
            )
        else:
            self.devnotetxtbx.insert(
                INSERT,
                f"----------------------------------\nBackup type: {self.setbackuptypevar.get()}\n",
            )

            self.bktpeselectlbl.configure(state="disabled")
            self.bktpeselecchkbx.configure(
                border_color="gray",
                button_color="gray",
                fg_color="gray75",
                state="disabled",
            )

            self.bktpeselecbtn.configure(
                text="Accepted", fg_color="gray", state="disabled"
            )

            self.fileidlbl.configure(state="normal")
            self.fileidselec.configure(
                fg_color="pale green",
                state="readonly",
                border_color="dark slate gray",
                button_color="dark slate gray",
                button_hover_color="green4",
                dropdown_fg_color="pale green",
                dropdown_hover_color="PaleGreen3",
            )
            self.fileidselec.set(value="Select")
            self.fileidbtn.configure(
                state="normal", fg_color="green", hover_color="green4"
            )

            self.progstatus.set(0.2)

            self.editgrpstatuslbl.configure(
                text=f"{self.setbackuptypevar.get()} accepted"
            )

    def setfileidtype(self):

        self.setfileidtypevar.set(self.fileidselec.get())

        if self.fileidselec.get() == "Select":
            tk.messagebox.showinfo(
                title="backup type",
                message="Please select a valid File identifier option.",
                icon="error",
                parent=self.tftpbackupwindow,
            )
        else:
            self.devnotetxtbx.insert(
                INSERT,
                f"----------------------------------\nFile identifier: {self.fileidselec.get()}\n",
            )

            self.fileidlbl.configure(state="disabled")
            self.fileidselec.configure(
                border_color="gray",
                button_color="gray",
                fg_color="gray75",
                state="disabled",
            )
            self.fileidbtn.configure(text="Accepted", fg_color="gray", state="disabled")

            activatebackupbtn(self)

            self.progstatus.set(0.3)
            self.editgrpstatuslbl.configure(
                text=f"File identified as: {self.setfileidtypevar.get()}"
            )

    def setdevice(self):
        if self.devnamecbx.get() == "select a device":
            tk.messagebox.showinfo(
                title="Device selection error",
                message="Please select a valid Device option.",
                icon="error",
                parent=self.tftpbackupwindow,
            )
        else:
            cbxid = re.findall(r"^\D*(\d+)", self.devnamecbx.get())
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

            self.tftpselectedid.set(str(retid1))

            self.devname.configure(state="disabled")
            self.devnamebtn.configure(
                text="Accepted", fg_color="gray", state="disabled"
            )
            self.devnamecbx.configure(
                border_color="gray",
                button_color="gray",
                fg_color="gray75",
                state="disabled",
            )

            self.bktpeselectlbl.configure(state="normal")
            self.bktpeselecchkbx.configure(
                fg_color="pale green",
                state="readonly",
                border_color="dark slate gray",
                button_color="dark slate gray",
                button_hover_color="green4",
                dropdown_fg_color="pale green",
                dropdown_hover_color="PaleGreen3",
            )
            self.bktpeselecchkbx.set(value="Select")
            self.bktpeselecbtn.configure(
                state="normal", fg_color="green", hover_color="green4"
            )

            self.devnotelbl.configure(state="normal")
            self.devnotetxtbx.configure(state="normal", bg="light yellow", wrap=WORD)
            self.devnotetxtbx.insert(
                INSERT,
                f"Device id: {retid1}\n"
                + f"Device Name: {retname1}\n"
                + f"Device IP address: {retip1}\n",
            )

            self.progstatus.set(0.1)
            self.editgrpstatuslbl.configure(text=f"{retname1} accepted")

    self.tftpbackupwindow = tk.Toplevel(master=self)
    self.tftpbackupwindow.title("Register")
    self.tftpbackupwindow.geometry("600x820+200+200")
    self.tftpbackupwindow.configure(background="powder blue")
    self.tftpbackupwindow.wm_iconphoto(
        False, (ImageTk.PhotoImage(Image.open(pythonicon)))
    )

    self.tftpbackupwindow.attributes("-topmost", "true")
    self.tftpbackupwindow.transient(self)
    self.tftpbackupwindow.update_idletasks()
    self.tftpbackupwindow.grab_set()

    self.tftpbackupwindow.grid_columnconfigure(0, weight=1)

    self.createlabel = ctk.CTkLabel(
        self.tftpbackupwindow,
        text="Backup a device configuration (TFTP)",
        font=("arial", 22, "bold"),
    )
    self.createlabel.grid(row=0, column=0, sticky=EW, columnspan=3, pady=(20, 16))
    self.separator1 = ttk.Separator(self.tftpbackupwindow, orient="horizontal")
    self.separator1.grid(row=1, sticky=EW, columnspan=3, padx=20, pady=10)

    self.devname = Label(
        self.tftpbackupwindow,
        text="Device selection",
        font=("arial", 14, "bold"),
        bg="powder blue",
        fg="black",
    )
    self.devname.grid(row=2, column=0, sticky=W, padx=(25, 10), pady=10)
    self.devnamecbx = ctk.CTkComboBox(
        self.tftpbackupwindow,
        width=220,
        font=("arial", 14, "bold"),
        fg_color="pale green",
        values=devicesdetails,
        border_color="dark slate gray",
        button_color="dark slate gray",
        button_hover_color="green4",
        dropdown_fg_color="pale green",
        dropdown_hover_color="PaleGreen3",
        dropdown_font=("arial", 16, "bold"),
    )
    self.devnamecbx.grid(row=2, column=1, sticky=EW, padx=(15, 10), pady=10)
    self.devnamecbx.set("select a device")
    self.devnamebtn = ctk.CTkButton(
        self.tftpbackupwindow,
        text="Set",
        width=100,
        fg_color="green",
        hover_color="green4",
        command=lambda: setdevice(self),
    )
    self.devnamebtn.grid(row=2, column=2, padx=(15, 25), pady=10)

    self.bktpeselectlbl = Label(
        self.tftpbackupwindow,
        text="Backup type",
        font=("arial", 14, "bold"),
        bg="powder blue",
        fg="black",
        state=DISABLED,
    )
    self.bktpeselectlbl.grid(row=3, column=0, sticky=W, padx=(25, 10), pady=10)
    self.bktpeselecchkbxvalues = ["running-config", "startup-config"]
    self.bktpeselecchkbx = ctk.CTkComboBox(
        self.tftpbackupwindow,
        font=("arial", 14, "bold"),
        state="disabled",
        values=self.bktpeselecchkbxvalues,
        dropdown_font=("arial", 16, "bold"),
    )
    self.bktpeselecchkbx.grid(row=3, column=1, sticky=EW, padx=(15, 10), pady=10)
    self.bktpeselecbtn = ctk.CTkButton(
        self.tftpbackupwindow,
        text="Set",
        state=DISABLED,
        width=100,
        fg_color="gray",
        hover_color="green4",
        command=lambda: setbackuptype(self),
    )
    self.bktpeselecbtn.grid(row=3, column=2, padx=(15, 25), pady=10)

    self.fileidlbl = Label(
        self.tftpbackupwindow,
        text="File identifier",
        font=("arial", 14, "bold"),
        bg="powder blue",
        fg="black",
        state=DISABLED,
    )
    self.fileidlbl.grid(row=4, column=0, sticky=W, padx=(25, 10), pady=10)
    self.fileidoptions = ["Daily", "Weekly", "Monthly", "Golden", "Silver"]
    self.fileidselec = ctk.CTkComboBox(
        self.tftpbackupwindow,
        state="disabled",
        font=("arial", 14, "bold"),
        values=self.fileidoptions,
        dropdown_font=("arial", 16, "bold"),
    )
    self.fileidselec.grid(row=4, column=1, sticky=EW, padx=(15, 10), pady=10)
    self.fileidbtn = ctk.CTkButton(
        self.tftpbackupwindow,
        text="Set",
        state=DISABLED,
        width=100,
        fg_color="gray",
        hover_color="green4",
        font=("arial", 12, "bold"),
        command=lambda: setfileidtype(self),
    )
    self.fileidbtn.grid(row=4, column=2, padx=(15, 25), pady=10)

    self.devnotelbl = Label(
        self.tftpbackupwindow,
        text="Notes",
        font="arial 14 bold",
        bg="powder blue",
        fg="black",
        state=DISABLED,
    )
    self.devnotelbl.grid(row=5, column=0, sticky=NW, padx=25, pady=10)

    self.devnotetxtbx = scrolledtext.ScrolledText(
        self.tftpbackupwindow,
        font="arial 12",
        height=10,
        width=25,
        bg="gray70",
        wrap=WORD,
        state=DISABLED,
    )
    self.devnotetxtbx.grid(
        row=6, column=0, sticky=EW, padx=(25, 10), pady=(20), columnspan=2
    )

    self.progstatus = ctk.CTkProgressBar(
        self.tftpbackupwindow,
        progress_color="green4",
        border_width=1,
        border_color="dark slate gray",
    )
    self.progstatus.grid(row=7, column=0, sticky=EW, padx=30, pady=10, columnspan=3)
    self.progstatus.set(0)

    self.btnbackup = ctk.CTkButton(
        self.tftpbackupwindow,
        text="Backup",
        state="disabled",
        width=120,
        fg_color="gray",
        hover_color="green4",
        font=("arial", 12, "bold"),
        command=lambda: tftpbtngo(self, self.tftpselectedid.get()),
    )
    self.btnbackup.grid(column=0, row=8, pady=10, padx=(25, 0), sticky=W)

    self.editgrpstatuslbl = Label(
        self.tftpbackupwindow,
        text="Select a device",
        font=("arial", 14, "bold"),
        bg="powder blue",
        fg="OrangeRed2",
    )
    self.editgrpstatuslbl.grid(row=8, column=1, padx=(0, 55), pady=10, sticky=EW)

    self.btnexit = ctk.CTkButton(
        self.tftpbackupwindow,
        text="EXIT",
        width=120,
        fg_color="red2",
        font=("arial", 12, "bold"),
        command=self.tftpbackupwindow.destroy,
        hover_color="red4",
        border_width=2,
        border_color="red4",
    )
    self.btnexit.grid(column=2, row=8, pady=10, padx=(0, 25), sticky=E)
    self.cgouttxtbx = scrolledtext.ScrolledText(
        self.tftpbackupwindow,
        font="arial 10",
        height=11,
        width=25,
        bg="light goldenrod yellow",
        wrap=WORD,
        state=DISABLED,
    )
    self.cgouttxtbx.grid(
        row=9, column=0, sticky=EW, padx=(25, 25), pady=10, columnspan=3
    )
