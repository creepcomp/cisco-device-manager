from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
from settings import *


def showcmdframe(self, choice, *args, **kwargs):

    if choice == "Paramiko":

        self.btncopy.configure(state="disabled")
        self.btnpaste.configure(state="disabled")

        for widgets in self.cmdframea.winfo_children():
            widgets.destroy()

        self.cmdframecontainer = Frame(self.cmdframea, background="light sky blue")
        self.cmdframecontainer.pack(fill="both", expand=TRUE, anchor="n", side=TOP)

        self.listbox = Listbox(
            self.cmdframecontainer,
            activestyle="none",
            font=("Helvetica", 11, "bold"),
            highlightthickness=0,
            selectforeground="black",
            background="light goldenrod yellow",
            selectbackground="palegreen",
            exportselection=False,
        )
        self.listbox.pack(
            side=LEFT, fill="both", expand=True, anchor="nw", padx=(15, 5), pady=(10, 5)
        )
        self.scrollbar = Scrollbar(self.cmdframecontainer)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)

        for i in listOfCMDs:
            self.listbox.insert("end", i)

        self.listbox.select_set(1)
        self.cmdvarselected.set("show running-config")
        self.statusvarcmd2.set(value=self.cmdvarselected.get())

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        def localindex_selected(event):
            selected_indices = self.listbox.curselection()
            selected_index = selected_indices[0]
            selected_value = self.listbox.get(selected_index)
            self.cmdvarselected.set(selected_value)

            self.statusvarcmd2.set(value=self.cmdvarselected.get())

        self.listbox.bind("<<ListboxSelect>>", localindex_selected)

    elif choice == "Netmiko":

        self.btncopy.configure(state="disabled")
        self.btnpaste.configure(state="disabled")

        for widgets in self.cmdframea.winfo_children():
            widgets.destroy()

        self.cmdframecontainer = Frame(self.cmdframea, background="light sky blue")
        self.cmdframecontainer.pack(fill="both", expand=TRUE, anchor="n", side=TOP)

        self.listbox = Listbox(
            self.cmdframecontainer,
            activestyle="none",
            font=("Helvetica", 11, "bold"),
            highlightthickness=0,
            selectforeground="black",
            background="light goldenrod yellow",
            selectbackground="palegreen",
            exportselection=False,
        )
        self.listbox.pack(
            side=LEFT, fill="both", expand=True, anchor="nw", padx=(15, 5), pady=(10, 5)
        )
        self.scrollbar = Scrollbar(self.cmdframecontainer)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)

        for i in listOfCMDs:
            self.listbox.insert("end", i)

        self.listbox.select_set(1)
        self.cmdvarselected.set("show running-config")
        self.statusvarcmd2.set(value=self.cmdvarselected.get())

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        def localindex_selected(event):
            selected_indices = self.listbox.curselection()
            selected_index = selected_indices[0]
            selected_value = self.listbox.get(selected_index)
            self.cmdvarselected.set(selected_value)

            self.statusvarcmd2.set(value=self.cmdvarselected.get())

        self.listbox.bind("<<ListboxSelect>>", localindex_selected)

    elif choice == "Netmiko_ch":

        self.btncopy.configure(state="disabled")
        self.btnpaste.configure(state="disabled")

        for widgets in self.cmdframea.winfo_children():
            widgets.destroy()

        self.cmdframecontainer = Frame(self.cmdframea, background="light sky blue")
        self.cmdframecontainer.pack(fill="both", expand=TRUE, anchor="n", side=TOP)

        self.listbox = Listbox(
            self.cmdframecontainer,
            activestyle="none",
            font=("Helvetica", 11, "bold"),
            highlightthickness=0,
            selectforeground="black",
            background="light goldenrod yellow",
            selectbackground="palegreen",
            exportselection=False,
        )
        self.listbox.pack(
            side=LEFT, fill="both", expand=True, anchor="nw", padx=(15, 5), pady=(10, 5)
        )
        self.scrollbar = Scrollbar(self.cmdframecontainer)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)

        for i in listOfCMDs:
            self.listbox.insert("end", i)

        self.listbox.select_set(1)
        self.cmdvarselected.set("show running-config")
        self.statusvarcmd2.set(value=self.cmdvarselected.get())

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        def localindex_selected(event):
            selected_indices = self.listbox.curselection()
            selected_index = selected_indices[0]
            selected_value = self.listbox.get(selected_index)
            self.cmdvarselected.set(selected_value)

            self.statusvarcmd2.set(value=self.cmdvarselected.get())

        self.listbox.bind("<<ListboxSelect>>", localindex_selected)

    elif choice == "Netmiko_ch_config":

        self.btncopy.configure(state="normal")
        self.btnpaste.configure(state="normal")

        for widgets in self.cmdframea.winfo_children():
            widgets.destroy()

        self.cmdframecontainer = Frame(self.cmdframea, background="light sky blue")
        self.cmdframecontainer.pack(fill="both", expand=TRUE, anchor="n", side=TOP)

        self.cmdtxtbox = scrolledtext.ScrolledText(
            self.cmdframecontainer,
            wrap=WORD,
            background="light goldenrod yellow",
            font=("Helvetica", 11, "bold"),
            height=5,
        )
        self.cmdtxtbox.pack(
            side=LEFT, fill="both", expand=True, anchor="nw", padx=(15, 5), pady=(10, 5)
        )

        def copy_select():
            global cmddata
            if self.cmdtxtbox.selection_get():
                cmddata = self.cmdtxtbox.selection_get()
                self.clipboard_clear()
                self.clipboard_append(cmddata)

        def paste_select():
            global data
            self.cmdtxtbox.insert(tk.END, self.clipboard_get())

        self.statusvarcmd2.set(value="Netmiko config multiline")

        popup = Menu(self.cmdtxtbox, tearoff=0)

        popup.add_command(label="Copy", command=lambda: copy_select())
        popup.add_command(label="Paste", command=lambda: paste_select())

        def menu_popup(event):

            try:
                popup.tk_popup(event.x_root, event.y_root, 0)
            finally:

                popup.grab_release()

        self.bind("<Button-3>", menu_popup)

    else:

        self.btncopy.configure(state="disabled")
        self.btnpaste.configure(state="disabled")

        for widgets in self.cmdframea.winfo_children():
            widgets.destroy()
