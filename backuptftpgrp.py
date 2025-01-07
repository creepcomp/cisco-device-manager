from netmiko import ConnectHandler


from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException
import time
import os
import shutil
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import customtkinter as ctk
import os
from settings import *
import json
from connecttodb import getdevicefromid
from PIL import ImageTk, Image


def grpselectiongettftp(self, groupselection):

    os.chdir(devicegroups)
    groupdevicepath = os.path.join(devicegroups, groupselection)
    os.chdir(groupdevicepath)

    filepath = os.path.join(groupselection + ".json")

    filetoread = open(filepath)
    inputjsondata = json.load(filetoread)

    return inputjsondata["members"]


def backupgrouptftp(self):

    self.tftpgrpcombxstrgrp = []
    self.tftpgrpcombxstrgrp_var = ctk.StringVar(self)

    self.membersofselecgrp = []

    self.selectedgrpbucket_var = []
    self.selectedgrpbucket_var_ids = []

    self.startuporrunning_var = ctk.StringVar(self)

    self.grpnameswitch_var = ctk.StringVar(self)

    self.fileidswitch_var = ctk.StringVar(self)

    items = os.listdir(devicegroups)
    self.groupcomboboxoptions = []
    for item in items:
        if os.path.isdir(item):
            self.tftpgrpcombxstrgrp.append(item)

    def tftpgrpcombxstrgrp_callback(self):
        self.backuptftpgrptbl.delete(*self.backuptftpgrptbl.get_children())
        self.tftpgrpcombxstrgrp_var.set(self.grpnamecbx.get())

        self.membersofselecgrp = grpselectiongettftp(
            self, self.tftpgrpcombxstrgrp_var.get()
        )

        count = 0

        for i in self.membersofselecgrp:
            count += 1
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
            ) = getdevicefromid(i)

            self.backuptftpgrptbl.insert(
                parent="",
                index="end",
                iid=count,
                text=count,
                values=(
                    f"{retid}",
                    f"{retname}",
                    f"{retip}",
                    f"{rettype}",
                    f"{retdescription[:10]}",
                ),
            )

            self.grpnameswitch.configure(
                state="normal",
                fg_color="yellow2",
                button_color="dark slate gray",
                border_color="dark slate gray",
                progress_color="pale green",
                text_color="black",
            )

            self.editgrpstatuslbl.configure(text="Confirm selection")

    def grpnameswitch_event():

        if self.grpnameswitch_var.get() == "on":

            self.grpnamecbx.configure(
                state="disabled",
                fg_color="gray80",
                button_color="gray",
                border_color="gray",
            )
            self.grpnamelbl.configure(state="disabled")
            self.backuptftpgrptbl.configure(style="dbgray.Treeview")

            self.bktypelbl.configure(state="normal")
            self.chkbxrunningcfg.configure(
                state="normal",
                fg_color="green",
                hover_color="dark slate gray",
                border_color="dark slate gray",
                text_color_disabled="dark slate gray",
            )
            self.chkbxstartupcfg.configure(
                state="normal",
                fg_color="green",
                hover_color="dark slate gray",
                border_color="dark slate gray",
                text_color_disabled="dark slate gray",
            )
            self.fileidlbl.configure(state="normal")
            self.fileidselec.configure(
                state="normal",
                fg_color="yellow2",
                font=("arial", 14, "bold"),
                border_color="dark slate gray",
                button_color="dark slate gray",
                dropdown_fg_color="khaki",
                border_width=2,
                dropdown_hover_color="khaki3",
                dropdown_font=("arial", 14, "bold"),
            )
            self.fileidswitch.configure(
                state="normal",
                fg_color="yellow2",
                button_color="dark slate gray",
                border_color="dark slate gray",
            )

        if self.grpnameswitch_var.get() == "off":

            self.grpnamecbx.configure(
                state="normal",
                fg_color="yellow2",
                button_color="dark slate gray",
                border_color="dark slate gray",
            )
            self.grpnamelbl.configure(state="normal")
            self.backuptftpgrptbl.configure(style="db.Treeview")

            self.bktypelbl.configure(state="disabled")
            self.chkbxrunningcfg.configure(
                state="disabled",
                fg_color="gray",
                hover_color="gray",
                border_color="gray",
                text_color_disabled="gray",
            )
            self.chkbxstartupcfg.configure(
                state="disabled",
                fg_color="gray",
                hover_color="gray",
                border_color="gray",
                text_color_disabled="gray",
            )
            self.fileidlbl.configure(state="disabled")
            self.fileidselec.configure(
                state="disabled",
                fg_color="gray80",
                button_color="gray",
                border_color="gray",
            )
            self.fileidswitch.configure(
                state="disabled",
                fg_color="gray50",
                button_color="gray30",
                border_color="gray30",
                progress_color="gray30",
                text_color="gray20",
            )

        count = 0

        for i in self.membersofselecgrp:
            count += 1

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
            ) = getdevicefromid(i)

            self.selectedgrpbucket_var.append(
                [retid, retname, retip, retusername, retpassword, rettype]
            )
            self.selectedgrpbucket_var_ids.append(retid)

        self.editgrpstatuslbl.configure(
            text=f"{self.tftpgrpcombxstrgrp_var.get()} selected"
        )

    def btnbackup_event():

        self.outputxtbx.configure(state="normal")
        self.btnbackup.configure(
            state="disabled", fg_color="gray", border_color="gray40"
        )
        self.fileidswitch.configure(
            state="disabled",
            fg_color="gray50",
            button_color="gray30",
            border_color="gray30",
            progress_color="gray",
            text_color="gray20",
        )

        count = 0
        self.update_idletasks()

        for i in self.selectedgrpbucket_var:
            buckethostname = ""
            bucketip = ""
            bucketusername = ""
            bucketpassword = ""
            buckettype = ""

            self.selectedgrpbucket_var[count][0]
            buckethostname = self.selectedgrpbucket_var[count][1]
            bucketip = self.selectedgrpbucket_var[count][2]
            bucketusername = self.selectedgrpbucket_var[count][3]
            bucketpassword = self.selectedgrpbucket_var[count][4]
            buckettype = self.selectedgrpbucket_var[count][5]

            count += 1

            device = {
                "device_type": f"{buckettype}",
                "host": f"{bucketip}",
                "username": f"{bucketusername}",
                "password": f"{bucketpassword}",
                "secret": f"{bucketpassword}",
            }

            hostname = ""
            filedatetime = str(time.strftime("%Y-%m-%d-%H-%M-%S"))

            self.outputxtbx.insert(
                INSERT, f"Starting ***--- {buckethostname} ({bucketip}) ---*** \n"
            )
            copy_command = f"copy {self.startuporrunning_var.get()} tftp://{tftpserver} {directorylocation}"

            try:
                net_connect = ConnectHandler(**device)

                net_connect.enable()

                hostname = net_connect.find_prompt()[:-1]
                copy_command = f"copy {self.startuporrunning_var.get()} tftp://{tftpserver}{directorylocation}"
                self.outputxtbx.insert(INSERT, f"Command:\n{copy_command}")
                output = net_connect.send_command_timing(copy_command)

                if "Address or name" in output:
                    output += net_connect.send_command_timing("\n")

                if "Destination filename" in output:

                    output += net_connect.send_command_timing(
                        f"{directorylocation}"
                        + "/"
                        + f"{hostname}_"
                        + f"{filedatetime}_"
                        + f"{self.startuporrunning_var.get()}_"
                        + f"{self.fileidselec.get()}"
                        + "\n"
                    )

                    net_connect.disconnect
            except NetMikoAuthenticationException as AuthException:

                self.outputxtbx.insert(
                    INSERT,
                    f"***--- {buckethostname} ({bucketip}) ---*** \n Authentication Error \n {AuthException}",
                )
                continue
            except NetMikoTimeoutException as TimeoutException:

                self.outputxtbx.insert(
                    INSERT,
                    f"Timeout Exception Error ***--- {buckethostname} ({bucketip}) ---*** \n {TimeoutException}",
                )
                continue
            except SSHException as sshexception:

                self.outputxtbx.insert(
                    INSERT,
                    f"SSHException Error ***--- {buckethostname} ({bucketip}) ---*** \n {sshexception}",
                )
                continue
            except Exception as unknown_error:

                self.outputxtbx.insert(
                    INSERT,
                    f"Unknown Error ***--- {buckethostname} ({bucketip}) ---*** \n  \n {unknown_error}",
                )
                continue
            finally:
                if net_connect == True:
                    net_connect.disconnect
                self.update_idletasks()
                self.outputxtbx.insert(
                    INSERT, f"\nMoving file from temporary location.\n"
                )
                self.outputxtbx.see("end")

            os.chdir(changetoDEVICEDATAdirectory)

            if hostname == buckethostname:

                try:
                    for file_name in os.listdir(filesource):
                        source = filesource + file_name
                        destination = filedestination + "/" + hostname + "/" + file_name
                        self.outputxtbx.insert(INSERT, f"Filename:\n{file_name}\n")
                        if os.path.isfile(source):
                            shutil.copy(source, destination)
                            self.outputxtbx.insert(
                                INSERT, f"Location:\n{filedestination}{hostname}\n"
                            )
                except OSError as error:
                    pass
                finally:
                    self.outputxtbx.insert(
                        INSERT,
                        f"\n---*---*---*---*---*---*---*---*---*---*---*---*---*--- \n",
                    )
                    if len(os.listdir(filesource)) > 0:

                        for f in os.listdir(filesource):
                            os.remove(os.path.join(filesource, f))
                    else:
                        pass

            else:
                pass

        self.outputxtbx.configure(state="disabled")
        self.editgrpstatuslbl.configure(text="Task complete")

    def chkbxrunningcfg_event(self):

        self.startuporrunning_var.set("running-config")

        self.chkbxstartupcfg.deselect()

    def chkbxstartupcfg_event(self):

        self.startuporrunning_var.set("startup-config")

        self.chkbxrunningcfg.deselect()

    def fileidselec_callback(self):

        self.editgrpstatuslbl.configure(
            text=f'Confirm "{self.fileidselec.get()}" selection'
        )
        self.fileidselec.configure(width=220)

    def fileidswitch(self):

        self.fileidselec.configure(width=220)

        if self.fileidswitch_var.get() == "on":

            if self.fileidselec.get() == "Select":

                messagebox.showinfo(
                    parent=self.tftpbackupwindowgrp,
                    title="Selection invalid",
                    message="Please select a valid file identifier.",
                )
                self.fileidswitch.deselect()

            else:

                self.grpnameswitch.configure(
                    state="disabled",
                    progress_color="gray",
                    fg_color="gray50",
                    button_color="gray30",
                    border_color="gray30",
                )
                self.bktypelbl.configure(state="disabled")
                self.chkbxrunningcfg.configure(
                    state="disabled",
                    fg_color="gray",
                    border_color="gray",
                    text_color_disabled="gray",
                )
                self.chkbxstartupcfg.configure(
                    state="disabled",
                    fg_color="gray",
                    border_color="gray",
                    text_color_disabled="gray",
                )
                self.fileidlbl.configure(fg="gray")
                self.fileidselec.configure(
                    state="disabled",
                    fg_color="gray80",
                    button_color="gray",
                    border_color="gray",
                )
                self.fileidswitch.configure(fg_color="yellow2")

                self.outputxtbx.configure(state="normal", bg="light yellow")
                self.outputxtbx.insert(
                    INSERT, f"Group: {self.tftpgrpcombxstrgrp_var.get()}\n"
                )
                self.outputxtbx.insert(
                    INSERT,
                    f"Member ID's: {str(self.selectedgrpbucket_var_ids)[1:-1]}\n",
                )
                self.outputxtbx.insert(
                    INSERT, f"Backing up the: {self.startuporrunning_var.get()}\n"
                )
                self.outputxtbx.insert(
                    INSERT, f"File identified as: '{self.fileidselec.get()}'\n"
                )
                self.outputxtbx.configure(state="disabled")

                self.btnbackup.configure(
                    state="normal", fg_color="green", border_color="green4"
                )

                self.editgrpstatuslbl.configure(text="Ready to run backup request")

        else:

            self.outputxtbx.configure(state="normal", bg="light yellow")
            self.outputxtbx.delete("1.0", END)
            self.outputxtbx.configure(bg="gray64", state="disabled")
            self.btnbackup.configure(
                state="disabled", fg_color="gray", border_color="gray40"
            )

        if self.fileidswitch_var.get() == "off":

            self.grpnameswitch.configure(
                state="normal",
                progress_color="pale green",
                fg_color="yellow2",
                button_color="dark slate gray",
                border_color="dark slate gray",
            )
            self.bktypelbl.configure(state="normal", fg="black")
            self.chkbxrunningcfg.configure(
                state="normal",
                fg_color="green",
                hover_color="dark slate gray",
                border_color="dark slate gray",
                text_color_disabled="dark slate gray",
            )
            self.chkbxstartupcfg.configure(
                state="normal",
                fg_color="green",
                hover_color="dark slate gray",
                border_color="dark slate gray",
                text_color_disabled="dark slate gray",
            )
            self.fileidlbl.configure(state="normal", fg="black")
            self.fileidselec.configure(
                state="normal",
                fg_color="yellow2",
                font=("arial", 14, "bold"),
                border_color="dark slate gray",
                button_color="dark slate gray",
                dropdown_fg_color="khaki",
                border_width=2,
                dropdown_hover_color="khaki3",
                dropdown_font=("arial", 14, "bold"),
            )
            self.editgrpstatuslbl.configure(text="Unlocked for change")

    self.tftpbackupwindowgrp = tk.Toplevel(master=self)
    self.tftpbackupwindowgrp.title("Backup group TFTP")
    self.tftpbackupwindowgrp.geometry("781x830+200+200")
    self.tftpbackupwindowgrp.minsize(500, 800)
    self.tftpbackupwindowgrp.maxsize(900, 850)
    self.tftpbackupwindowgrp.configure(background="powder blue")
    self.tftpbackupwindowgrp.wm_iconphoto(
        False, (ImageTk.PhotoImage(Image.open(pythonicon)))
    )

    self.tftpbackupwindowgrp.attributes("-topmost", "true")
    self.tftpbackupwindowgrp.transient(self)
    self.tftpbackupwindowgrp.update_idletasks()
    self.tftpbackupwindowgrp.grab_set()

    self.tftpbackupwindowgrp.grid_columnconfigure(0, weight=1)
    self.tftpbackupwindowgrp.grid_columnconfigure(1, weight=1)
    self.tftpbackupwindowgrp.grid_columnconfigure(2, weight=1)

    self.createlabel = ctk.CTkLabel(
        self.tftpbackupwindowgrp,
        text="Backup a Group configuration (TFTP)",
        font=("arial", 22, "bold"),
    )
    self.createlabel.grid(row=0, column=0, sticky=EW, columnspan=3, pady=(20, 16))
    self.separator1 = ttk.Separator(self.tftpbackupwindowgrp, orient="horizontal")
    self.separator1.grid(row=1, sticky=EW, columnspan=3, padx=(40, 10), pady=10)

    self.grpnamelbl = Label(
        self.tftpbackupwindowgrp,
        text="Group selection",
        font=("arial", 14, "bold"),
        bg="powder blue",
        fg="black",
    )
    self.grpnamelbl.grid(row=2, column=0, sticky=W, padx=(25, 10), pady=10)
    self.grpnamecbx = ctk.CTkComboBox(
        self.tftpbackupwindowgrp,
        width=220,
        fg_color="yellow2",
        font=("arial", 14, "bold"),
        border_color="dark slate gray",
        button_color="dark slate gray",
        dropdown_fg_color="khaki",
        border_width=2,
        dropdown_hover_color="khaki3",
        dropdown_font=("arial", 14, "bold"),
        variable=self.tftpgrpcombxstrgrp_var,
        values=self.tftpgrpcombxstrgrp,
        command=lambda v: tftpgrpcombxstrgrp_callback(self),
    )
    self.grpnamecbx.grid(row=2, column=1, sticky="w", padx=(20, 5), pady=10)
    self.grpnamecbx.set("select a group")
    self.grpnameswitch = ctk.CTkSwitch(
        self.tftpbackupwindowgrp,
        text="Unlock | Lock",
        command=grpnameswitch_event,
        variable=self.grpnameswitch_var,
        onvalue="on",
        offvalue="off",
        switch_width=40,
        switch_height=20,
        fg_color="gray50",
        button_color="gray30",
        border_width=2,
        border_color="gray30",
        progress_color="pale green",
        text_color="gray20",
    )
    self.grpnameswitch.grid(row=2, column=2)
    self.grpnameswitch.configure(state="disabled")

    self.backuptftpgrptbl = ttk.Treeview(
        self.tftpbackupwindowgrp, selectmode="none", height=10, style="db.Treeview"
    )
    self.backuptftpgrptbl.grid(
        row=3, column=0, sticky=EW, padx=(25, 0), pady=10, columnspan=3
    )

    self.bktftpgrptblscroll = ttk.Scrollbar(
        self.tftpbackupwindowgrp,
        orient=tk.VERTICAL,
        command=self.backuptftpgrptbl.yview,
    )
    self.backuptftpgrptbl.configure(yscrollcommand=self.bktftpgrptblscroll.set)
    self.bktftpgrptblscroll.grid(row=3, column=3, sticky="nes", padx=(0, 30), pady=10)

    self.backuptftpgrptbl["columns"] = ("1", "2", "3", "4", "5")
    self.backuptftpgrptbl["show"] = "headings"
    self.backuptftpgrptbl.column("1", width=50, anchor="center")
    self.backuptftpgrptbl.column("2", width=100, anchor="center")
    self.backuptftpgrptbl.column("3", width=100, anchor="center")
    self.backuptftpgrptbl.column("4", width=100, anchor="center")
    self.backuptftpgrptbl.column("5", width=200, anchor="center")
    self.backuptftpgrptbl.heading("1", text="id")
    self.backuptftpgrptbl.heading("2", text="hostname")
    self.backuptftpgrptbl.heading("3", text="ip")
    self.backuptftpgrptbl.heading("4", text="type")
    self.backuptftpgrptbl.heading("5", text="Description")

    self.tftpbackupwindowgrp.geometry("780x820")

    self.bktypelbl = Label(
        self.tftpbackupwindowgrp,
        text="Backup Type",
        font=("arial", 14, "bold"),
        bg="powder blue",
        fg="black",
        state="disabled",
    )
    self.bktypelbl.grid(row=4, column=0, sticky=W, padx=(25, 10), pady=10)
    self.chkbxrunningcfg = ctk.CTkCheckBox(
        self.tftpbackupwindowgrp,
        text="running-config",
        onvalue="on",
        offvalue="off",
        fg_color="gray",
        hover_color="dark slate gray",
        border_color="gray",
        border_width=2,
        text_color_disabled="gray",
        command=lambda: chkbxrunningcfg_event(self),
    )
    self.chkbxrunningcfg.grid(row=4, column=1, pady=(10, 10), padx=(40, 20))
    self.chkbxstartupcfg = ctk.CTkCheckBox(
        self.tftpbackupwindowgrp,
        text="startup-config",
        onvalue="on",
        offvalue="off",
        fg_color="gray",
        hover_color="dark slate gray",
        border_color="gray",
        border_width=2,
        text_color_disabled="gray",
        command=lambda: chkbxstartupcfg_event(self),
    )
    self.chkbxstartupcfg.grid(row=4, column=2, pady=(10, 10), padx=(40, 20))
    self.chkbxrunningcfg.select()
    self.startuporrunning_var.set("running-config")
    self.chkbxrunningcfg.configure(state="disabled")
    self.chkbxstartupcfg.configure(state="disabled")

    self.fileidlbl = Label(
        self.tftpbackupwindowgrp,
        state="disabled",
        text="File identifier",
        font=("arial", 14, "bold"),
        bg="powder blue",
        fg="black",
    )
    self.fileidlbl.grid(row=5, column=0, sticky=W, padx=(25, 10), pady=10)
    self.fileidoptions = ["Daily", "Weekly", "Monthly", "Golden", "Silver"]
    self.fileidselec = ctk.CTkComboBox(
        self.tftpbackupwindowgrp,
        state="normal",
        font=("arial", 14, "bold"),
        values=self.fileidoptions,
        dropdown_font=("arial", 16, "bold"),
        command=lambda v: fileidselec_callback(self),
        width=220,
    )
    self.fileidselec.grid(row=5, column=1, sticky=W, padx=(15, 10), pady=10)
    self.fileidselec.set("Select")
    self.fileidselec.configure(state="disabled")
    self.fileidswitch = ctk.CTkSwitch(
        self.tftpbackupwindowgrp,
        text="Unlock | Lock",
        state="disabled",
        command=lambda: fileidswitch(self),
        variable=self.fileidswitch_var,
        onvalue="on",
        offvalue="off",
        switch_width=40,
        switch_height=20,
        fg_color="gray50",
        button_color="gray30",
        border_width=2,
        border_color="gray30",
        progress_color="pale green",
        text_color="gray20",
    )
    self.fileidswitch.grid(row=5, column=2, padx=(15, 25), pady=10)

    self.separator2 = ttk.Separator(self.tftpbackupwindowgrp, orient="horizontal")
    self.separator2.grid(row=6, sticky=EW, columnspan=3, padx=(40, 0), pady=10)

    self.outputxtbx = scrolledtext.ScrolledText(
        self.tftpbackupwindowgrp,
        font="arial 12",
        height=10,
        width=25,
        bg="gray64",
        wrap=WORD,
        state="disabled",
    )
    self.outputxtbx.grid(
        row=7, column=0, sticky=EW, padx=(25, 0), pady=10, columnspan=3
    )

    self.progstatus = ctk.CTkProgressBar(
        self.tftpbackupwindowgrp,
        progress_color="green4",
        border_width=1,
        border_color="dark slate gray",
    )
    self.progstatus.grid(row=8, column=0, sticky=EW, padx=(25, 0), pady=5, columnspan=3)
    self.progstatus.set(0)

    self.btnbackup = ctk.CTkButton(
        self.tftpbackupwindowgrp,
        text="Backup",
        width=120,
        fg_color="gray",
        hover_color="green4",
        font=("arial", 12, "bold"),
        border_width=2,
        border_color="gray40",
        command=btnbackup_event,
        state="disabled",
    )
    self.btnbackup.grid(row=9, column=0, pady=5, padx=(25, 1), sticky=W)
    self.editgrpstatuslbl = Label(
        self.tftpbackupwindowgrp,
        text="Select a Group",
        font=("arial", 14, "bold"),
        bg="powder blue",
        fg="OrangeRed2",
    )
    self.editgrpstatuslbl.grid(row=9, column=1, pady=5, sticky=W, padx=10)
    self.btnexit = ctk.CTkButton(
        self.tftpbackupwindowgrp,
        text="EXIT",
        width=120,
        fg_color="red2",
        font=("arial", 12, "bold"),
        command=self.tftpbackupwindowgrp.destroy,
        hover_color="red4",
        border_width=2,
        border_color="red4",
    )
    self.btnexit.grid(row=9, column=2, pady=5, padx=(0, 0), sticky=E)
