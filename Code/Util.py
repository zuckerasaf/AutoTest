# -*- coding: utf-8 -*-

"""
Created on Sun Jan 16 13:43:46 2022

@author: AZucker
"""

#from datetime import datetime
import datetime
import subprocess
import pyautogui
pyautogui.FAILSAFE = False
import os
import platform
import time
import pygetwindow as gw
import sys
import shutil
import random
import Global_Setting_Var
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import _tkinter
import threading
import webbrowser
import Creattest
import runTest
from DataWindow import *
from docx import Document
from docx.shared import Cm, Inches
# from PIL import Image

def replace_line(file_name, line_number, new_string):
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()

        if 1 <= line_number <= len(lines):
            lines[line_number - 1] = new_string + "\n"

            with open(file_name, "w") as file:
                file.writelines(lines)

            print(f"Line {line_number} replaced successfully.")
        else:
            print(f"Invalid line number: {line_number}")

    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
    except IOError as e:
        print(f"An error occurred while reading or writing the file: {e}")


def runMainAutoScript():

    scriptPath = Global_Setting_Var.scriptPath#"D:\ElbitProjects\ATH\GIT\AutoTest\Code\MainAutoTest.py"
    close_Notefic()
    try:
        subprocess.run(['python',scriptPath],check=True)
    except:
        messagebox.showinfo('Auto Test', 'could not run the auto test app')




def copyRSN():

    filepath = Global_Setting_Var.RSN
    apppath = r'C:\Windows\System32\notepad.exe'
    p = subprocess.Popen([apppath, filepath])
    time.sleep(0.1)


    pyautogui.keyDown('ctrlright')  # press the left arrow key
    pyautogui.press('a')  # press the left arrow key
    pyautogui.keyUp('ctrlright')  # press the left arrow key
    pyautogui.keyUp('a')  # press the left arrow key
    pyautogui.keyDown('ctrlright')  # press the left arrow key
    pyautogui.press('c')  # press the left arrow key
    pyautogui.keyUp('ctrlright')  # press the left arrow key
    pyautogui.keyUp('c')  # press the left arrow key

    p.terminate()


    #webbrowser.get("C://Users//ath//AppData//Local//Google//Chrome//Application//chrome.exe %s").open('http://192.168.18.153:8000/webios')

# input: none
# what does it do: return date and time in convenient way
# output: none
def Timefordispaly():
    now = datetime.datetime.now()
    str_now = now.strftime(" %B %d. %Y %H:%M:%S")
    return (str_now)


# input: "pointer" to open TXT file
# what does it do: write time + date + the machine name that run the script in the income TXT file
# output: none
def general_Data(filenamedest):
    now = datetime.datetime.now()
    str_now = now.strftime(" %B %d. %Y   %H:%M:%S")
    filenamedest.writelines('general data:  \n')
    filenamedest.writelines('this DOC was created in : \t ' + str_now + '\n')
    filenamedest.writelines('this DOC was created from : \t' + platform.uname().node + '\n \n')


def TranslateUserDifftoValue(num):

    if num == 0:
        difference = Global_Setting_Var.diffrence_static
    elif num == 1:
        difference = Global_Setting_Var.diffrence_dynamic
    elif num == 2:
        difference = Global_Setting_Var.diffrence_extreme
    else:
        difference = 0
    return difference


def ReteurnDiffrencevalue(filename):

    file1 = open(filename, "r") 
    file1Line = file1.readlines()
    Diff_From_ATP = file1Line[2].split(" ")[6]
    if Diff_From_ATP == "static":
        difference = Global_Setting_Var.diffrence_static
    elif Diff_From_ATP == "dynamic":
        difference = Global_Setting_Var.diffrence_dynamic
    elif Diff_From_ATP == "extreme":
        difference = Global_Setting_Var.diffrence_extreme
    else:
        difference = 27000
    file1.close()
    return difference
# input:
#   versionFile = string - path for the  version declaration txt file according to setting file 
#   filenamedest = "pointer" to open TXT file  
#   docType = string - define if the destination file is going to be ATP, ATP comment or ATR  
#   testName = string - the current test name   
# what does it do:
#   Step 1 write general  data in destination file 
#   Step 2 copy version data to  destination file + add data for version modification 
#   Step 3 create header for the process table according  to the type of the DOC 
# output: none
def CreateDocHeader(versionFile, filenamedest, docType, testName, testSummary, version_mnot=None):
    # step 1 
    filenamedest.writelines('************** ' + testName + ' ' + docType + ' **************\n')
    filenamedest.writelines(testSummary + '\n')
    curDiffNum = Global_Setting_Var.diffrence
    if curDiffNum == Global_Setting_Var.diffrence_static:
        curDiffStr = "static - nothing move"
    elif curDiffNum == Global_Setting_Var.diffrence_dynamic:
        curDiffStr = "dynamic - small amount of moving object"
    elif curDiffNum == Global_Setting_Var.diffrence_extreme:
        curDiffStr = "extreme - large amount of moving object"
    else:
        curDiffStr =""

    filenamedest.writelines('Test difference filter was define as: ' + curDiffStr + ' \n\n')
    general_Data(filenamedest)

    # step 2     
    file_Source = open(Global_Setting_Var.versionFile, "r")
    version_m_time = os.path.getmtime(Global_Setting_Var.versionFile)
    version_m_time_str = datetime.datetime.fromtimestamp(version_m_time).strftime(" %B %d. %Y   %H:%M:%S")

    for line in file_Source:
        filenamedest.writelines(line)
    file_Source.close()
    filenamedest.writelines('\n->>> Versions data was update on: ' + version_m_time_str + ' \n')
    # Step 3
    if docType == "ATP":
        filenamedest.writelines('\n \n' + testName + ' ATP procedure :\n')
        filenamedest.writelines('Step number \t Step name \t  Step expected result \t  image path \n')
    elif docType == "comment":
        filenamedest.writelines('\n \n' + testName + ' ATP comment procedure :\n')
        filenamedest.writelines('Step number \t  Step comment \t image path \n')
    else:
        filenamedest.writelines('\n \n' + testName + ' ATR procedure :\n')
        filenamedest.writelines(
            'Step number \t Step name \t  Step expected result \t  image path \t diffrence from ATP \t status \n')


# input: string
# what does it do: check that the test name contain  only letters \ numbers \ spaces
# output: string
def check_space(test_name):
    STR1 = "this name of test need to be without special characters   - choose another"
    newTestName = test_name.replace(" ", "_")
    print(newTestName)
    LenN = len(newTestName)
    for i in range(len(newTestName)):
        Let = ord(newTestName[i])
        if Let < 32:
            pyautogui.alert(STR1, title=test_name)
            sys.exit()
        if Let > 32 and Let < 48:
            pyautogui.alert(STR1, title=test_name)
            sys.exit()
        #if len(line) > 57 and len(line) < 65:
        if Let > 57 and Let < 65:
            pyautogui.alert(STR1, title=test_name)
            sys.exit()
        #if len(line) > 90 and 95 < len(line):
        if Let > 90 and Let < 95:
            pyautogui.alert(STR1, title=test_name)
            sys.exit()
        #if len(line) == 96:
        if Let == 96:
            pyautogui.alert(STR1, title=test_name)
            sys.exit()
        #if len(line) > 122:
        if Let > 122:
            pyautogui.alert(STR1, title=test_name)
            sys.exit()
    return (newTestName)


# input:
#   ParentDirResu = string - path for the Tests directory
#   testName = string - the current test name
#   Type =   int : 1,2  
# what does it do: if string(test name) exsits and type =1  popup message, type = 2 will delete the directey (for the result)
# output: none
def check_name_exists(ParentDir, test_name, type):
    if os.path.isdir(ParentDir + test_name + "/"):
        if type == 1:
            messagebox.showinfo('Auto Test','this name of test is exists  - choose another')
            sys.exit()
        if type == 2:
            shutil.rmtree(ParentDir + test_name + "/")
            #print(ParentDir + test_name + "/ has been deleted")


# input:
#   ParentDirResu = string - path for the Tests directory 
#   testName = string - the current test name   
# what does it do: if true  popup message
# output: none
def check_name_not_exists(ParentDir, test_name):
    if not (os.path.isdir(ParentDir + test_name + "/")):
        mesg = "the " + test_name + " is not in the test directory, check the test list file"
        messagebox.showinfo('Auto Test', mesg)
        sys.exit()


def Service_Remote_API():
    # Create Test
    print("WEB_API:Create Test")
    Global_Setting_Var.Web_user_test_name = "Boris20002"
    Global_Setting_Var.Web_user_test_summary = "auto_test"
    Global_Setting_Var.Web_diff = 5000
    Global_Setting_Var.diffrence = Global_Setting_Var.Web_diff
    # Creattest.main_c()
    time.sleep(0)

    # Create Step
    print("WEB_API:Create Step")
    time.sleep(10)
    Global_Setting_Var.Web_stepProcess = "Step_1"
    Global_Setting_Var.Web_stepResult = "Step_1_result"
    Global_Setting_Var.Web_stepComment = "Step_1_Comment"
    Global_Setting_Var.Web_Critic = "Normal"
    pyautogui.press('f6')

    # Stop Test
    print("WEB_API:Exit")
    time.sleep(10)
    pyautogui.press('esc')

# input:
#   text = string - text to be written in the window   
# what does it do:create and display TXT (status window) file with the income "text"  inside
#               use parameters from setting file in order to display the window correctly   
# output: none
def Open_Notefic(text):
    Global_Setting_Var.stop_flag = False
    notifi_window = Tk()
    notifi_window.title("AutoTestNotification")
    notifi_window.geometry("1000x30+2+2")
    notifi_window.option_add('*Font', '19')
    notifi_window.configure(background='light green')
    notifi_window.attributes("-topmost", True)
    notifi_window.lift()
    notifi_label = Label(notifi_window, text=text, bg="light green")
    notifi_label.pack()
    notifi_window.protocol("WM_DELETE_WINDOW", killProcess)
    notifi_window.mainloop()



def killProcess():
    pass
    Global_Setting_Var.stop_flag = True
    #pyautogui.press('esc')
    sys.exit()


# input: none
# what does it do: "find" the status window and close it
# output: none
def close_Notefic():
   if Global_Setting_Var.stop_flag == False:
       Notif_win1 = gw.getWindowsWithTitle('AutoTestNotification')[0]
       time.sleep(2)
       Notif_win1.close()



# input: none
# what does it do: go to desktop by simulated the WIN+D
# output: none
def alt_Tab():
    pyautogui.keyDown('altleft')  # press the left arrow key
    pyautogui.press('tab')  # press the left arrow key
    pyautogui.keyUp('altleft')  # press the left arrow key
    pyautogui.keyUp('tab')  # press the left arrow key



# input: none
# what does it do: go to desktop by simulated the WIN+D
# output: none
def go_2desktop():
    pyautogui.keyDown('winleft')  # press the left arrow key
    pyautogui.press('d')  # press the left arrow key
    pyautogui.keyUp('winleft')  # press the left arrow key
    pyautogui.keyUp('d')  # press the left arrow key


def _Open_analasys_update(text, num):
    T = num*Global_Setting_Var.progressBar_Timing
    proges_window = Tk()
    proges_window.title("analasys update")
    proges_window.geometry("500x100+100+100")
    proges_window.option_add('*Font', '19')
    proges_window.configure(background='light green')
    proges_window.attributes("-topmost", True)
    proges_window_label = Label(proges_window, text=text, bg="light green")
    proges_window_label.pack()
    p = ttk.Progressbar(proges_window,orient=HORIZONTAL,length=300,mode="determinate",maximum = T, value=0)
    p.pack()

    proges_window.update()
    p['value'] = 0
    proges_window.update()
 
    while p['value'] < T:
        p['value'] += 10
        # Keep updating the master object to redraw the progress bar
        proges_window.update()
        time.sleep(0.1)
    proges_window.mainloop()

def Open_analasys_update(text, num):
    try:
        _Open_analasys_update(text, num)
    except _tkinter.TclError:
        pass
# input: none
# what does it do: "find" the status window and close it
# output: none
def close_analasys_update():
   
    Notif_win1 = gw.getWindowsWithTitle('analasys update')[0]
    Notif_win1.close()


# input:
#   FP = string - filename(path for the test name)
#   TLX = integer - top left x value of the snapping image
#   TLY = integer - top left Y value of the snapping image
#   BRX = integer - bottom right  x value of the snapping image
#   TLX = integer - bottom right y value of the snapping image 
#   FNIN = integer - number of picture in the test  
# what does it do: save the snapshot picture in the proper directory
# output: none
def take_snapshot(FP, TLX, TLY, BRX, BRY, FNIN):
    pyautogui.moveTo(10, 10, 0.1)  # move the mouse
    full_file_name_image = FP + "_step_" + str(FNIN) + "P.jpg"
    my_screen_shot = pyautogui.screenshot(region=(TLX, TLY, BRX, BRY))
    my_screen_shot.save(full_file_name_image)


# input:
#   ip_address = string - the IP for the remote desktop connection
#   window_location = 2 integer - the position of the top left window
#   window_size = 2 integer - the size of the remote connection
# what does it do: open remote desktop onnection
# output: none

def open_remote_desktop(ip_address, window_location=(100, 100), window_size=(600, 400)):
 # Open the Start menu
    pyautogui.hotkey('winleft')

    # Type "Remote Desktop Connection" and press Enter
    pyautogui.write('Remote Desktop Connection')
    pyautogui.press('enter')

    # Wait for the Remote Desktop Connection window to open
    time.sleep(5)

    # Type the IP address and press Enter
    pyautogui.write(ip_address)
    pyautogui.press('enter')

    # Wait for the remote desktop connection to establish
    time.sleep(5)

    # Get the Remote Desktop Connection window
    remote_desktop_window = gw.getWindowsWithTitle('Remote Desktop Connection')[0]

    # Move and resize the window to not be in full mode
    remote_desktop_window.moveTo(window_location[0], window_location[1])
    remote_desktop_window.resizeTo(window_size[0], window_size[1])

    time.sleep(2)
    pyautogui.write('407Nat')
    pyautogui.press('enter')


# input:
#   FP = string - filename(path for the test name)
#   TLX = integer - top left x value of the snapping image
#   TLY = integer - top left Y value of the snapping image
#   BRX = integer - bottom right  x value of the snapping image
#   TLX = integer - bottom right y value of the snapping image 
#   FNIN = integer - number of picture in the test  
# what does it do: save the snapshot picture in the proper directory
# output: none
def CreateRandTestName(filename):
    TimeNow = ""
    TimeNow = datetime.datetime.now()
    testNameRand = "AutoTest_" + TimeNow.strftime("%H_%M_%S")
    TempData = open(filename, "+w")
    TempData.writelines(testNameRand)
    TempData.close()
    return (testNameRand)

def DBG(fileNameLog, ATRLog, fileNameATR):
    Sourcetime = 0.0
    AutoRunTime = 0.0
    numberofMouseup_source = 0
    numberofmousedown_source = 0
    keypress_source = 0
    numberofMouseup_AutoRun = 0
    numberofmousedown_AutoRun = 0
    keypress_AutoRun = 0

    ATPLog = open(fileNameLog, "r")
    ATPLines = ATPLog.readlines()
    index = 0
    number_of_line_in_Doc = len(ATPLines)  # the amount of line in the test log
    if number_of_line_in_Doc > 1:
        val = ATPLines[number_of_line_in_Doc - 2].split(' ')[0]
        # check where is the last time value in the file
        if  val[0].isdigit():
            i = 2
        else:
            i = 3
        Sourcetime = float(ATPLines[number_of_line_in_Doc - i].split(' ')[0])
        while index < number_of_line_in_Doc - 1:
            # skip all the lines that describe the step name - they are start with s or n and not a number
            if ATPLines[index][0] == "n" or ATPLines[index][0] == "s":
                index = index + 1
            #print(str(index) + ATPLines[index][0])
            else:
                if ATPLines[index].split(' ')[1] == 'mouse':
                    if ATPLines[index].split(' ')[2] == 'up':
                        numberofMouseup_source = numberofMouseup_source + 1
                    else:
                        numberofmousedown_source = numberofmousedown_source + 1
                elif ATPLines[index].split(' ')[1] == 'keyboard':
                    if ATPLines[index].split(' ')[4] != 'Key.ctrl_l':
                        keypress_source = keypress_source + 1
                # if ATPLines[index].split(' ')[0] == 'scrolled': TBD
                index = index + 1
    else:
        numberofMouseup_source = 0
        numberofmousedown_source = 0
        keypress_source = 0

    ATRLog = open(ATRLog, "r")
    ATRLines = ATRLog.readlines()
    index = 0
    number_of_line_in_Doc = len(ATRLines)  # the amount of line in the test log
    if number_of_line_in_Doc > 1:
        val = ATRLines[number_of_line_in_Doc - 2].split(' ')[0]
        # check where is the last time value in the file
        if  val[0].isdigit():
            i = 2
        else:
            i = 3
        AutoRunTime = float(ATRLines[number_of_line_in_Doc - i].split(' ')[0])
        while index < number_of_line_in_Doc - 1:
            if ATRLines[index].split(' ')[1] == 'mouse':
                if ATRLines[index].split(' ')[2] == 'up':
                    numberofMouseup_AutoRun = numberofMouseup_AutoRun + 1
                else:
                    numberofmousedown_AutoRun = numberofmousedown_AutoRun + 1
            elif ATRLines[index].split(' ')[1] == 'keyboard':
                if ATRLines[index].split(' ')[4] != 'Key.ctrl_l':
                    keypress_AutoRun = keypress_AutoRun + 1
            # if ATRLines[index].split(' ')[0] == 'scrolled': TBD
            index = index + 1
    else :
        numberofMouseup_AutoRun=0
        numberofmousedown_AutoRun=0
        keypress_AutoRun=0

    ATPLog.close()
    ATRLog.close()

    ATRDoc = open(fileNameATR, "a")
    ATRDoc.writelines("\n auto test data analyses \n")  # update
    ATRDoc.writelines("Test origin \n")  # update
    ATRDoc.writelines("Duration: \t" + str(Sourcetime) + " \tMouse up event: \t" + str(
        numberofMouseup_source) + "\t Mouse down event: \t" + str(
        numberofmousedown_source) + "\t keyboard event: \t" + str(
        keypress_source) + "\n")
    ATRDoc.writelines("Auto Test \n")  # update
    ATRDoc.writelines("Duration: \t" + str(AutoRunTime) + " \tMouse up event: \t" + str(
        numberofMouseup_AutoRun) + "\t Mouse down event: \t" + str(
        numberofmousedown_AutoRun) + "\t keyboard event: \t" + str(
        keypress_AutoRun) + "\n")  # update general result file

    ATRDoc.close()

def main():
    print("Runing Util.py directly")

if __name__ == "__main__":
    main()
