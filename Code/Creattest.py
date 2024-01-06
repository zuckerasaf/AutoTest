# -*- coding: utf-8 -*-

"""

Created on Sun Jan 16 13:43:46 2022



@author: AZucker

"""
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key
import os
import time
import MainAutoTest
import DataWindow
from Global_Setting_Var import *
from ChromeIssue import *
import ChromeIssue
import Listener
import threading
import pyautogui
import time
import PIL.Image
import PIL.ImageChops
import os
import ctypes
from datetime import datetime
import datetime
from Util import *
import Util
import threading
from selenium import webdriver
import subprocess

############# local function for this script   #########

# input:
#   x = integer - mouse X location  
#   y = integer - mouse Y location   
#   button = string - type of button  
#   press = bool - press= true , release = false   
# what does it do: write the "TestLog" the mouse location + button type + if press or release with running time
# output: none
def mouse_click(x, y, button, pressed):
    if Global_Setting_Var.toRec == 1:
        Listener.Listener_mouse_click(x, y, button, pressed, Global_Setting_Var.start_time, TestLog)


# input:
#   x = integer - mouse X location  
#   y = integer - mouse Y location   
#   dx = integer - number of click in scroll 
#   dy = integer - scroll direction 1 = up , -1 = down  with running time
# what does it do: write the "TestLog" the mouse scroll operation
# output: none
def mouse_scroll(x, y, dx, dy):

    if Global_Setting_Var.toRec == 1:
        Listener.Listener_mouse_scroll(x, y, dx, dy, Global_Setting_Var.start_time, TestLog)


# input: key = string - keyboard mouse X operation
# what does it do:
#   Step 1 in case Left ctrl was press :
#      create snapshot 
#      write the "TestLog" the left ctrl click with running time#
#      stop the mouse location recording 
#      open user form for fulfill the step data
#      update the running time - subtracted the time while the user form was open from the running time  
#      continue running the time

# Step 2 in case ESC was press - close the running threads, close the open files and remove the status window and go
# to desktop Step 3 in all other keyboard press  - write the "TestLog" the keyboard click with running time output: none
def keyboard_press(key):
    global fileNameImage_number

    # step 1
    if key == Key.f6 or key == Key.ctrl_l :

        print('Start Step ...')
        a = format(key)
        Listener.Listener_keyboard_press(a, Global_Setting_Var.start_time, TestLog)
        # total_time = round((time.time() - Global_Setting_Var.start_time), 2)
        # TestLog.writelines(str(total_time) + ' keyboard pressed with {0} \n'.format(key))
        StepNameImage = fileNameImage

        Util.take_snapshot(StepNameImage, Global_Setting_Var.TopLeft_X, Global_Setting_Var.TopLeft_Y,
                          Global_Setting_Var.ButtomRight_X, Global_Setting_Var.ButtomRight_Y, fileNameImage_number)

        time.sleep(0.1)  # wait for the snppoint image to end before continue
        Global_Setting_Var.toRec = 0
        timestartgui = time.time()
        if Global_Setting_Var.Web_GUI==False:
            stepProcess, stepResult, stepComment ,Critic= DataWindow.getinput(TestLog, ATPfile, CommentFile, fileNameImage, test_name, fileNameImage_number)
        else:
            WEB_Income_data = "D:\ATH-AutoTestingSystem\AutoTestingSystem_TempData\Income_data.ini"
            WEB_Step_data = "D:\ATH-AutoTestingSystem\AutoTestingSystem_TempData\Step_data.ini"
            Util.replace_line(WEB_Income_data, 5, "CreateStep   		=1")
            CreateStep = "1"
            while CreateStep == "1":
                time.sleep(1)
                with open(WEB_Income_data, "r") as ID:  # open the Income data for decide what to do
                    Lines = ID.readlines()
                    CreateStep = Lines[4].split("=")[-1][:-1]
                    #ChromeIssue.OpenSite("http://127.0.0.1:5000/docs")
                    print("here we should deal with the step data")

            if CreateStep == "0":
                with open(WEB_Step_data, "r") as SD:  # open the Income data for decide what to do
                    Lines = SD.readlines()
                    stepProcess = Lines[1].split("=")[-1][:-1]
                    stepResult = Lines[2].split("=")[-1][:-1]
                    stepComment = Lines[3].split("=")[-1][:-1]
                    Critic = Lines[4].split("=")[-1][:-1]
                    fileNameImagenum = fileNameImage + "_step_" + str(fileNameImage_number)
                    DataWindow.UpdateATP(ATPfile, stepProcess, stepResult, fileNameImage_number, fileNameImagenum)



        DataWindow.UpdateLog(TestLog, Critic, stepProcess)
        time.sleep(0.5)  # wait for the user form to close before continue
        timeoutofgui = time.time()
        timeingui = timeoutofgui - timestartgui
        Global_Setting_Var.start_time = Global_Setting_Var.start_time + timeingui
        fileNameImage_number = fileNameImage_number + 1
        Global_Setting_Var.toRec = 1

    # remote desktop to CGF 1
    elif key == Key.f7 :
        a = format(key)
        Listener.Listener_keyboard_press(a, Global_Setting_Var.start_time, TestLog)
        open_remote_desktop(Global_Setting_Var.F7_IP, Global_Setting_Var.Remote_window_location, Global_Setting_Var.Remote_window_size)

    # remote desktop to TC
    elif key == Key.f8:
        a = format(key)
        Listener.Listener_keyboard_press(a, Global_Setting_Var.start_time, TestLog)
        open_remote_desktop(Global_Setting_Var.F8_IP, Global_Setting_Var.Remote_window_location,
                            Global_Setting_Var.Remote_window_size)
    # remote desktop to Own1
    elif key == Key.f9:
        a = format(key)
        Listener.Listener_keyboard_press(a, Global_Setting_Var.start_time, TestLog)
        open_remote_desktop(Global_Setting_Var.F9_IP, Global_Setting_Var.Remote_window_location,
                            Global_Setting_Var.Remote_window_size)

    # simulate alt tab function
    elif key == Key.f2 or Key == Key.ctrl_r:
        a = format(key)
        Listener.Listener_keyboard_press(a, Global_Setting_Var.start_time, TestLog)
        alt_Tab()


    # step 2   
    elif key == Key.esc:
        Global_Setting_Var.Testtime = time.time() - Global_Setting_Var.start_time
        Global_Setting_Var.terminate = 1
        TestLog.writelines("close the file")
        M_listener.stop()
        K_listener.stop()
        TestLog.close()
        ATPfile.close()
        CommentFile.close()
        Util.close_Notefic()
        go_2desktop()
        if Global_Setting_Var.Web_GUI == False:
            runMainAutoScript()

        # return False
    # step3 
    else:
        if Global_Setting_Var.toRec == 1:
            a = format(key)
            Listener.Listener_keyboard_press(a, Global_Setting_Var.start_time, TestLog)


def terminateTheprocess():
    MainAutoTest.main()



############# the script code start here  #########
def main_c():
    global TestLog
    global ATPfile
    global CommentFile
    global test_name
    global fileNameImage
    global fileNameImage_number
    global K_listener
    global M_listener

    pyautogui.FAILSAFE = False

    if Global_Setting_Var.Web_GUI == False:
        user_test_name, user_test_summary, diff = DataWindow.gettestinput()  # gets test name and summary from user
        Global_Setting_Var.stop_flag = 0
        #terminte the process befor we start
        if user_test_name =="terminate":
            terminateTheprocess()
    else:
        create_test_data = "D:\ATH-AutoTestingSystem\AutoTestingSystem_TempData\create_test.ini"
        CTD = open(create_test_data, "r")  # open the test file that is going to be executed
        Lines = CTD.readlines()
        user_test_name = Lines[5].split("=")[-1][:-1]
        user_test_summary = Lines[7].split("=")[-1][:-1]
        test_start_point = Lines[6].split("=")[-1][:-1]
        if test_start_point == 1:
            Global_Setting_Var.TestAPP = "_Desktop"
        elif test_start_point == 2:
            Global_Setting_Var.TestAPP = "_IOS_WEB"
        else:
            Global_Setting_Var.TestAPP = "_Other1"
        user_test_name = user_test_name + Global_Setting_Var.TestAPP
        diff= Lines[6].split("=")[-1][:-1]
        if diff == 0:
            Global_Setting_Var.diffrence = Global_Setting_Var.diffrence_static
        elif diff == 1:
            Global_Setting_Var.diffrence = Global_Setting_Var.diffrence_dynamic
        elif diff == 2:
            Global_Setting_Var.diffrence = Global_Setting_Var.diffrence_extreme
        else:
            Global_Setting_Var.diffrence = Global_Setting_Var.diffrence_static


    Global_Setting_Var.terminate = 0
    test_name = Util.check_space(user_test_name)  # replaces the spaces with underscore
    Util.check_name_exists(Global_Setting_Var.ParentDirTest, test_name,
                      1)  # check if the test directory is already existing, popup message if it is


    RandScenrioName  = Util.CreateRandTestName(Global_Setting_Var.Notifile)

    # Create the test directory
    path = os.path.join(Global_Setting_Var.ParentDirTest, test_name)
    os.mkdir(path)

    fileNameImage = path + "/" + test_name  # prefix for the images file
    fileNameImage_number = 1  # suffix for the images file

    fileNameLog = path + "/" + test_name + ".txt"  # user log file name
    TestLog = open(fileNameLog, "w+")  # open the file for writing the user operation


    # create ATP file
    fileNameATP = path + "/" + test_name + "_ATP.txt"  # user ATP file name
    ATPfile = open(fileNameATP, "w+")  # open the file for writing the ATP - data from user step form
    Util.CreateDocHeader(Global_Setting_Var.versionFile, ATPfile, "ATP", test_name, user_test_summary)  # create header for the ATP txt file

    # create comment filedd
    fileNameATPcomment = path + "/" + test_name + "_comment.txt"  # user ATP comment file name
    CommentFile = open(fileNameATPcomment, "w+")  # open the file for writing the ATP comment- data from user step form
    Util.CreateDocHeader(Global_Setting_Var.versionFile, CommentFile, "comment",
                    test_name, user_test_summary)  # create header for the ATP commenttxt file
    Global_Setting_Var.toRec = 1  # flag for define if need to updet the log file or not, 1 = update , 0 = dont update
    Global_Setting_Var.start_time = time.time()  # start timer

    # create random string for IOS scenario name
    RandScenrioName = Util.CreateRandTestName(Global_Setting_Var.RSN)
    Util.copyRSN()
    #go_2desktop()  # Goto desktop as the beginning of the test

    # for test that contaion the WEB suffix go to the IOS web , if contain Desktop suffix do to the desktop for the
    # other do nothing
    #if (user_test_name[len(user_test_name)-3:len(user_test_name)]) =="WEB":
    if "WEB" in user_test_name:
        KillIOS()
        time.sleep(5)
        OpenSite(Global_Setting_Var.site2open)
    #elif (user_test_name[len(user_test_name) - 3:len(user_test_name)]) == "Desktop":
    elif "Desktop" in user_test_name:
        go_2desktop()
    else:
        pass


    text_not = "Record test " + test_name
    NotifThread = threading.Thread(target=Util.Open_Notefic, args=(text_not,), daemon=True)
    NotifThread.start()# presnt the status window

    Global_Setting_Var.toRec = 1 # start recording
    # start the thread listener keyboard and mouse
    K_listener = KeyboardListener(on_press=keyboard_press)
    M_listener = MouseListener(on_click=mouse_click, on_scroll=mouse_scroll)

    K_listener.start()
    M_listener.start()

    K_listener.join()
    M_listener.join()

    subprocess.Popen(["python", "Notification.py"])

    def main_c_mini(user_test_name_in, user_test_summary_in, diff_in):
        global TestLog
        global ATPfile
        global CommentFile
        global test_name
        global fileNameImage
        global fileNameImage_number
        global K_listener
        global M_listener

        pyautogui.FAILSAFE = False

        # dialog
        #user_test_name, user_test_summary, diff = DataWindow.gettestinput()  # gets test name and summary from user
        # user_test_name = user_test_name_in
        # user_test_summary = user_test_summary_in
        # diff = diff_in
        # Global_Setting_Var.diffrence = 5000


        Global_Setting_Var.stop_flag = 0
        # terminte the process befor we start
        if user_test_name == "terminate":
            terminateTheprocess()

        Global_Setting_Var.terminate = 0


        test_name = check_space(user_test_name)  # replaces the spaces with underscore
        check_name_exists(Global_Setting_Var.ParentDirTest, test_name,
                          1)  # check if the test directory is already existing, popup message if it is

        RandScenrioName = CreateRandTestName(Global_Setting_Var.Notifile)

        # Create the test directory
        path = os.path.join(Global_Setting_Var.ParentDirTest, test_name)
        os.mkdir(path)

        fileNameImage = path + "/" + test_name  # prefix for the images file
        fileNameImage_number = 1  # suffix for the images file

        fileNameLog = path + "/" + test_name + ".txt"  # user log file name
        TestLog = open(fileNameLog, "w+")  # open the file for writing the user operation

        # create ATP file
        fileNameATP = path + "/" + test_name + "_ATP.txt"  # user ATP file name
        ATPfile = open(fileNameATP, "w+")  # open the file for writing the ATP - data from user step form
        CreateDocHeader(Global_Setting_Var.versionFile, ATPfile, "ATP", test_name,
                        user_test_summary)  # create header for the ATP txt file

        # create comment filedd
        fileNameATPcomment = path + "/" + test_name + "_comment.txt"  # user ATP comment file name
        CommentFile = open(fileNameATPcomment,
                           "w+")  # open the file for writing the ATP comment- data from user step form
        CreateDocHeader(Global_Setting_Var.versionFile, CommentFile, "comment",
                        test_name, user_test_summary)  # create header for the ATP commenttxt file
        Global_Setting_Var.toRec = 1  # flag for define if need to updet the log file or not, 1 = update , 0 = dont update
        Global_Setting_Var.start_time = time.time()  # start timer

        # create random string for IOS scenario name
        RandScenrioName = CreateRandTestName(Global_Setting_Var.RSN)
        copyRSN()
        # go_2desktop()  # Goto desktop as the beginning of the test

        # for test that contaion the WEB suffix go to the IOS web , if contain Desktop suffix do to the desktop for the
        # other do nothing
        # if (user_test_name[len(user_test_name)-3:len(user_test_name)]) =="WEB":
        if "WEB" in user_test_name:
            KillIOS()
            time.sleep(5)
            OpenIOS()
        # elif (user_test_name[len(user_test_name) - 3:len(user_test_name)]) == "Desktop":
        elif "Desktop" in user_test_name:
            go_2desktop()
        else:
            pass

        text_not = "Record test " + test_name
        NotifThread = threading.Thread(target=Open_Notefic, args=(text_not,), daemon=True)
        NotifThread.start()  # presnt the status window

        Global_Setting_Var.toRec = 1  # start recording
        # start the thread listener keyboard and mouse
        K_listener = KeyboardListener(on_press=keyboard_press)
        M_listener = MouseListener(on_click=mouse_click, on_scroll=mouse_scroll)

        K_listener.start()
        M_listener.start()

        K_listener.join()
        M_listener.join()

        subprocess.Popen(["python", "Notification.py"])


if __name__ == "__main__":
    main_c()


