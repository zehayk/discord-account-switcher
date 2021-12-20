import getpass
import os
import json
import psutil
import subprocess

from tkinter import Label, Tk, Button, Text

CURRENT_USER = getpass.getuser()

def launchDiscord():
    os.startfile(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc\\Discord")

def exitDiscord():
    os.system("taskkill /F /im discord.exe")

def newAccount(accountName):
    exitDiscord()

    while True:
        if "discord.exe" not in (i.name() for i in psutil.process_iter()):
            break

    print("Adding new account")

    file = open(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json", "r+")
    data = json.load(file)
    file.close()

    for account in data:
        if data[account] == "Local Storage":
            os.rename(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\Local Storage",
                      f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\Local Storage - {account}")
            data[account] = f"Local Storage - {account}"

            file = open(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json", "r+")
            json.dump(data, file)
            file.close()

            break

    file = open(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json", "r+")
    data = json.load(file)
    file.close()

    data[accountName] = "Local Storage"

    file = open(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json", "r+")
    json.dump(data, file)
    file.close()

    launchDiscord()
    refresh()

def switchAccount(name):
    print("Switching account to " + name)

    file = open(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json", "r+")
    data = json.load(file)
    file.close()

    if name not in data:
        print("Account not found")
        return

    for account in data:
        if data[account] == "Local Storage":
            if name == account:
                print("This account is already active")
                return
            else:
                exitDiscord()

                while True:
                    if "discord.exe" not in (i.name() for i in psutil.process_iter()):
                        break

            os.rename(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\Local Storage",
                      f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\Local Storage - {account}")
            data[account] = f"Local Storage - {account}"

            file = open(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json", "w+")
            json.dump(data, file)
            file.close()
            break

    for account in data:
        if data[account] == f"Local Storage - {name}":
            os.rename(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\Local Storage - {name}",
                      f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\Local Storage")
            data[account] = f"Local Storage"

            file = open(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json", "w+")
            json.dump(data, file)
            file.close()
            break

    launchDiscord()

def startup():
    print("Hello " + CURRENT_USER + "!")

    if not os.path.exists(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json"):
        file = open(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json", "w+")
        file.write('{}')
        file.close()
        print("Created \"accounts_list.json\"")

    file = open(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json", "r+")
    data = json.load(file)
    file.close()

    if len(data) == 0:
        accountNameWindow = Tk()
        accountNameWindow.geometry("330x150")
        accountNameWindow.configure(bg="gray")
        accountNameWindow.resizable(False, False)
        accountNameWindow.title("Discord Account Switcher")

        header_text = Label(accountNameWindow, bg="gray", fg="white", font=("Times", 15), relief="flat")
        header_text.configure(text="What is your current account name?")
        header_text.place(x=20, y=20)

        print("What is the current account name ?")
        submitButton = Button(accountNameWindow, text="submit", command=lambda: submit(nameInput())).place(x=60, y=85)

        def nameInput():
            inputText = inputtxt.get(1.0, "end-1c")
            inputtxt.delete(1.0, "end-1c")
            return inputText

        # switch_button.place(x=10, y=10)

        inputtxt = Text(accountNameWindow, height=1, width=15)
        inputtxt.place(x=60, y=60)

        def submit(accountName):
            data[accountName] = "Local Storage"

            file = open(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json", "r+")
            json.dump(data, file)
            file.close()

            accountNameWindow.destroy()
        accountNameWindow.mainloop()

def refresh():
    window.destroy()
    setupWindow()

def setupWindow():
    global window
    window = Tk()
    window.geometry("400x400")
    window.configure(bg="gray")
    window.resizable(False, False)
    window.title("Discord Account Switcher")

    header_text = Label(window, bg="gray", fg="white", font=("Times", 30, "italic"),
                        relief="flat")

    # switch_button = Button(window, text="start", command=switchAccount)

    refresh_button = Button(window, text="Refresh Window", command=lambda: refresh()).place(x=290, y=10)


    new_account_button = Button(window, text="Add new account", command=lambda: newAccount(getInput(inputtxt)))

    def getInput(inputtxt):
        inputText = inputtxt.get(1.0, "end-1c")
        inputtxt.delete(1.0, "end-1c")
        return inputText

    # switch_button.place(x=10, y=10)
    new_account_button.place(x=30, y=155)

    header_text.configure(text="Hello World")
    header_text.place(x=100, y=50)

    inputtxt = Text(window, height=1, width=15)
    inputtxt.place(x=30, y=130)

    openFile_button = Button(window, text="Open \"accounts_list.json\"", command=lambda: openAccountsFileLocation()).place(x=250, y=340)
    def openAccountsFileLocation():
        subprocess.Popen(f"explorer /select,\"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json\"")

    exit_button = Button(window, text="Exit", command=lambda: os._exit(0)).place(x=365, y=370)

    file = open(f"C:\\Users\\{CURRENT_USER}\\AppData\\Roaming\\discord\\accounts_list.json", "r+")
    data = json.load(file)
    file.close()

    Label(window, bg="gray", fg="white", font=("Times", 15), relief="flat", text="Accounts:").place(x=250, y=130)
    yCoord = 170
    for account in data:
        print(account)
        newButton = Button(window, text=account, command=lambda acc=account: switchAccount(acc))
        newButton.place(x=250, y=yCoord)
        yCoord += 30

    window.mainloop()

if __name__ == "__main__":
    startup()

    setupWindow()

