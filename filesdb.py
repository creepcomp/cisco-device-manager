import os
from tkinter import *


from settings import *
from datetime import datetime


def saveframeoutput(self):

    thisdevicename = ""
    saveoutputroot = ""

    if self.groupswitch_var.get() == "on":
        thisdevicename = f"{self.groupoptionselected.get()}"

        saveoutputroot = devicegroups

    else:

        thisdevicename = f"{self.returnedname.get()}"

        saveoutputroot = devicesaveddata

    devicepath = os.path.join(saveoutputroot, thisdevicename)

    if not os.path.exists(devicepath):
        os.mkdir(devicepath)

    os.chdir(os.path.join(saveoutputroot, thisdevicename))

    mydatetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S" + ".txt")

    stufftowrite = self.txtcontent.get("1.0", END)

    appenddata = open(mydatetime, "w", encoding="utf-8")
    appenddata.write(stufftowrite)
    appenddata.close()

    os.chdir(directorypathroot)
