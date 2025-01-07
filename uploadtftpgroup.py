from settings import *
from tkinter import *
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import ImageTk, Image
import customtkinter as ctk
import os
import json
from connecttodb import getdevicefromid
import shutil
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException


def configuploadtftpgroup(self):

    self.idsofmembers = []

    self.tftpgrpseleccbx = []
    self.tftpgrpcombxstr_var = ctk.StringVar(self)

    self.grpnameswitch_var = ctk.StringVar(self)

    self.tftpselectedid = StringVar(self)
    self.setbackuptypevar = StringVar(self)
    self.setfileidtypevar = StringVar(self)
    self.filename = StringVar(self)
    self.filedest = StringVar(self)
    self.filesrc = StringVar(self)
    self.tftprootdir = StringVar(self)
    self.tftprootdir.set(tftprootdir)

    self.checkboxcopygrp_var = ctk.StringVar(value="off")
    self.checkboxreplgrp_var = ctk.StringVar(value="off")
    self.checkboxcrsgrp_var = ctk.StringVar(value="off")
    self.checkboxcstrngrp_var = ctk.StringVar(value="off")
    self.chkbxrunningcfgrp_var = ctk.StringVar(value="off")
    self.chkbxstartupcfgrp_var = ctk.StringVar(value="off")

    self.tftpuploadcmd = ctk.StringVar(self)

    self.running_startup_vargrp = StringVar(self)

    self.tftpuploadgroupw = tk.Toplevel()
    self.tftpuploadgroupw.geometry("730x820+200+200")
    self.tftpuploadgroupw.title("TFTP Upload to group")
    self.tftpuploadgroupw.configure(background="powder blue")

    self.tftpuploadgroupw.wm_iconphoto(
        False, (ImageTk.PhotoImage(Image.open(pythonicon)))
    )

    self.tftpuploadgroupw.attributes("-topmost", "true")
    self.tftpuploadgroupw.transient(self)
    self.tftpuploadgroupw.update_idletasks()
    self.tftpuploadgroupw.grab_set()

    def tftpgrpgobtn(self):
        self.grpnotetxtbx.configure(state="normal", bg="light goldenrod yellow")
        self.grpnotetxtbx.insert("end", "This is a list of id members of the group\n")
        self.grpnotetxtbx.insert("end", f"{self.idsofmembers}\n")

        self.tftpgrpgo.configure(state="disabled", fg_color="gray", border_color="gray")

        self.grpnameswitch.configure(
            state="disabled",
            fg_color="gray50",
            button_color="gray30",
            border_color="gray30",
            progress_color="gray",
            text_color="gray20",
        )

        self.checkboxcopygrp.select()
        self.checkboxcopygrp.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )
        self.chkbxrunningcfgrp.select()
        self.chkbxrunningcfgrp.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )
        self.checkboxreplgrp.deselect()
        self.checkboxreplgrp.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )
        self.chkbxstartupcfgrp.deselect()
        self.chkbxstartupcfgrp.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )
        self.checkboxcrsgrp.deselect()
        self.checkboxcrsgrp.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )
        self.checkboxcstrngrp.deselect()
        self.checkboxcstrngrp.configure(
            state="disabled", fg_color="gray", border_color="gray"
        )

        count = 0
        for i in self.idsofmembers:
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

            self.grpnotetxtbx.insert(
                "end", f"id:{retid}\nhostname:{retname}\nip:{retip}\nfile:{retgolden}\n"
            )

            self.progstatus1.set(0.3)
            self.update_idletasks()

            os.chdir(self.tftprootdir.get())

            self.grpnotetxtbx.insert(
                INSERT, f"2) Looking for file in the TFTP staging area:\n{retgolden}\n"
            )

            if self.chkbxstartupcfgrp_var.get() == "on":
                self.running_startup_vargrp.set("startup-config")

            elif self.chkbxrunningcfgrp_var.get() == "on":
                self.running_startup_vargrp.set("running-config")

            else:
                pass

            if os.path.isfile(retgolden):

                self.tftpstatuslbl.configure(text=f"Running task on: {retname}")
                self.progstatuslbl.configure(text=f"id:{retid} ({retname})")
                self.update_idletasks()

                cisco_device = {
                    "device_type": f"{rettype}",
                    "host": f"{retip}",
                    "username": f"{retusername}",
                    "password": f"{retpassword}",
                    "port": 22,
                    "secret": f"{retpassword}",
                    "verbose": True,
                }

                self.grpnotetxtbx.insert(
                    INSERT, f"3) Initiating Connection to : {retname}\n"
                )

                conn = ConnectHandler(**cisco_device)
                conn_prompt = conn.find_prompt()
                if ">" in conn_prompt:
                    conn.enable()
                output = conn.send_command(f"\n")

                self.grpnotetxtbx.insert(
                    INSERT,
                    f"4) The config mode on the device is: {conn.check_config_mode()}\n",
                )

                self.progstatus1.set(0.4)
                self.update_idletasks()

                try:
                    f"device{str(1)}"
                    net_connect = ConnectHandler(**cisco_device)

                    net_connect.enable()
                    hostname = net_connect.find_prompt()[:-1]

                    self.grpnotetxtbx.insert(
                        INSERT, f"5) The hostname on the device is: {hostname}\n"
                    )

                    self.tftpstatuslbl.configure(
                        font=("arial", 12, "bold"), text="Task in progress"
                    )
                    self.progstatus1.set(0.5)
                    self.update_idletasks()

                    if self.checkboxcopygrp_var.get() == "on":

                        self.tftpuploadcmd.set(
                            f"copy tftp://{tftpserver}{tftprootdir}/{retgolden} {self.running_startup_vargrp.get()}"
                        )
                        self.grpnotetxtbx.insert(
                            INSERT,
                            f"6) Sending the command: {self.tftpuploadcmd.get()}\n",
                        )

                        output = net_connect.send_command_timing(
                            self.tftpuploadcmd.get()
                        )
                        if "Address or name" in output:
                            output += net_connect.send_command_timing(f"{tftpserver}\n")

                        if "Source filename" in output:
                            output += net_connect.send_command_timing(f"{retgolden}\n")

                            net_connect.disconnect
                        if "Destination filename" in output:
                            output += net_connect.send_command_timing(f"\n")

                            self.grpnotetxtbx.insert(
                                INSERT, f"7) Running the command on the device.\n"
                            )

                        self.progstatus1.set(0.7)
                        self.update_idletasks()

                        if (
                            self.chkbxrunningcfgrp_var.get() == "on"
                            and self.checkboxcrsgrp_var.get() == "on"
                        ):

                            copy_command1 = "copy running-config startup-config"
                            output1 = net_connect.send_command_timing(copy_command1)
                            self.grpnotetxtbx.insert(INSERT, f"Output1:\n{output1}\n")

                            if "Destination filename" in output1:
                                output1 += net_connect.send_command_timing("\n")
                                self.grpnotetxtbx.insert(
                                    INSERT,
                                    f"copy running-config startup-config: COMPLETED\n{output1}\n",
                                )
                            else:
                                pass

                            self.progstatus1.set(0.8)
                            self.update_idletasks()

                        if (
                            self.chkbxstartupcfgrp_var.get() == "on"
                            and self.checkboxcstrngrp_var.get() == "on"
                        ):

                            copy_command1 = "copy startup-config running-config "
                            output1 = net_connect.send_command_timing(copy_command1)
                            self.grpnotetxtbx.insert(INSERT, f"Output1:\n{output1}\n")

                            if "Destination filename" in output1:
                                output1 += net_connect.send_command_timing("\n")
                                self.grpnotetxtbx.insert(
                                    INSERT,
                                    f"copy startup-config running-config: COMPLETED\n{output1}\n",
                                )

                            else:
                                pass

                            self.progstatus1.set(0.8)
                            self.update_idletasks()

                        if (
                            self.chkbxstartupcfgrp_var.get() == "on"
                            and self.checkboxcstrngrp_var.get() == "on"
                        ):

                            copy_command1 = "copy startup-config running-config"
                            output1 = net_connect.send_command_timing(copy_command1)
                            self.grpnotetxtbx.insert(INSERT, f"Output1:\n{output1}\n")

                            if "Destination filename" in output1:
                                output1 += net_connect.send_command_timing("\n")
                                self.grpnotetxtbx.insert(
                                    INSERT,
                                    f"startup-config > running-config output:\n{output1}\n",
                                )
                                self.grpnotetxtbx.insert(
                                    INSERT,
                                    "------------------------------------------------\n",
                                )
                                self.grpnotetxtbx.insert(
                                    INSERT,
                                    f"Request completed: startup-config has been copied to the running-config\n",
                                )
                                self.grpnotetxtbx.insert(
                                    INSERT,
                                    "------------------------------------------------\n",
                                )
                            else:
                                pass

                            self.progstatus1.set(0.8)
                            self.grpnotetxtbx.see("end")
                            self.update_idletasks()

                    elif self.checkboxreplgrp_var.get() == "on":

                        self.tftpuploadcmd.set(
                            f"configure replace tftp://{tftpserver}{tftprootdir}/{retgolden} force"
                        )
                        self.grpnotetxtbx.insert(
                            INSERT,
                            f"6) Sending the command: {self.tftpuploadcmd.get()}\n",
                        )

                        output = net_connect.send_command_timing(
                            self.tftpuploadcmd.get()
                        )
                        self.grpnotetxtbx.insert(INSERT, f"7) Output:\n{output}\n")

                        if self.checkboxcrsgrp_var.get() == "on":

                            copy_command1 = "copy running-config startup-config"
                            output1 = net_connect.send_command_timing(copy_command1)
                            self.grpnotetxtbx.insert(
                                INSERT, f"8) Output1:\n{output1}\n"
                            )

                            if "Destination filename" in output1:
                                output1 += net_connect.send_command_timing("\n")
                                self.grpnotetxtbx.insert(
                                    INSERT,
                                    f"8a) running-config > startup-config output:\n{output1}\n",
                                )
                                self.grpnotetxtbx.insert(
                                    INSERT,
                                    "------------------------------------------------\n",
                                )
                                self.grpnotetxtbx.insert(
                                    INSERT,
                                    f"Request completed: running-config has been copied to the startup-config\n",
                                )
                                self.grpnotetxtbx.insert(
                                    INSERT,
                                    "------------------------------------------------\n",
                                )
                            else:
                                pass

                        else:
                            pass

                        self.progstatus.set(0.8)
                        self.grpnotetxtbx.see("end")
                        self.update_idletasks()

                except NetMikoAuthenticationException as AuthException:

                    self.grpnotetxtbx.insert(
                        INSERT,
                        "5) (uploadtftpgroup.py 290) Authentication Error \n"
                        % AuthException,
                    )
                    continue
                except NetMikoTimeoutException as TimeoutException:

                    self.grpnotetxtbx.insert(
                        INSERT,
                        "5) (uploadtftpgroup.py 295) TimeoutException Error \n"
                        % TimeoutException,
                    )
                    continue
                except SSHException as sshexception:

                    self.grpnotetxtbx.insert(
                        INSERT,
                        "5) (uploadtftpgroup.py 299) An netmiko SSHException Error \n"
                        % sshexception,
                    )
                    continue
                except Exception as unknown_error:

                    self.grpnotetxtbx.insert(
                        INSERT,
                        "5) An error occured in the try block unknown_error\n"
                        % unknown_error,
                    )
                    continue

                finally:

                    net_connect.disconnect
                    self.grpnotetxtbx.insert(
                        INSERT, "------------------------------------------------\n"
                    )
                    self.grpnotetxtbx.insert(
                        INSERT,
                        f"Request was completed {retname} has a new {self.running_startup_vargrp.get()}\n",
                    )
                    self.grpnotetxtbx.insert(
                        INSERT, "------------------------------------------------\n"
                    )

                    if os.path.exists(f"{tftprootdir}/{retgolden}"):
                        os.remove(f"{tftprootdir}/{retgolden}")

                    else:

                        self.grpnotetxtbx.insert(
                            INSERT,
                            f"9) (finally|else 352) I couldn't delete the file:\n{tftprootdir}/{retgolden}",
                        )

                    self.grpnotetxtbx.insert(
                        INSERT,
                        f"-----------------------------End ({retname})-------------------------------\n",
                    )
                    self.tftpstatuslbl.configure(text="Task Completed")
                    self.grpnotetxtbx.see("end")
                    self.progstatus1.set(1)
                    self.update_idletasks()

            else:

                self.grpnotetxtbx.insert(INSERT, f"File or Location ERROR\n")
                self.grpnotetxtbx.insert(INSERT, f"1) Expected file:\n {retgolden}\n")
                self.grpnotetxtbx.insert(
                    INSERT, f"2) Expected location:\n {self.tftprootdir.get()}\n"
                )

        self.grpnotetxtbx.insert(
            INSERT,
            f"--------------------Tasks Finished ({self.tftpgrpcombxstr_var.get()})-------------------------------",
        )
        self.grpnotetxtbx.see("end")
        self.grpnotetxtbx.configure(state="disabled", bg="light goldenrod yellow")

    def populatemembxg(self, *args, **kwargs):

        os.chdir(devicegroups)

        items = os.listdir(devicegroups)

        for item in items:
            if os.path.isdir(item):

                self.tftpgrpseleccbx.append(item)

        self.tftpgrpcombx.configure(values=self.tftpgrpseleccbx)

    def tftpgrpcombxcallback(self):

        self.grpnameswitch.configure(
            state="normal",
            fg_color="pale green",
            button_color="dark slate gray",
            border_color="dark slate gray",
            text_color="black",
        )
        tftpgrpcbxselc(self)

    def checkboxcopygrp_event(self):

        if self.checkboxcopygrp.get() == "on":

            self.checkboxreplgrp.deselect()

            self.chkbxrunningcfgrp.configure(
                border_color="dark slate gray", state="normal"
            )

            self.chkbxstartupcfgrp.configure(
                border_color="dark slate gray", state="normal"
            )

            self.checkboxcstrngrp.configure(
                border_color="dark slate gray", state="normal"
            )

            self.checkboxcrsgrp.deselect()
            self.checkboxcrsgrp.configure(
                border_color="dark slate gray", state="normal"
            )

            self.checkboxcstrngrp.deselect()
            self.checkboxcstrngrp.configure(border_color="gray", state="disabled")

            self.chkbxrunningcfgrp.select()

        else:

            self.checkboxreplgrp.select()

            self.chkbxrunningcfgrp.deselect()
            self.chkbxrunningcfgrp.configure(border_color="gray", state="disabled")

            self.chkbxstartupcfgrp.deselect()
            self.chkbxstartupcfgrp.configure(border_color="gray", state="disabled")

            self.checkboxcstrngrp.deselect()
            self.checkboxcstrngrp.configure(border_color="gray", state="disabled")

            self.checkboxcrsgrp.deselect()
            self.checkboxcrsgrp.configure(
                border_color="dark slate gray", state="normal"
            )

    def checkboxreplgrp_event(self):

        self.checkboxcopygrp.deselect()

        if self.checkboxreplgrp.get() == "on":

            self.checkboxcrsgrp.deselect()
            self.checkboxcrsgrp.configure(
                border_color="dark slate gray", state="normal"
            )

            self.checkboxcstrngrp.deselect()
            self.checkboxcstrngrp.configure(border_color="gray", state="disabled")

            self.chkbxrunningcfgrp.deselect()
            self.chkbxrunningcfgrp.configure(border_color="gray", state="disabled")

            self.chkbxstartupcfgrp.deselect()
            self.chkbxstartupcfgrp.configure(border_color="gray", state="disabled")

            self.running_startup_vargrp.set("running-config")
        else:

            self.checkboxcopygrp.select()

            self.chkbxrunningcfgrp.configure(
                border_color="dark slate gray", state="normal"
            )
            self.chkbxrunningcfgrp.select()

            self.chkbxstartupcfgrp.deselect()
            self.chkbxstartupcfgrp.configure(
                border_color="dark slate gray", state="normal"
            )

            self.checkboxcrsgrp.deselect()

    def chkbxrunningcfgrp_event(self):

        if self.chkbxrunningcfgrp.get() == "on":
            self.chkbxstartupcfgrp.deselect()

            self.checkboxcrsgrp.configure(
                border_color="dark slate gray", state="normal"
            )

            self.checkboxcstrngrp.deselect()
            self.checkboxcstrngrp.configure(border_color="gray", state="disabled")

        else:
            self.chkbxstartupcfgrp.select()

            self.checkboxcrsgrp.deselect()
            self.checkboxcrsgrp.configure(border_color="gray", state="disabled")

            self.checkboxcstrngrp.deselect()
            self.checkboxcstrngrp.configure(
                border_color="dark slate gray", state="normal"
            )

    def chkbxstartupcfgrp_event(self):

        self.checkboxcstrngrp.deselect()

        if self.chkbxstartupcfgrp.get() == "on":

            self.chkbxrunningcfgrp.deselect()

            self.checkboxcrsgrp.deselect()

            self.checkboxcstrngrp.configure(
                border_color="dark slate gray", state="normal"
            )

            self.checkboxcrsgrp.configure(border_color="gray", state="disabled")

        else:

            self.chkbxrunningcfgrp.select()

            self.checkboxcrsgrp.deselect()
            self.checkboxcrsgrp.configure(
                border_color="dark slate gray", state="normal"
            )

            self.checkboxcstrngrp.configure(border_color="gray", state="disabled")

    def checkboxcrsgrp_event(self):
        pass

    def checkboxcstrngrp_event(self):
        pass

    def tftpgrpcbxselc(self):
        self.tftpgrptbl.delete(*self.tftpgrptbl.get_children())

        groudevicepath = os.path.join(devicegroups, self.tftpgrpcombx.get())

        dest_path = os.path.join(groudevicepath, self.tftpgrpcombx.get() + ".json")
        filetoread = open(dest_path)
        inputjsondata = json.load(filetoread)

        self.idsofmembers = inputjsondata["members"]

        count = 0

        for i in self.idsofmembers:
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

            self.tftpgrptbl.insert(
                parent="",
                index="end",
                iid=count,
                text=count,
                values=(f"{retid}", f"{retname}", f"{retip}", f"{retgolden}"),
            )

        self.tftpstatuslbl.configure(text="Number of devices in group: " + str(count))

    def tftpgrpconfirm(self):

        if self.grpnameswitch_var.get() == "on":

            self.tftpgrpcombx.configure(
                state="disabled",
                fg_color="gray80",
                border_color="gray",
                button_color="gray",
            )

            self.tftpgrptbl.configure(style="dbgray.Treeview")

            self.checkboxcopygrp.configure(
                state="normal", fg_color="green4", border_color="dark slate gray"
            )
            self.chkbxrunningcfgrp.configure(
                state="normal", fg_color="green4", border_color="dark slate gray"
            )
            self.checkboxreplgrp.configure(
                state="normal", fg_color="green4", border_color="dark slate gray"
            )
            self.chkbxstartupcfgrp.configure(
                state="normal", fg_color="green4", border_color="dark slate gray"
            )
            self.checkboxcrsgrp.configure(
                state="normal", fg_color="green4", border_color="dark slate gray"
            )
            self.checkboxcstrngrp.configure(fg_color="green4", border_color="gray")

            self.tftpgrpgo.configure(
                state="normal", fg_color="green4", border_color="dark green"
            )

            self.grpnotetxtbx.configure(state="normal", bg="light goldenrod yellow")
            devlist = []
            devlistcount = 0

            for child in self.tftpgrptbl.get_children():
                devlist.append(self.tftpgrptbl.item(child)["values"])

            for file in devlist:

                self.filesrc.set(
                    f"{devicesaveddata}/{devlist[devlistcount][1]}/{devlist[devlistcount][3]}"
                )

                self.filedest.set(f"{tftprootdir}/{devlist[devlistcount][3]}")

                try:
                    shutil.copy(self.filesrc.get(), self.filedest.get())
                    self.grpnotetxtbx.insert(
                        INSERT,
                        f"{devlistcount+1}) File ready: {devlist[devlistcount][3]}\n",
                    )

                except:

                    self.grpnotetxtbx.insert(
                        INSERT,
                        f"{devlistcount+1}) Problem preparing file: {devlist[devlistcount][3]}\n",
                    )

                devlistcount += 1
            self.grpnotetxtbx.configure(state="disabled")

        if self.grpnameswitch_var.get() == "off":

            self.tftpgrpcombx.configure(
                state="normal",
                fg_color="yellow2",
                border_color="dark slate gray",
                button_color="dark slate gray",
            )

            self.tftpgrptbl.configure(style="db.Treeview")

            self.grpnotetxtbx.configure(state="normal")
            self.grpnotetxtbx.delete("1.0", END)
            self.grpnotetxtbx.configure(state="disabled", bg="gray60")

            if len(os.listdir(filesource)) > 0:

                for f in os.listdir(filesource):
                    os.remove(os.path.join(filesource, f))

            self.checkboxcopygrp.select()
            self.checkboxcopygrp.configure(
                state="disabled", fg_color="gray", border_color="gray"
            )
            self.chkbxrunningcfgrp.select()
            self.chkbxrunningcfgrp.configure(
                state="disabled", fg_color="gray", border_color="gray"
            )
            self.checkboxreplgrp.deselect()
            self.checkboxreplgrp.configure(
                state="disabled", fg_color="gray", border_color="gray"
            )
            self.chkbxstartupcfgrp.deselect()
            self.chkbxstartupcfgrp.configure(
                state="disabled", fg_color="gray", border_color="gray"
            )
            self.checkboxcrsgrp.deselect()
            self.checkboxcrsgrp.configure(
                state="disabled", fg_color="gray", border_color="gray"
            )
            self.checkboxcstrngrp.deselect()
            self.checkboxcstrngrp.configure(
                state="disabled", fg_color="gray", border_color="gray"
            )

            self.tftpgrpgo.configure(
                state="disabled", fg_color="gray", border_color="gray"
            )

    self.topframea = ctk.CTkFrame(
        master=self.tftpuploadgroupw, fg_color="powder blue", height=30
    )
    self.topframea.pack(fill="both", expand=False, side="top")
    self.topframea.pack_propagate(True)
    self.lbltopa = ctk.CTkLabel(
        self.topframea,
        text="Upload a configuration to a group of devices.",
        font=("arial", 22, "bold"),
    )
    self.lbltopa.pack(pady=(15, 7), side="top")
    self.separator1 = ttk.Separator(self.topframea, orient="horizontal")
    self.separator1.pack(padx=20, pady=(5, 10), fill="x", expand=True, side="top")

    self.grpname = ctk.CTkLabel(
        self.topframea, text="Group name", font=("arial", 18, "bold")
    )
    self.grpname.pack(anchor="w", padx=(30, 30), pady=(1, 20), side="left")
    self.tftpgrpcombx = ctk.CTkComboBox(
        self.topframea,
        state="normal",
        command=lambda v: tftpgrpcombxcallback(self),
        variable=self.tftpgrpcombxstr_var,
        width=270,
        height=30,
        fg_color="yellow2",
        font=("arial", 14, "bold"),
        border_color="dark slate gray",
        button_color="dark slate gray",
        dropdown_fg_color="khaki",
        border_width=2,
        dropdown_hover_color="khaki3",
        dropdown_font=("arial", 14, "bold"),
    )
    self.tftpgrpcombx.pack(padx=(60, 0), pady=(1, 20), side="left")
    self.tftpgrpcombx.set("Group Selection")

    self.grpnameswitch = ctk.CTkSwitch(
        self.topframea,
        text="Unlock | Lock",
        onvalue="on",
        offvalue="off",
        switch_width=40,
        switch_height=20,
        fg_color="gray50",
        button_color="gray30",
        border_width=2,
        border_color="gray30",
        progress_color="yellow",
        text_color="gray20",
        command=lambda: tftpgrpconfirm(self),
        variable=self.grpnameswitch_var,
    )
    self.grpnameswitch.pack(padx=(0, 30), pady=(1, 20), side="right")
    self.grpnameswitch.configure(state="disabled")

    self.centerframe = ctk.CTkFrame(
        master=self.tftpuploadgroupw, fg_color="powder blue"
    )
    self.centerframe.pack(fill="both", expand=True, side="top")
    self.topframea.pack_propagate(True)

    self.grpnotetxtbx = scrolledtext.ScrolledText(
        master=self.centerframe,
        font="arial 12",
        height=10,
        bg="gray60",
        wrap=WORD,
        state="disabled",
    )
    self.grpnotetxtbx.pack(side="bottom", expand="True", fill="x", padx=(20, 20))

    self.tftpgrptbl = ttk.Treeview(
        self.centerframe, selectmode="none", height=10, style="db.Treeview"
    )
    self.tftpgrptbl.pack(side="left", expand="True", fill="both", padx=(20, 0))

    self.tftpgrptblscroll = ttk.Scrollbar(
        self.centerframe, orient="vertical", command=self.tftpgrptbl.yview
    )
    self.tftpgrptbl.configure(yscrollcommand=self.tftpgrptblscroll.set)
    self.tftpgrptblscroll.pack(
        side="right", expand="False", fill="y", anchor=E, padx=(0, 20)
    )

    self.tftpgrptbl["columns"] = ("1", "2", "3", "4")
    self.tftpgrptbl["show"] = "headings"
    self.tftpgrptbl.column("1", width=50, anchor="center")
    self.tftpgrptbl.column("2", width=100, anchor="center")
    self.tftpgrptbl.column("3", width=100, anchor="center")
    self.tftpgrptbl.column("4", width=400, anchor="e")
    self.tftpgrptbl.heading("1", text="id")
    self.tftpgrptbl.heading("2", text="hostname")
    self.tftpgrptbl.heading("3", text="ip")
    self.tftpgrptbl.heading("4", text="File")

    self.bottomframe1 = ctk.CTkFrame(
        master=self.tftpuploadgroupw, fg_color="powder blue"
    )
    self.bottomframe1.pack(fill="x")

    self.separator2 = ttk.Separator(master=self.bottomframe1, orient="horizontal")
    self.separator2.pack(padx=20, pady=(4, 5), fill="x", expand=True, side="top")

    self.checkboxcopygrp = ctk.CTkCheckBox(
        self.bottomframe1,
        state="disabled",
        command=lambda: checkboxcopygrp_event(self),
        variable=self.checkboxcopygrp_var,
        text="Copy(merge) config",
        onvalue="on",
        offvalue="off",
        fg_color="gray",
        hover_color="dark slate gray",
        border_color="gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.checkboxcopygrp.pack(side="left", anchor="n", pady=(10, 10), padx=(60, 20))
    self.checkboxreplgrp = ctk.CTkCheckBox(
        self.bottomframe1,
        state="disabled",
        command=lambda: checkboxreplgrp_event(self),
        variable=self.checkboxreplgrp_var,
        text="Replace running-config",
        onvalue="on",
        offvalue="off",
        fg_color="gray",
        hover_color="dark slate gray",
        border_color="gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.checkboxreplgrp.pack(side="left", anchor="n", pady=(10, 10), padx=(20, 20))
    self.separator3a = ttk.Separator(master=self.bottomframe1, orient="vertical")
    self.separator3a.pack(fill="y", expand=False, side="left", padx=20)
    self.checkboxcrsgrp = ctk.CTkCheckBox(
        self.bottomframe1,
        state="disabled",
        command=lambda: checkboxcrsgrp_event(self),
        variable=self.checkboxcrsgrp_var,
        text="copy runnning > startup",
        onvalue="on",
        offvalue="off",
        fg_color="gray",
        hover_color="dark slate gray",
        border_color="gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.checkboxcrsgrp.pack(side="left", anchor="n", pady=(10, 10), padx=(40, 20))

    self.bottomframe2 = ctk.CTkFrame(
        master=self.tftpuploadgroupw, fg_color="powder blue"
    )
    self.bottomframe2.pack(fill="x", ipadx=10)

    self.chkbxrunningcfgrp = ctk.CTkCheckBox(
        self.bottomframe2,
        state="disabled",
        command=lambda: chkbxrunningcfgrp_event(self),
        variable=self.chkbxrunningcfgrp_var,
        text="running-config",
        onvalue="on",
        offvalue="off",
        fg_color="gray",
        hover_color="dark slate gray",
        border_color="gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.chkbxrunningcfgrp.pack(side="left", anchor="n", pady=(10, 10), padx=(60, 20))
    self.chkbxstartupcfgrp = ctk.CTkCheckBox(
        self.bottomframe2,
        state="disabled",
        command=lambda: chkbxstartupcfgrp_event(self),
        variable=self.chkbxstartupcfgrp_var,
        text="startup-config",
        onvalue="on",
        offvalue="off",
        fg_color="gray",
        hover_color="dark slate gray",
        border_color="gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.chkbxstartupcfgrp.pack(side="left", anchor="n", pady=(10, 10), padx=(50, 70))
    self.separator3b = ttk.Separator(master=self.bottomframe2, orient="vertical")
    self.separator3b.pack(fill="y", expand=False, side="left", padx=20, pady=(0, 1))
    self.checkboxcstrngrp = ctk.CTkCheckBox(
        self.bottomframe2,
        state="disabled",
        command=lambda: checkboxcstrngrp_event(self),
        variable=self.checkboxcstrngrp_var,
        text="copy startup > runnning",
        onvalue="on",
        offvalue="off",
        fg_color="green4",
        hover_color="dark slate gray",
        border_color="gray",
        border_width=2,
        text_color_disabled="gray",
    )
    self.checkboxcstrngrp.pack(side="left", anchor="n", pady=(10, 10), padx=(40, 20))

    self.bottomframe3 = ctk.CTkFrame(
        master=self.tftpuploadgroupw, fg_color="powder blue"
    )
    self.bottomframe3.pack(fill="x", ipadx=50, pady=1)
    self.separator4 = ttk.Separator(master=self.bottomframe3, orient="horizontal")
    self.separator4.pack(padx=20, pady=(5, 5), fill="x", expand=True, side="top")
    self.tftpgrpgo = ctk.CTkButton(
        self.bottomframe3,
        state="disabled",
        text="GoGroup",
        width=150,
        fg_color="gray",
        hover_color="green4",
        command=lambda: tftpgrpgobtn(self),
    )
    self.tftpgrpgo.pack(padx=(30, 30), pady=(10, 5), side="left")
    self.tftpstatuslbl = Label(
        self.bottomframe3,
        text="Select a Group ",
        font=("arial", 14, "bold"),
        bg="powder blue",
        fg="OrangeRed2",
    )
    self.tftpstatuslbl.pack(padx=(30, 30), pady=(10, 5), side="left")
    self.tftpgrpexit = ctk.CTkButton(
        self.bottomframe3,
        text="Exit",
        width=150,
        fg_color="red3",
        hover_color="red4",
        command=self.tftpuploadgroupw.destroy,
        font=("arial", 12, "bold"),
        border_width=2,
        border_color="red4",
    )
    self.tftpgrpexit.pack(padx=(30, 30), pady=(10, 5), side="right")

    self.bottomframe4 = ctk.CTkFrame(
        master=self.tftpuploadgroupw, fg_color="powder blue"
    )
    self.bottomframe4.pack(fill="x", pady=1)
    self.progstatuslbl = Label(
        self.bottomframe4,
        text="id:",
        font=("arial", 14, "bold"),
        bg="powder blue",
        fg="OrangeRed2",
    )
    self.progstatuslbl.pack(padx=(40, 30), pady=(5, 15), side="left")
    self.progstatus1 = ctk.CTkProgressBar(
        self.bottomframe4,
        progress_color="green4",
        border_width=1,
        border_color="dark slate gray",
        width=500,
    )
    self.progstatus1.pack(padx=(40, 30), pady=(5, 15), side="right")
    self.progstatus1.set(0)

    self.checkboxcopygrp.select()
    self.chkbxrunningcfgrp.select()

    populatemembxg(self)
