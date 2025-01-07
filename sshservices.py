from tkinter import *
from settings import *
import sqlite3
from paramiko import client, ssh_exception
from netmiko import (
    Netmiko,
    ConnectHandler,
    NetMikoTimeoutException,
    NetMikoAuthenticationException,
)
import time


def getdevicefromid(rowIDrow):

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


def runcmdparamiko(self, iam_selecteddevice):
    retid = 0
    retname = ""
    retip = ""
    retusername = ""
    retpassword = ""
    retid, retname, retip, retusername, retpassword = getdevicefromid(
        iam_selecteddevice
    )

    ssh_client = client.SSHClient()

    ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())

    self.returnedname.set(retname)

    try:
        ssh_client.connect(
            hostname=retip, port=22, username=retusername, password=retpassword
        )

        cmd = self.cmdvarselected.get()

        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        self.txtcontent.insert(
            INSERT,
            f"- - - - * - - - - * - - - - * - START ("
            + retname
            + ") - * - - - - * - - - - * - - - - "
            + "\n",
        )
        for line in stdout.readlines():
            testvar = line.strip()
            self.txtcontent.insert(INSERT, f"{testvar}" + "\n")
        self.txtcontent.insert(
            INSERT,
            "\n"
            + "- - - - * - - - - * - - - - * - - END ("
            + retname
            + ") - - * - - - - * - - - - * - - - - "
            + "\n",
        )

    except ssh_exception.NoValidConnectionsError as sshNoValidException:
        pass

    except ssh_exception.AuthenticationException as authException:
        pass

    except ssh_exception.BadAuthenticationType as authTypeException:
        pass

    except ssh_exception.SSHException as sshException:
        pass

    except Exception as unknown_error:

        self.txtcontent.insert(
            INSERT,
            f"- - - - * - - - - * - - - - * - START ("
            + retname
            + ") - * - - - - * - - - - * - - - - "
            + "\n",
        )
        self.txtcontent.insert(INSERT, "\n" + f"{unknown_error}" + "\n")
        self.txtcontent.insert(
            INSERT,
            "\n"
            + "- - - - * - - - - * - - - - * - - END ("
            + retname
            + ") - - * - - - - * - - - - * - - - - "
            + "\n",
        )

    finally:
        ssh_client.close()


def runcmdnetmiko(self, iam_selecteddevice):
    retid = 0
    retname = ""
    retip = ""
    retusername = ""
    retpassword = ""
    retid, retname, retip, retusername, retpassword = getdevicefromid(
        iam_selecteddevice
    )

    credentials = {
        "device_type": "cisco_ios",
        "host": f"{retip}",
        "username": f"{retusername}",
        "password": f"{retpassword}",
    }

    time.sleep(1)
    self.returnedname.set(retname)

    try:

        net_connect = Netmiko(**credentials)
        net_connect.find_prompt()

        sh_output = net_connect.send_command(self.cmdvarselected.get())
        net_connect.disconnect()

    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        pass

    finally:
        try:
            if net_connect:
                net_connect.disconnect()
        except:
            pass

        self.txtcontent.insert(
            INSERT,
            "- - - - * - - - * - - - - *   START  ("
            + retname
            + ")   * - - - * - - - - * - - - - "
            + "\n",
        )
        try:
            self.txtcontent.insert(INSERT, f"{sh_output}")
        except:
            self.txtcontent.insert(INSERT, f"Error connecting to device")
        self.txtcontent.insert(
            INSERT,
            "\n"
            + "- - - - * - - - * - - - - *   END  ("
            + retname
            + ")   * - - - * - - - - * - - - - "
            + "\n"
            + "\n",
        )

    self.returnedname.set(retname)


def runcmdnetmiko_ch(self, iam_selecteddevice):
    retid = 0
    retname = ""
    retip = ""
    retusername = ""
    retpassword = ""
    retid, retname, retip, retusername, retpassword = getdevicefromid(
        iam_selecteddevice
    )

    cisco_device = {
        "device_type": "cisco_ios",
        "host": retip,
        "username": retusername,
        "password": retpassword,
        "port": 22,
        "secret": retpassword,
        "verbose": True,
    }

    output = ""
    self.txtcontent.insert(
        INSERT, f"- - - - * - - - - * - START - * - - - - * - - - - " + "\n"
    )

    self.returnedname.set(retname)

    try:
        conn = ConnectHandler(**cisco_device)
        conn_prompt = conn.find_prompt()
        if ">" in conn_prompt:
            conn.enable()

        output = conn.send_command(self.cmdvarselected.get())

    except:
        pass

    finally:

        conn.disconnect()

    self.txtcontent.insert(INSERT, f"{output}")
    self.txtcontent.insert(
        INSERT, "\n" + "- - - - * - - - - * -  END  - * - - - - * - - - - " + "\n"
    )


def runcmdnetmiko_ch_config(self, iam_selecteddevice):
    retid = 0
    retname = ""
    retip = ""
    retusername = ""
    retpassword = ""
    retid, retname, retip, retusername, retpassword = getdevicefromid(
        iam_selecteddevice
    )

    cmd_list = []
    thisoutput = StringVar()
    conn_prompt = ""

    credentials = {
        "device_type": "cisco_ios",
        "host": retip,
        "username": retusername,
        "password": retpassword,
        "port": 22,
        "secret": retusername,
        "verbose": True,
    }

    self.txtcontent.insert(
        INSERT, f"- - - - * - - - - * - START - * - - - - * - - - - " + "\n"
    )

    custcmdsget = self.cmdtxtbox.get("1.0", END)

    for line in custcmdsget.split("\n"):
        pass

    cmd_list = [y for y in (x.strip() for x in custcmdsget.splitlines()) if y]

    self.returnedname.set(retname)

    try:

        net_connect = ConnectHandler(**credentials)

        conn_prompt = net_connect.find_prompt()
        if ">" in conn_prompt:
            net_connect.enable()

        thisoutput = net_connect.send_config_set(cmd_list)
        self.txtcontent.insert(INSERT, f"{thisoutput}")

    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        pass

    finally:

        wmout = StringVar()
        wmout = net_connect.send_command("write memory")
        net_connect.disconnect()

        self.txtcontent.insert(INSERT, f"{wmout}")
        self.txtcontent.insert(
            INSERT, "\n" + "- - - - * - - - - * -  END  - * - - - - * - - - - " + "\n"
        )
