import os

ROOT_DIR = os.path.abspath(os.curdir)

tftpserver = "10.24.35.253"

sideframecolour = "light blue"
bottomframecolour = "light blue"
topframeacolour = "light blue"
topframebcolour = "light blue"

dbfile = os.path.join(ROOT_DIR, "database.db")

directorypathroot = ROOT_DIR
devicegroups = os.path.join(ROOT_DIR, "devicegroups")
pythonicon = os.path.join(ROOT_DIR, "icon.png")

devicesaveddata = os.path.join(ROOT_DIR, "devicedata/")
tftprootdir = os.path.join(ROOT_DIR, "devicedata/tftp_temp")

directorylocation = os.path.join(ROOT_DIR, "devicedata/tftp_temp/")
filesource = os.path.join(ROOT_DIR, "devicedata/tftp_temp/")
filedestination = os.path.join(ROOT_DIR, "devicedata/")
changetoDEVICEDATAdirectory = ROOT_DIR

listOfCMDs = [
    "show version",
    "show running-config",
    "show ip interface brief",
    "show ip route",
    "show interface gigabitEthernet 0/0",
    "show interface gigabitEthernet 0/1",
    "show interface gigabitEthernet 0/2",
    "show interface gigabitEthernet 0/3",
    "show interface gigabitEthernet 0/4",
    "show interface gigabitEthernet 1/0",
    "show interface gigabitEthernet 1/1",
    "show arp",
    "show flash:",
    "show vlan",
]
