import tkinter as tk
import tkinter.ttk as ttk
import numpy as np


class ChecklistCombobox(ttk.Combobox):

    def __init__(self, master=None, **kw):
        self.values = kw.pop("values", None)
        if self.values is None:
            self.values = []
        if not isinstance(self.values, (list, tuple, np.ndarray)):
            self.values = list(self.values)

        ttk.Combobox.__init__(self, master, values=self.values)
        self.tk.eval("ttk::combobox::ConfigureListbox %s" % (self))

        self.popdown = tk.Toplevel()
        self.popdown.withdraw()
        self.popdown._w = "%s.popdown" % (self)
        self.popdown_frame = tk.Frame()
        self.popdown_frame._w = "%s.popdown.f" % (self)
        self.listbox = tk.Listbox()
        self.listbox._w = "%s.popdown.f.l" % (self)
        self.scrollbar = tk.Scrollbar()
        self.scrollbar_repeatdelay = self.scrollbar.cget("repeatdelay")
        self.scrollbar_repeatinterval = self.scrollbar.cget("repeatinterval")
        self.scrollbar._w = "%s.popdown.f.sb" % (self)

        self.canvas_frame = tk.Frame(self.popdown_frame)
        self.canvas = tk.Canvas(self.canvas_frame)
        self.checkbutton_frame = tk.Frame(self.canvas)
        self.checkbuttons = []
        self.variables = []
        self.selection = None
        if len(self.values) > 0:
            self.create_checkbuttons()

        self.checkbutton_frame.grid_propagate(0)
        self.checkbutton_frame.columnconfigure(0, weight=1)
        self.canvas_frame.grid_propagate(0)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.canvas.grid(row=0, column=0, sticky="news")
        self.checkbutton_frame.grid(row=0, column=0, sticky="news")
        self.canvas.create_window((0, 0), window=self.checkbutton_frame, anchor="nw")
        self.canvas_frame.grid(row=0, column=0, padx=1, pady=1, sticky="news")

        self.listbox.configure(yscrollcommand="")
        self.configure(**kw)

        self.last_clicked_button = None
        self.autoscrolling = False
        self.mouse_has_entered_popdown = False
        self.afterId = None
        self.b1_motion_entered_popdown = False
        self.configure_popdown()
        self.topbutton = 0
        if len(self.cget("values")) > self.cget("height"):
            self.bottombutton = self.cget("height") - 1
        else:
            self.bottombutton = len(self.checkbuttons) - 1

        self.previous_button_kw = {}
        if self.checkbuttons:
            self.selection = 0
            for key in self.checkbuttons[self.selection].keys():
                self.previous_button_kw[key] = self.checkbuttons[self.selection].cget(
                    key
                )

            self.checkbuttons[self.selection].configure(
                bg=self.checkbutton_selected_background[self.selection],
                fg=self.checkbutton_selected_foreground[self.selection],
                selectcolor=self.checkbutton_selected_selectcolor[self.selection],
                activebackground=self.checkbutton_selected_activebackground[
                    self.selection
                ],
                activeforeground=self.checkbutton_selected_activeforeground[
                    self.selection
                ],
            )

        self.listbox.bind("<Down>", self.on_down)
        self.listbox.bind("<Up>", self.on_up)
        self.listbox.bind(
            "<Prior>", lambda event: self.scroll(event, amount=-1, units="pages")
        )
        self.listbox.bind(
            "<Next>", lambda event: self.scroll(event, amount=1, units="pages")
        )
        self.listbox.bind(
            "<Control-Home>", lambda event: self.select(self.checkbuttons[0])
        )
        self.listbox.bind(
            "<Control-End>", lambda event: self.select(self.checkbuttons[-1])
        )
        self.listbox.bind("<KeyPress-Return>", self.on_carraige_return)
        self.listbox.bind("<Motion>", self.do_nothing)
        self.listbox.bind("<KeyPress-Tab>", self.on_lb_tab)
        self.listbox.bind("<<PrevWindow>>", self.on_lb_prevwindow)
        self.listbox.bind("<MouseWheel>", self.do_nothing)

        self.bind("<MouseWheel>", self.do_nothing)
        if self.tk.eval(
            'if {[tk windowingsystem] eq "x11"} {expr {1}} else {expr {0}}'
        ):
            self.bind("<ButtonPress-4>", self.do_nothing)
            self.bind("<ButtonPress-5>", self.do_nothing)
        self.popdown.bind("<MouseWheel>", self.on_popdown_mousewheel)
        self.bind("<ButtonPress-1>", lambda event: self.popdown.focus_set())

        self.popdown_frame.bind("<Configure>", self.configure_popdown)

        self.popdown.bind("<Unmap>", self.popdown_unmap)
        self.bind("<FocusOut>", self.popdown_unmap)

        self.popdown.bind("<Motion>", self.on_motion)
        self.popdown.bind("<B1-Motion>", self.on_b1_motion)

    def __getattribute__(self, attr):

        if attr == "configure" or attr == "config":
            return self.custom_configure
        return super(ChecklistCombobox, self).__getattribute__(attr)

    def custom_configure(self, cnf=None, **kw):
        self.checkbutton_selected_background = kw.get(
            "checkbutton_selected_background",
            [self.listbox.cget("selectbackground")] * len(self.checkbuttons),
        )
        self.checkbutton_selected_foreground = kw.get(
            "checkbutton_selected_foreground",
            [self.listbox.cget("selectforeground")] * len(self.checkbuttons),
        )
        self.checkbutton_selected_selectcolor = kw.get(
            "checkbutton_selected_selectcolor", self.checkbutton_selected_background
        )
        self.checkbutton_selected_activebackground = kw.get(
            "checkbutton_selected_activebackground",
            self.checkbutton_selected_background,
        )
        self.checkbutton_selected_activeforeground = kw.get(
            "checkbutton_selected_activeforeground",
            self.checkbutton_selected_foreground,
        )

        kw["popdown_bg"] = kw.get(
            "popdown_bg", kw.get("popdown_background", self.listbox.cget("background"))
        )
        kw["popdown_background"] = kw["popdown_bg"]
        kw["popdown_highlightthickness"] = kw.get("popdown_highlightthickness", 0)
        kw["popdown_highlightbackground"] = kw.get(
            "popdown_highlightbackground", self.listbox.cget("highlightbackground")
        )
        kw["canvas_bg"] = kw.get("canvas_bg", kw["popdown_bg"])
        kw["canvas_background"] = kw["canvas_bg"]
        kw["canvas_highlightthickness"] = kw.get("canvas_highlightthickness", 0)
        kw["canvas_yscrollcommand"] = kw.get(
            "canvas_yscrollcommand", self.scrollbar.set
        )
        kw["canvas_frame_highlightthickness"] = kw.get(
            "canvas_frame_highlightthickness", 1
        )
        kw["canvas_frame_highlightbackground"] = kw.get(
            "canvas_frame_highlightbackground", kw["popdown_bg"]
        )
        kw["scrollbar_command"] = kw.get("scrollbar_command", self.canvas.yview)

        kw["checkbutton_text"] = kw.get("checkbutton_text")
        if self.values:
            kw["checkbutton_text"] = self.values

        kw["checkbutton_font"] = kw.get("checkbutton_font", self.listbox.cget("font"))
        kw["checkbutton_anchor"] = kw.get("checkbutton_anchor", "w")
        kw["checkbutton_bd"] = kw.get("checkbutton_bd", 0)
        kw["checkbutton_highlightthickness"] = kw.get(
            "checkbutton_highlightthickness", 0
        )
        kw["checkbutton_padx"] = kw.get("checkbutton_padx", 0)
        kw["checkbutton_pady"] = kw.get("checkbutton_pady", 0)
        kw["checkbutton_bg"] = kw.get(
            "checkbutton_bg", kw.get("checkbutton_background", kw["popdown_bg"])
        )
        kw["checkbutton_fg"] = kw.get(
            "checkbutton_fg",
            kw.get("checkbutton_foreground", self.listbox.cget("foreground")),
        )
        kw["checkbutton_background"] = kw["checkbutton_bg"]
        kw["checkbutton_foreground"] = kw["checkbutton_fg"]
        kw["checkbutton_variable"] = kw.get("checkbutton_variable", self.variables)
        kw["checkbutton_overrelief"] = kw.get("checkbutton_overrelief", "flat")
        kw["checkbutton_activebackground"] = kw.get(
            "checkbutton_activebackground", kw["checkbutton_bg"]
        )
        kw["checkbutton_activeforeground"] = kw.get(
            "checkbutton_activeforeground", kw["checkbutton_fg"]
        )
        kw["checkbutton_selectcolor"] = kw.get(
            "checkbutton_selectcolor", kw["checkbutton_bg"]
        )

        popdown_kw = {}
        popdown_frame_kw = {}
        scrollbar_kw = {}
        canvas_kw = {}
        canvas_frame_kw = {}
        checkbutton_frame_kw = {}
        checkbutton_kw = {}
        checkbutton_selected_kw = {}
        combobox_kw = {}
        for key, value in kw.items():
            keysplit = key.split("_")
            if keysplit[0] == "checkbutton":
                if keysplit[1] == "frame":
                    checkbutton_frame_kw["".join(keysplit[2:])] = value
                if self.checkbuttons:
                    if keysplit[1] == "selected":
                        checkbutton_selected_kw["".join(keysplit[2:])] = value
                    else:
                        checkbutton_kw["".join(keysplit[1:])] = value
            elif keysplit[0] == "popdown":
                if keysplit[1] == "frame":
                    popdown_frame_kw["".join(keysplit[2:])] = value
                else:
                    popdown_kw["".join(keysplit[1:])] = value
            elif keysplit[0] == "canvas":
                if keysplit[1] == "frame":
                    canvas_frame_kw["".join(keysplit[2:])] = value
                else:
                    canvas_kw["".join(keysplit[1:])] = value
            elif keysplit[0] == "scrollbar":
                scrollbar_kw["".join(keysplit[1:])] = value
            else:

                if key == "values":
                    self.values = value
                    self.create_checkbuttons()
                combobox_kw[key] = value

        for key, value in checkbutton_kw.items():
            if not isinstance(value, (list, tuple, np.ndarray)):
                checkbutton_kw[key] = [value] * len(self.checkbuttons)
            elif len(value) != len(self.checkbuttons):
                raise ValueError(
                    "Array-like argument for configuring Checkbuttons is length '"
                    + str(len(value))
                    + "', but expected length '"
                    + str(len(self.checkbuttons))
                    + "'"
                )
        for key, value in checkbutton_selected_kw.items():
            myvalue = value
            if not isinstance(value, (list, tuple, np.ndarray)):
                myvalue = [value] * len(self.checkbuttons)
            elif len(value) != len(self.checkbuttons):
                raise ValueError(
                    "Array-like argument for configuring Checkbuttons is length '"
                    + str(len(value))
                    + "', but expected length '"
                    + str(len(self.checkbuttons))
                    + "'"
                )
            if key == "background":
                self.checkbutton_selected_background = myvalue
            elif key == "foreground":
                self.checkbutton_selected_foreground = myvalue
            elif key == "selectcolor":
                self.checkbutton_selected_selectcolor = myvalue
            elif key == "activebackground":
                self.checkbutton_selected_activebackground = myvalue
            elif key == "activeforeground":
                self.checkbutton_selected_activeforeground = myvalue
            else:
                raise TypeError("Unrecognized keyword argument '" + str(key) + "'")

        self._configure("configure", cnf, combobox_kw)
        self.popdown.configure(**popdown_kw)
        self.popdown_frame.configure(**popdown_frame_kw)
        self.scrollbar.configure(**scrollbar_kw)
        self.canvas.configure(**canvas_kw)
        self.canvas_frame.configure(**canvas_frame_kw)
        self.checkbutton_frame.configure(**checkbutton_frame_kw)

        for i, button in enumerate(self.checkbuttons):
            my_kw = {}
            for key, value in checkbutton_kw.items():
                my_kw[key] = value[i]
            button.configure(**my_kw)

    def current(self, newindex=None):

        if newindex is not None:
            if isinstance(newindex, (list, tuple, np.ndarray)):
                for i in newindex:
                    self.checkbuttons[i].event_generate("<ButtonRelease-1>")
            else:
                self.checkbuttons[newindex].event_generate("<ButtonRelease-1>")
        else:
            retarr = self.get()
            if len(retarr) == 0:
                return -1
            elif len(retarr) == 1:
                if retarr[0] == "":
                    return -1
                else:
                    return self.cget("values").index(retarr[0])
            else:
                return [self.cget("values").index(i) for i in self.get()]

    def get(self):

        all_text = [
            b.cget("text")
            for b, v in zip(self.checkbuttons, self.variables)
            if v.get() == 1
        ]
        if len(all_text) > 1:
            return all_text
        elif len(all_text) == 1:
            return all_text[0]
        else:
            return ""

    def set(self, value):

        if isinstance(value, (list, tuple, np.ndarray)):

            check = [str(v) for v in value]
            idx = -1
            my_button = None
            for button in self.checkbuttons:
                if button.cget("text") in check:
                    button.select()
                    if check.index(button.cget("text")) > idx:
                        idx = check.index(button.cget("text"))
                        my_button = button
                else:
                    button.deselect()
            if my_button is not None and not self.popdown.winfo_ismapped():
                self.select(my_button)
                self.last_clicked_button = my_button
            return super(ChecklistCombobox, self).set(", ".join(value))
        else:
            return super(ChecklistCombobox, self).set(value)

    def select(self, button):
        if button not in self.checkbuttons:
            return
        if self.selection is not None and button == self.checkbuttons[self.selection]:
            return
        idx = self.checkbuttons.index(button)

        if self.selection is not None:
            self.checkbuttons[self.selection].configure(**self.previous_button_kw)
        self.previous_button_kw = {}
        for key in button.keys():
            self.previous_button_kw[key] = button.cget(key)

        button.configure(
            bg=self.checkbutton_selected_background[idx],
            fg=self.checkbutton_selected_foreground[idx],
            selectcolor=self.checkbutton_selected_selectcolor[idx],
            activebackground=self.checkbutton_selected_activebackground[idx],
            activeforeground=self.checkbutton_selected_activeforeground[idx],
        )
        self.selection = self.checkbuttons.index(button)

        visible_bottom = self.canvas.winfo_height() - self.checkbutton_frame.winfo_y()
        visible_top = -self.checkbutton_frame.winfo_y()
        button_height = button.winfo_height()
        button_y0 = button.winfo_y()
        button_y1 = button_y0 + button_height
        if button_y1 > visible_bottom:
            self.scroll(amount=int((button_y1 - visible_bottom) / button_height))
        elif button_y0 < visible_top:
            self.scroll(amount=-int((visible_top - button_y0) / button_height))

    def create_checkbuttons(self):

        if len(self.values) < len(self.checkbuttons):
            for button in self.checkbuttons[len(values) :]:
                self.checkbuttons.pop(button)

                button.destroy()
        else:

            for i in range(len(self.checkbuttons), len(self.values)):
                self.checkbuttons.append(tk.Checkbutton())
                self.checkbuttons[-1]._w = "%s%s" % (
                    self.checkbutton_frame,
                    self.checkbuttons[-1],
                )
                self.tk.eval("checkbutton %s" % (self.checkbuttons[-1]))
                self.variables.append(tk.IntVar())

        for i, button in enumerate(self.checkbuttons):
            button.configure(text=self.values[i])
            button.grid(row=i, column=0, sticky="news")

            for button in self.checkbuttons:
                button.bind("<ButtonRelease-1>", self.on_checkbutton_click_release)
                button.bind("<Button-1>", self.on_checkbutton_click_press)

        self.configure()

        if self.checkbuttons and self.selection is not None:
            self.previous_button_kw = {}
            for key in self.checkbuttons[self.selection].keys():
                self.previous_button_kw[key] = self.checkbuttons[self.selection].cget(
                    key
                )

            self.checkbuttons[self.selection].configure(
                bg=self.checkbutton_selected_background[self.selection],
                fg=self.checkbutton_selected_foreground[self.selection],
                selectcolor=self.checkbutton_selected_selectcolor[self.selection],
                activebackground=self.checkbutton_selected_activebackground[
                    self.selection
                ],
                activeforeground=self.checkbutton_selected_activeforeground[
                    self.selection
                ],
            )

    def scrollbar_autoscroll_down(self):
        self.scroll(amount=1)
        self.update()
        self.afterId = self.after(
            self.scrollbar_repeatinterval, self.scrollbar_autoscroll_down
        )

    def scrollbar_autoscroll_up(self):
        self.scroll(amount=-1)
        self.update()
        self.afterId = self.after(
            self.scrollbar_repeatinterval, self.scrollbar_autoscroll_up
        )

    def on_popdown_mousewheel(self, event):

        if event.num == 4:
            self.scroll(event, amount=-5)
        elif event.num == 5:
            self.scroll(event, amount=5)
        elif event.delta == 120:
            self.scroll(event, amount=-4)
        elif event.delta == -120:
            self.scroll(event, amount=4)
        return "break"

    def scroll(self, event=None, amount=1, units="units"):
        if len(self.cget("values")) > self.cget("height"):

            return self.canvas.yview_scroll(amount, units)

    def on_down(self, event=None):
        if self.selection is None:
            self.select(self.checkbuttons[self.topbutton])
        elif self.selection < len(self.checkbuttons) - 1:
            self.select(self.checkbuttons[self.selection + 1])
        return "break"

    def on_up(self, event=None):
        if self.selection is None:
            self.select(self.checkbuttons[self.bottombutton])
        elif self.selection > 0:
            self.select(self.checkbuttons[self.selection - 1])
        return "break"

    def do_nothing(self, *args, **kwargs):
        return "break"

    def on_lb_tab(self, event):
        self.on_checkbutton_click_release(event)
        self.tk.eval(
            'set newFocus [tk_focusNext %s] \n\
        if {$newFocus ne ""} {\n\
        ttk::combobox::Unpost %s \n\
        update \n\
        ttk::traverseTo $newFocus \n\
        }'
            % (self, self)
        )
        return "break"

    def on_lb_prevwindow(self, event):
        self.on_checkbutton_click_release(event)
        self.tk.eval(
            'set newFocus [tk_focusPrev %s] \n\
        if {$newFocus ne ""} {\n\
        ttk::combobox::Unpost %s \n\
        update \n\
        ttk::traverseTo $newFocus \n\
        }'
            % (self, self)
        )
        return "break"

    def on_carraige_return(self, event):
        if self.selection is not None:
            self.checkbuttons[self.selection].event_generate("<ButtonRelease-1>")
        return "break"

    def on_motion(self, event):
        if event.widget in [str(b) for b in self.checkbuttons]:
            for button in self.checkbuttons:
                y0 = button.winfo_rooty()
                y1 = y0 + button.winfo_height()
                if y0 < event.y_root and event.y_root < y1:
                    self.select(button)

    def on_b1_motion(self, event):
        y = event.y_root - self.popdown.winfo_rooty()
        x = event.x_root - self.popdown.winfo_rootx()
        if not self.b1_motion_entered_popdown:
            if (
                y < self.popdown.winfo_height()
                and y >= 0
                and x < self.popdown.winfo_width()
                and x >= 0
            ):
                self.b1_motion_entered_popdown = True
        if self.b1_motion_entered_popdown:
            if y >= self.popdown.winfo_height() and self.scrollbar.get()[1] != 1.0:
                if not self.autoscrolling:
                    self.autoscrolling = True
                    self.autoscan("down")
            elif y < 0 and self.scrollbar.get()[0] != 0.0:
                if not self.autoscrolling:
                    self.autoscrolling = True
                    self.autoscan("up")
            else:
                self.cancel_autoscan()
                self.on_motion(event)

    def autoscan(self, direction):
        if not self.autoscrolling:
            return
        cy0 = self.canvas.winfo_rooty()
        if direction == "down":
            if self.scrollbar.get()[1] == 1.0:
                self.cancel_autoscan()
                return

            cy1 = cy0 + self.canvas.winfo_height()
            for i, button in enumerate(self.checkbuttons):
                by1 = button.winfo_rooty() + button.winfo_height()
                if by1 - cy1 == 0 and i < len(self.checkbuttons) - 1:
                    self.select(self.checkbuttons[i + 1])
        elif direction == "up":
            if self.scrollbar.get()[0] == 0.0:
                self.cancel_autoscan()
                return
            for i, button in enumerate(self.checkbuttons):
                by0 = button.winfo_rooty()
                if by0 - cy0 == 0 and i > 0:
                    self.select(self.checkbuttons[i - 1])
        else:
            raise ValueError("'direction' must be either 'up' or 'down'")
        self.afterId = self.after(
            50, lambda direction=direction: self.autoscan(direction)
        )

    def cancel_autoscan(self, event=None):
        self.autoscrolling = False
        if self.afterId is not None:
            self.afterId = self.after_cancel(self.afterId)

    def on_checkbutton_click_press(self, event):
        buttons = [b._w for b in self.checkbuttons]
        button = self.checkbuttons[buttons.index(event.widget)]
        self.select(button)

    def on_checkbutton_click_release(self, event):
        self.cancel_autoscan()
        button = self.checkbuttons[self.selection]
        variable = self.variables[self.selection]
        if variable.get() == 0:
            button.select()
            self.last_clicked_button = button
            self.event_generate("<<ComboboxSelected>>", when="mark")
        else:
            button.deselect()
        all_text = [
            b.cget("text")
            for b, v in zip(self.checkbuttons, self.variables)
            if v.get() == 1
        ]
        self.set(all_text)
        self.selection_range(0, "end")
        self.icursor("end")
        return "break"

    def configure_popdown(self, event=None):

        self.canvas.update()
        self.canvas_frame.update()
        self.checkbutton_frame.update()
        borders = np.array(
            [
                self.popdown.cget("highlightthickness"),
                self.checkbutton_frame.cget("highlightthickness"),
                self.canvas_frame.cget("highlightthickness"),
            ],
            dtype=int,
        )
        visible_height = 0
        total_height = 0
        for i, button in enumerate(self.checkbuttons):
            button.update()
            bheight = button.winfo_height()
            if i < self.cget("height"):
                visible_height += bheight
            total_height += bheight

        w = self.canvas.winfo_width()
        self.canvas.config(height=visible_height + 2 * borders[1])
        self.checkbutton_frame.config(height=total_height + 2 * borders[1], width=w)
        self.canvas_frame.config(height=visible_height + 2 * np.sum(borders[1:3]))
        if len(self.cget("values")) > self.cget("height"):
            self.canvas.config(scrollregion=(0, 0, w, total_height))
            self.canvas.config(
                yscrollincrement=total_height / float(len(self.checkbuttons))
            )
            self.canvas_frame.grid_configure(padx=(1, 0))
            if self.get() == "":
                self.last_clicked_button = self.checkbuttons[0]
                self.canvas.yview_moveto(0.0)
            self.b1_motion_entered_popdown = False
        else:
            self.canvas_frame.grid_configure(padx=1)
        self.checkbutton_frame.update()
        self.popdown_frame.update()
        self.popdown.update()

    def popdown_unmap(self, event):
        if event.widget != self.popdown._w:
            return
        self.autoscrolling = False
        self.mouse_has_entered_popdown = False

    def scroll_to_last_clicked_button(self, event):

        if event.widget != self.popdown_frame._w:
            return
        if not self.scrollbar.winfo_ismapped():
            return
        button = self.last_clicked_button

        visible_height = self.canvas.winfo_height()
        total_height = self.checkbutton_frame.winfo_height()
        by0 = button.winfo_y()
        by1 = by0 + button.winfo_height()
        y0 = self.canvas.winfo_rooty()
        y1 = y0 + visible_height
        topbutton = None
        bottombutton = None
        for b in self.checkbuttons:
            if b.winfo_rooty() - y0 == 0:
                topbutton = b
            if b.winfo_rooty() + b.winfo_height() == y1:
                bottombutton = b
        if topbutton is None or bottombutton is None:
            raise Exception(
                "Something went wrong when trying to figure out where the top and bottom buttons in the view are. Perhaps this is a problem with border thicknesses?"
            )

        dt = self.checkbuttons.index(button) - self.checkbuttons.index(topbutton)
        db = self.checkbuttons.index(bottombutton) - self.checkbuttons.index(button)
        if dt >= 0 and db < 0:
            if db >= -2:

                self.canvas.yview_moveto((by1 - visible_height) / total_height)
            else:
                self.canvas.yview_moveto((by1 - 0.5 * visible_height) / total_height)
        elif dt < 0 and db >= 0:
            if dt >= -2:

                self.canvas.yview_moveto(by0 / total_height)
            else:
                self.canvas.yview_moveto((by1 - 0.5 * visible_height) / total_height)

        self.select(button)


if __name__ == "__main__":
    root = tk.Tk()
    values = (
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
    )
    cb_orig = ttk.Combobox(root, state="readonly", width=100, height=6, values=values)
    cb_orig.grid(row=0, column=0)

    cb = ChecklistCombobox(
        root, state="readonly", checkbutton_height=1, width=100, height=6, values=values
    )
    cb.grid(row=0, column=1)

    def set_custom_look():

        cb.checkbuttons[2].config(highlightthickness=5)

    b = tk.Button(root, text="Set", command=set_custom_look)
    b.grid(row=1, column=0)

    root.mainloop()
