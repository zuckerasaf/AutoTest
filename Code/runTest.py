# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 16:02:02 2022

@author: AZucker
"""
import pyautogui
import time
import PIL.Image
import PIL.ImageChops
import PIL.ImageOps
import ctypes
import sys
from datetime import datetime
import ChromeIssue
import ImageProcess
#from Code import MainAutoTest
import MainAutoTest
from Util import *
from DataWindow import *
from ChromeIssue import *
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key
from Listener import *
import Listener
import threading
from selenium import webdriver
import Global_Setting_Var
pyautogui.FAILSAFE = False





############# function for this Script ###########
def update_data(TestResualt,OverAllResault,test_name,fileNameImage_number,status,diff_scale, diff) :
    TestResualt.writelines(test_name + "_step_" + str(fileNameImage_number) + status + " The difference scale =" + str(
        diff_scale) + " " + Util.Timefordispaly() + "\n")  # update test analasys file
    OverAllResault.writelines(
        test_name + "_step_ " + str(fileNameImage_number) + status + " define difference " + str(diff) +" The difference scale = " + str(
            diff_scale) + " " + Util.Timefordispaly() + "\n")  # update general result file


# input:
#   ATRfile = pointer for open file  -the ATR Txt file
#   ATPfile = pointer for open file  -the ATP Txt file
#   status = string - pass or file status  
#   difference  = integer - the difference value after image compare   
#   FileNameSourc = string - the name of the current image 
#   ATPLine  = Object – hold  all the line in the ATP TXT 
# what does it do: search the ATP text file for the current image name
# in case it found it its copy the founded line from the ATP to the ATR (file 4) and ad difference value and status
# output: none
def Update_ATR(ATRfile, ATPfile, status, difference, FileNameSourc, ATPLine):
    Filenameclean = ""

    for line in ATPLine:
        Filenameclean = str(FileNameSource.split("/")[-1:])[2:-6]
        #print(line)
        if Filenameclean in line:
            ATRfile.writelines(line[:-1] + "\t difference " + str(difference) + "\t status " + status + "\n")


# input:
#   FileNameSource = string - full path of JPG image    
#   FileNameNew = string - full path of JPG image
# what does it do: merge between the two JPGs to one JPG (new) that present the difference + save the new JPG
# output: none
def Create_Def_Image(FileNameSource, FileNameNew, number):
    Image1 = PIL.Image.open(FileNameSource)
    Image2 = PIL.Image.open(FileNameNew)
    diff = PIL.ImageChops.difference(Image1, Image2)
    DifffileNameImage = fileNameImage + "_step_" + number + "N_Diff.jpg"
    diff.save(DifffileNameImage)

def calcdiffrance(FileNameNew,FileNameSource,path,scale):
    diff = 0

    img_a_pixels_open = PIL.Image.open(FileNameSource)
    img_b_pixels_open = PIL.Image.open(FileNameNew)

    img_a_pixels_grey = PIL.ImageOps.grayscale(img_a_pixels_open)
    img_b_pixels_grey = PIL.ImageOps.grayscale(img_b_pixels_open)

    GreyScaleSourec = path + "GS_Source.jpg"
    GreyScaleNew = path + "GS_target.jpg"

    img_a_pixels_grey.save(GreyScaleSourec)
    img_b_pixels_grey.save(GreyScaleNew)

    img_a_pixels_grey_data = PIL.Image.open(GreyScaleSourec).getdata()
    img_b_pixels_grey_data = PIL.Image.open(GreyScaleNew).getdata()

    for pixel_g_a, pixel_g_b in zip(img_a_pixels_grey_data, img_b_pixels_grey_data):
        if abs(pixel_g_a - pixel_g_b) > scale:
            diff = diff + 1

    return diff

# write the mouse position and click  to log
# the function is in "Listener.py" file
# output: none
def mouse_click(x, y, button, pressed):
    Listener_mouse_click(x, y, button, pressed, Global_Setting_Var.start_time, ATRLogfilePointer)

# write the mouse scroll to log
# the function is in "Listener.py" file
def mouse_scroll(x, y, dx, dy):
    Listener_mouse_scroll(x, y, dx, dy,Global_Setting_Var.start_time, ATRLogfilePointer)


# write the keybord press to log
# the function is in "Listener.py" file
# def keyboard_press(key):
def keyboard_press(key):
    if key == Key.esc:
        Global_Setting_Var.terminate = 1


# def getcritical(ATPfile,fileNameImage_number):
#     ATPLine = ATPfile.readlines()
#     for i in range (1, len(ATPLine) - 1):
#         step_name = ATPLine[i].split(" ")[0]
#         if   step_name == fileNameImage_number:
#             critic = ATPLine[i].split(" ")[:0]
#             if critic == 'x':
#                 return 1
#     return 0

 ############# the script code start here  ###########
def main_r():
    global TestLog
    global FileNameSource
    global fileNameImage
    global ATRfile
    global test_name
    global ATRLogfilePointer
    global starttime
    global K_listener
    global M_listener
    global ATRLogfilePointer
    global total_time


    #TestLog = pointer to the file that contain the desire tests list
    TestLog = open(Global_Setting_Var.TestListF, "r")  # open the test list
    TestLine = TestLog.readlines()

    # Global_Setting_Var.terminate = "flag" for terminate the automatic run 1= terminate
    Global_Setting_Var.terminate = 0

    # run on the tests list file line by line until the EOF and checks
    # 1. The test name exists on the test directory
    # 2. in case there is old result for this test it deletes the old the result directory
    for y in range(1, len(TestLine) - 1):
        test_name = TestLine[y].split(" ")[0]
        Util.check_name_not_exists(Global_Setting_Var.ParentDirTest, test_name)
        Util.check_name_exists(Global_Setting_Var.ParentDirResu, test_name, 2)

    numberOfTest = 0
    # run on the tests list file line by line until the EOF the main loop !
    for x in range(1, len(TestLine) - 1):
        # create random string for IOS scenario name
        RandScenrioName = Util.CreateRandTestName(Global_Setting_Var.RSN)
        Util.copyRSN()
        # Create the result directory with reference to the desire test
        test_name = TestLine[x].split(" ")[0]
        path = os.path.join(Global_Setting_Var.ParentDirResu, test_name)
        os.mkdir(path)

        # full path of the running test LOG
        fileNameLog = Global_Setting_Var.ParentDirTest + test_name + "/" + test_name + ".txt"
        TestLog = open(fileNameLog, "r")  # open the test file that is going to be executed
        Lines = TestLog.readlines()  # read all the line in the test file that is going to be executed - the most important
        # line
        number_of_line = len(Lines)  # the anoumnt of line in the test that is going to be execute

        #full path of the test analysis in result directory
        fileNameLogResault = Global_Setting_Var.ParentDirResu + test_name + "/" + test_name + "_analasys.txt"
        fileNameImage = Global_Setting_Var.ParentDirResu + test_name + "/" + test_name  # prefix for the new images files
        filegeneralLogResault = Global_Setting_Var.GeneralResult  # full path for the general resault file

        # file for display the current test result
        currentRunningresultfile = Global_Setting_Var.ParentDirResu + "/currentresult.txt"
        fileNameImage_number = 1  # suffix for the new images file

        # create log file of the test similar logic while creating the test for later compare
        ATRLogfile = Global_Setting_Var.ParentDirResu + test_name + "/" + test_name + "CopyLog.txt"  # user log file name
        ATRLogfilePointer = open(ATRLogfile, "w+")  # open the file for writing the user operation

        # OPen ATP file for copy the header data to the ATR
        fileNameATP = Global_Setting_Var.ParentDirTest + test_name + "/" + test_name + "_ATP.txt"
        ATPfile = open(fileNameATP, "r")
        ATPLine = ATPfile.readlines()

        # arrange the ATR file
        fileNameATR = Global_Setting_Var.ParentDirResu + test_name + "/" + test_name + "_ATR.txt"  # full path for the ATR file in the resualt file
        ATRfile = open(fileNameATR, "w+")
        # get the difference value from the ATP
        Global_Setting_Var.diffrence = Util.ReteurnDiffrencevalue(fileNameATP)
        testSummary = ATPLine[1]
        Util.CreateDocHeader(Global_Setting_Var.versionFile, ATRfile, "ATR", test_name, testSummary)  # create the ATR txt file header

        TestResualt = open(fileNameLogResault, "w+")  # open the test analysand file
        OverAllResault = open(filegeneralLogResault, "a")  # open the general result file
        currentRunningresault = open(currentRunningresultfile, "a")  # open the general result file


        # presnt the status window with the test name
        text_not = "Automatic run of :  " + test_name + ". Its test number " + str(x) + " out of : " + str(len(TestLine) - 2)
        NotifThread = threading.Thread(target=Util.Open_Notefic, args=(text_not,), daemon=True)



        if test_name.find("IOS_WEB") != -1: # if the test is with IOS open IOS
            Util.go_2desktop()  # Goto desktop as the beginning of the test
            NotifThread.start()
            ChromeIssue.KillIOS()
            time.sleep(2)
            ChromeIssue.OpenSite(Global_Setting_Var.site2open)
            time.sleep(2)
        elif test_name.find("Desktop") != -1: # Goto desktop as the beginning of the test
            Util.go_2desktop()
            NotifThread.start()
        else:
            NotifThread.start()



        #starttime = time.time()  # start the timer
        Global_Setting_Var.start_time = time.time()  # start timer

        # start the thread listener keyboard and mouse
        K_listener = KeyboardListener(on_press=keyboard_press)
        #M_listener = MouseListener(on_click=mouse_click, on_scroll=mouse_scroll)
        K_listener.start()
        #M_listener.start()



        index = 0
        scroll_setp = 0
        num_scroll_setp = 0
        mouseOperationCounter = 0
        fileNameImage_number = 1
        numberoffail = 0
        numberofpass = 0
        generalresault = 0
        currentRunningresault.writelines(Util.Timefordispaly() + " running Test :" + test_name + "\n")
        while index < number_of_line - 1:

            # zeroized  the data
            controller = ""
            controller2 = ""
            xValueMouse = 0
            yValueMouse = 0
            buttonMouse = ""
            commandMouse = ""
            keyPressed = ""
            #totaltime = round((time.time() - starttime), 2)  # update the current time

            # lineContainList = Global_Setting_Var.Lines[index].split(' ') - to be discuss with marco
            lineContainList = Lines[index].split(' ')
            #print(index)
            controller = lineContainList[1]  # find the command type  in the current test step  : "close" or "scrolled" or
            # "mouse" or "keyboard"

            # if we reach "close" = the end of the test procedure so  break out
            if lineContainList[0] == "close":
                Util.close_Notefic()  # close the status window = running auto test
                break

            # in case of pres esc while sutomatic running the system kill the python
            if Global_Setting_Var.terminate == 1:
                ATRLogfilePointer.writelines("close the file")
                #M_listener.stop()
                K_listener.stop()
                ATRLogfilePointer.close()
                Util.go_2desktop()
                text_not = "the automatic run  was terminated"
                Open_Notefic(text_not)
                #os.system("taskkill /f /t /IM python.exe")

            # the system wait until the running time is equal or greater from the test step time
            if (any(map(str.isdigit, lineContainList[0]))):
                StepTime = float(lineContainList[0])
            Global_Setting_Var.Lasttime = time.time()
            runTime = 0
            while runTime < StepTime:
                #totaltime = round((time.time() - starttime), 2)
                #runTime = round((time.time() - Global_Setting_Var.Lasttime), 2)
                runTime =(time.time() - Global_Setting_Var.Lasttime)
            Global_Setting_Var.Lasttime = time.time()
            # if the current step is scrolled move the mouse to the written location and make the number of scroll desire
            # (sum of all scroll command)
            if controller == 'scrolled':
                if Lines[index + 1].split(' ')[
                    1] != 'scrolled':  # make the scroll command if the next step isnot scroll command
                    xValueMouse = int(lineContainList[3].split(',')[0][1:])  # read mouse X value
                    yValueMouse = int(lineContainList[3].split(',')[1][:-1])  # read mouse Y value
                    pyautogui.moveTo(xValueMouse, yValueMouse, 0.1)  # move the mouse
                    scroll_setp = scroll_setp * Global_Setting_Var.mouse_scroll  # alignment value for scroll command
                    pyautogui.scroll(scroll_setp)  # make scroll command

                    index = index + 1
                    ATRLogfilePointer.writelines(
                        str(runTime) + ' mouse scrolled at ({0},{1}) {2} times  \n'.format(yValueMouse, xValueMouse,
                                                                                           num_scroll_setp))
                    scroll_setp = 0
                    num_scroll_setp = 0
                else:
                    index = index + 1
                    if lineContainList[4][-3:-1] == '-1':
                        scroll_setp = scroll_setp - 1
                        num_scroll_setp = num_scroll_setp + 1

                    else:
                        scroll_setp = scroll_setp + 1
                        num_scroll_setp = num_scroll_setp + 1

            # if the current step is mouse move the mouse to the written location and make click on  or drag command
            elif controller == 'mouse' and lineContainList[2] == "down":
                mouseOperationCounter = mouseOperationCounter + 1
                xValueMouse = int(lineContainList[4].split(',')[0][1:])  # read mouse X value
                yValueMouse = int(lineContainList[4].split(',')[1][0:-1])  # read mouse Y value
                buttonMouse = lineContainList[-2].split('.')[1]

                xnewValueMouse = int(Lines[index + 1].split(' ')[4].split(',')[0][1:])
                ynewValueMouse = int(Lines[index + 1].split(' ')[4].split(',')[1][:-1])
                diff_movmemnt = abs(xValueMouse - xnewValueMouse) + abs(yValueMouse - ynewValueMouse)
                if diff_movmemnt < 10:  # if the current location of the mouse and the next location of the mouse
                    # equal to button press up its "Click"
                    pyautogui.moveTo(xValueMouse, yValueMouse, 0.1)  # move the mouse
                    pyautogui.click(button=buttonMouse)  # do the click (left or right)
                    ATRLogfilePointer.writelines(
                        str(runTime) + ' mouse click at ({0},{1}) with Button. {2} \n'.format(yValueMouse, xValueMouse,
                                                                                              buttonMouse))
                    xnewValueMouse = 0
                    ynewValueMouse = 0
                    index = index + 2

                else:  # its drug and drop command
                    pyautogui.moveTo(xValueMouse, yValueMouse, 0.1)  # move the mouse
                    Dragtime = float(Lines[index + 1].split(' ')[0]) - float(Lines[index].split(' ')[0])
                    xnewValueMouse = int(Lines[index + 1].split(' ')[4].split(',')[0][1:])
                    ynewValueMouse = int(Lines[index + 1].split(' ')[4].split(',')[1][:-1])
                    pyautogui.dragTo(xnewValueMouse, ynewValueMouse, 1.0,
                                     button=buttonMouse)  # do the drag and drop
                    ATRLogfilePointer.writelines(
                        str(runTime) + ' mouse drag to  ({0},{1}) with Button {2} \n'.format(xnewValueMouse,
                                                                                             ynewValueMouse,
                                                                                             buttonMouse))
                    index = index + 2

            # if the current step is keyboard command define if it "special key" or "letter key" or "ctrl left"
            elif controller == 'keyboard':
                index = index + 1
                listA = ['accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
                         'browserback', 'browserfavorites', 'browserforward', 'browserhome',
                         'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
                         'convert', 'ctrl', 'ctrlright', 'decimal', 'del', 'delete',
                         'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                         'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                         'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                         'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
                         'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
                         'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                         'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
                         'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
                         'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
                         'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
                         'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                         'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                         'command', 'option', 'optionleft', 'optionright']

                keyPressed = lineContainList[-2].split('.')[-1][:]

                if keyPressed == "f6" or keyPressed == "ctrl_l":  # if f5 or f6 or f7
                    Util.take_snapshot(fileNameImage, Global_Setting_Var.TopLeft_X, Global_Setting_Var.TopLeft_Y,
                                  Global_Setting_Var.ButtomRight_X, Global_Setting_Var.ButtomRight_Y, fileNameImage_number)

                    FileNameNew = fileNameImage + "_step_" + str(fileNameImage_number) + "P.jpg"
                    FileNameSource = Global_Setting_Var.ParentDirTest + test_name + "/" + test_name + "_step_" + str(fileNameImage_number) + "P.jpg"
                    #print(FileNameNew + " " + FileNameSource)
                    ATRLogfilePointer.writelines(str(runTime) + ' Ctrl_l was push image was taken \n')

                    difference = 0
                    critic = 0
                    stepname = Lines[index]
                    if Lines[index].split(' ')[0] == "show":
                        critic = 1
                        Type = "showstoper"
                    else:
                        Type = "normal"

                    path = Global_Setting_Var.ParentDirTest + test_name + "/"

                    difference = ImageProcess.calcdiffrance(FileNameNew, FileNameSource, path, Global_Setting_Var.image_treshold,str(fileNameImage_number))
                    diff_scale = difference / Global_Setting_Var.diffrence
                    #print (difference , Global_Setting_Var.diffrence)

                    resualtImagename = FileNameNew.split("/")[-1]
                    # search if this current step is critical in the ATP file
                    if diff_scale > 1 and critic == 1:
                        status = 'fail critic step'
                        update_data(TestResualt, OverAllResault, test_name, fileNameImage_number, status, diff_scale,Global_Setting_Var.diffrence)

                        Update_ATR(ATRfile, ATPfile, status, difference, FileNameSource,ATPLine)  # update test ATR file
                        #Create_Def_Image(FileNameSource, FileNameNew, str(fileNameImage_number))  # create merge image between the old and the new
                        currentRunningresault.writelines("#" + test_name + " #step number: #" + str(fileNameImage_number) + " #Type: #" + Type + " #" + stepname[:-1] + " #Fail -> #" + resualtImagename + " #"+ Util.Timefordispaly() +"#\n")
                        index = number_of_line
                        generalresault = generalresault + 1
                    elif diff_scale <= 1:  # in case the difference value smaller then predefine in setting file
                        status = 'Pass'
                        update_data(TestResualt, OverAllResault, test_name, fileNameImage_number, status, diff_scale,Global_Setting_Var.diffrence)
                        Update_ATR(ATRfile, ATPfile, status, difference, FileNameSource,
                                   ATPLine)  # update test ATR file
                        #Create_Def_Image(FileNameSource, FileNameNew,str(fileNameImage_number))  # create merge image between the old and the new
                        #currentRunningresault.writelines("\t step number: #" + str(fileNameImage_number) + " #" +stepname[:-1] + " #pass -> #" + resualtImagename +"\n") #Lines[index].split("\t")[1])
                        currentRunningresault.writelines("#" + test_name + " #step number: #" + str(fileNameImage_number) + " #Type: #" + Type + " #" + stepname[:-1] + " #Pass -> #" + resualtImagename + " #"+ Util.Timefordispaly() +"#\n")
                        generalresault = generalresault + 1
                    else:  # in case the difference value bigger then the  predefine in setting file
                        status = 'Fail'
                        update_data(TestResualt, OverAllResault, test_name, fileNameImage_number, status, diff_scale,Global_Setting_Var.diffrence)
                        Update_ATR(ATRfile, ATPfile, status, difference, FileNameSource,
                                   ATPLine)  # update test ATR file
                        #Create_Def_Image(FileNameSource, FileNameNew,str(fileNameImage_number))  # create merge image between the old and the new
                        currentRunningresault.writelines("#" + test_name + " #step number: #" + str(fileNameImage_number) + " #Type: #" + Type + " #" + stepname[:-1] + " #Fail -> #" + resualtImagename + " #"+ Util.Timefordispaly() +"#\n")

                        generalresault = generalresault + 1

                    fileNameImage_number = fileNameImage_number + 1
                    index = index + 1

                # remote desktop to CGF1
                elif keyPressed == "f7":
                    Util.open_remote_desktop(Global_Setting_Var.F7_IP, Global_Setting_Var.Remote_window_location,
                                        Global_Setting_Var.Remote_window_size)
                # remote desktop to TC
                elif keyPressed == "f8":
                    Util.open_remote_desktop(Global_Setting_Var.F8_IP, Global_Setting_Var.Remote_window_location,
                                        Global_Setting_Var.Remote_window_size)
                # remote desktop to Own1
                elif keyPressed == "f9":
                    Util.open_remote_desktop(Global_Setting_Var.F9_IP, Global_Setting_Var.Remote_window_location,
                                        Global_Setting_Var.Remote_window_size)

                # simulate alt-tab functione
                elif keyPressed == "f2" or keyPressed== "ctrl_r":
                    alt_Tab()

                elif keyPressed in listA:  # if "speciel key" press down and up
                    pyautogui.keyDown(keyPressed)
                    pyautogui.keyUp(keyPressed)

                else:  # if "letter key" type the letter
                    keyPressed = lineContainList[-2][:-1].split('\r')[0]
                    txt = keyPressed[1]
                    pyautogui.typewrite(txt)

            else:
                index = index + 1


        ATRLogfilePointer.writelines("close the file")
        #M_listener.stop()
        #K_listener.stop()
        ATRLogfilePointer.close()
        Util.close_Notefic()  # close the status window = running auto test

        # text_not = test_name + " is been analysand, its test number " + str(x) + " out of : " + str(len(TestLine) - 2)
        # progressThread = threading.Thread(target=Open_analasys_update, args=(text_not, fileNameImage_number,), daemon=True)
        # progressThread.start()

        now = str(datetime.datetime.now())
        time.sleep(2)
        # open the ATP for referane

        generalresault = 0
        numberofpass = 0
        numberoffail = 0

        if generalresault < 1:  # if all the steps is in "pass" status the overall test will be define as pass
            OverAllResault.writelines(test_name + " pass " + Util.Timefordispaly() + "\n")

        # close the files connect to this test run
        TestResualt.close()
        ATRfile.close()
        ATPfile.close()
        ATRLogfilePointer.close()
        Util.DBG(fileNameLog, ATRLogfile, fileNameATR)

        # close_Notefic()  # close status window
        #close_analasys_update()


    OverAllResault.close()  # close general result file
    currentRunningresault.close() # close the current test result file

    #Notepadath = r'C:\Windows\System32\notepad.exe'
    #p = subprocess.Popen([Notepadath, currentRunningresultfile])
    K_listener.stop()  # stop header

    Util.runMainAutoScript()

    #endmsg()




if __name__ == "__main__":
    main_r()