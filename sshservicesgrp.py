from tkinter import *
import sqlite3
from paramiko import client
from netmiko import (
    Netmiko,
    ConnectHandler,
    NetMikoTimeoutException,
    NetMikoAuthenticationException,
)
import time
import os
from settings import *
import json


def getdevicefromidgrp(rowIDrow):

    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()

        query = f"SELECT * FROM devices WHERE id = {rowIDrow}"
        cursor.execute(query)
        record = cursor.fetchall()
        for row in record:
            retid = row[0]
            retname = row[1]
            retip = row[2]
            retusername = row[3]
            retpassword = row[4]

        return retid, retname, retip, retusername, retpassword

    except sqlite3.Error as error:
        pass


def grpselectionget(self, groupselection):

    os.chdir(devicegroups)
    groupdevicepath = os.path.join(devicegroups, groupselection)
    os.chdir(groupdevicepath)

    filepath = os.path.join(groupselection + ".json")

    filetoread = open(filepath)
    inputjsondata = json.load(filetoread)

    return inputjsondata["members"]


def runcmdparamikogrp(self, groupselection, cmdselected):

    grpmemberreturn = grpselectionget(self, groupselection)

    for i in grpmemberreturn:
        retid = 0
        retname = ""
        retip = ""
        retusername = ""
        retpassword = ""

        getdevicefromidgrp(i)

        try:
            retid, retname, retip, retusername, retpassword = getdevicefromidgrp(i)
        except TypeError:
            pass

        ssh_client = client.SSHClient()

        ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())

        try:
            ssh_client.connect(
                hostname=retip, port=22, username=retusername, password=retpassword
            )

            cmd = cmdselected
            stdin, stdout, stderr = ssh_client.exec_command(cmd)

            self.txtcontent.insert(
                INSERT,
                "- - - - * - - - * - - - - *   START  ("
                + retname
                + ")   * - - - * - - - - * - - - - "
                + "\n",
            )
            for line in stdout.readlines():
                testvar = line.strip()
                self.txtcontent.insert(INSERT, f"{testvar}" + "\n")
            self.txtcontent.insert(
                INSERT,
                "\n"
                + "- - - - * - - - * - - - - *   END  ("
                + retname
                + ")   * - - - * - - - - * - - - - "
                + "\n",
            )
        except:
            self.txtcontent.insert(
                INSERT,
                "\n"
                + "- - - - * - - - * - - - - *   FAILED TO CONNECT  ("
                + retname
                + ")   * - - - * - - - - * - - - - "
                + "\n",
            )
        finally:
            ssh_client.close()


def runcmdnetmikogrp(self, groupselection, cmdselected):
    grpmemberreturn = grpselectionget(self, groupselection)
    self.txtcontent.insert(
        INSERT,
        "- - - - * - - - * - - - - *   START  ("
        + groupselection
        + ")   * - - - * - - - - * - - - - "
        + "\n",
    )
    for i in grpmemberreturn:
        retid = 0
        retname = ""
        retip = ""
        retusername = ""
        retpassword = ""

        try:
            retid, retname, retip, retusername, retpassword = getdevicefromidgrp(i)
        except TypeError:
            pass

        credentials = {
            "device_type": "cisco_ios",
            "host": f"{retip}",
            "username": f"{retusername}",
            "password": f"{retpassword}",
        }

        time.sleep(0.3)

        try:

            net_connect = Netmiko(**credentials)
            dev_prompt = net_connect.find_prompt()

            sh_output = net_connect.send_command(cmdselected)
            net_connect.disconnect()
            self.statuslbl.set(f"Successfull: ({dev_prompt})")

        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:

            self.statuslbl.set(f"Connection Error to : ({retip})")
        finally:
            if net_connect == True:
                net_connect.disconnect()

            self.txtcontent.insert(
                INSERT,
                "- - - - * - - - * - - - - *   START  ("
                + retname
                + ")   * - - - * - - - - * - - - - "
                + "\n",
            )
            self.txtcontent.insert(INSERT, f"{sh_output}")
            self.txtcontent.insert(
                INSERT,
                "\n"
                + "- - - - * - - - * - - - - *   END  ("
                + retname
                + ")   * - - - * - - - - * - - - - "
                + "\n"
                + "\n",
            )

    self.txtcontent.insert(
        INSERT,
        "\n"
        + "- - - - * - - - * - - - - *   END  ("
        + groupselection
        + ")   * - - - * - - - - * - - - - "
        + "\n",
    )


def runcmdnetmikogrp_ch(self, groupselection, cmdselected):

    grpmemberreturn = grpselectionget(self, groupselection)
    self.txtcontent.insert(
        INSERT,
        "- - - - * - - - * - - - - *   START  ("
        + groupselection
        + ")   * - - - * - - - - * - - - - "
        + "\n",
    )
    for i in grpmemberreturn:
        retid = 0
        retname = ""
        retip = ""
        retusername = ""
        retpassword = ""

        try:
            retid, retname, retip, retusername, retpassword = getdevicefromidgrp(i)
        except TypeError:
            pass

        credentials = {
            "device_type": "cisco_ios",
            "host": f"{retip}",
            "username": f"{retusername}",
            "password": f"{retpassword}",
        }

        cisco_device = {
            "device_type": "cisco_ios",
            "host": retip,
            "username": retusername,
            "password": retpassword,
            "port": 22,
            "secret": retpassword,
            "verbose": True,
        }

        try:
            conn = ConnectHandler(**cisco_device)
            conn_prompt = conn.find_prompt()
            if ">" in conn_prompt:
                conn.enable()

            output = conn.send_command(cmdselected)

        except:
            pass

        finally:
            conn.disconnect()
            self.txtcontent.insert(
                INSERT,
                "- - - - * - - - * - - - - *   START  ("
                + retname
                + ")   * - - - * - - - - * - - - - "
                + "\n",
            )
            self.txtcontent.insert(INSERT, f"{output}")
            self.txtcontent.insert(
                INSERT,
                "\n"
                + "- - - - * - - - * - - - - *   END  ("
                + retname
                + ")   * - - - * - - - - * - - - - "
                + "\n"
                + "\n",
            )

        self.txtcontent.insert(
            INSERT,
            "\n"
            + "- - - - * - - - * - - - - *   END  ("
            + groupselection
            + ")   * - - - * - - - - * - - - - "
            + "\n",
        )


def runcmdnetmikogrp_ch_config(self, groupselection):

    grpmemberreturn = grpselectionget(self, groupselection)
    self.txtcontent.insert(
        INSERT,
        "- - - - * - - - * - - - - *   START  ("
        + groupselection
        + ")   * - - - * - - - - * - - - - "
        + "\n",
    )

    for i in grpmemberreturn:
        retid = 0
        retname = ""
        retip = ""
        retusername = ""
        retpassword = ""

        try:
            retid, retname, retip, retusername, retpassword = getdevicefromidgrp(i)
        except TypeError:
            pass

        credentials = {
            "device_type": "cisco_ios",
            "host": f"{retip}",
            "username": f"{retusername}",
            "password": f"{retpassword}",
        }

        cisco_device = {
            "device_type": "cisco_ios",
            "host": retip,
            "username": retusername,
            "password": retpassword,
            "port": 22,
            "secret": retpassword,
            "verbose": True,
        }

        cmd_list = []
        thisoutput = StringVar()
        conn_prompt = ""

        custcmdsget = self.cmdtxtbox.get("1.0", END)

        for line in custcmdsget.split("\n"):
            pass

        cmd_list = [y for y in (x.strip() for x in custcmdsget.splitlines()) if y]

        try:

            net_connect = ConnectHandler(**credentials)

            conn_prompt = net_connect.find_prompt()
            if ">" in conn_prompt:
                net_connect.enable()

            thisoutput = net_connect.send_config_set(cmd_list)
            self.txtcontent.insert(INSERT, f"{thisoutput}")

        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:

            self.txtcontent.insert(INSERT, f"{e}")

        finally:

            wmout = StringVar()
            wmout = net_connect.send_command("write memory")
            net_connect.disconnect()
            self.txtcontent.insert(INSERT, f"{wmout}")

        self.txtcontent.insert(
            INSERT, "\n" + "- - - - * - - - - * -  END  - * - - - - * - - - - " + "\n"
        )
