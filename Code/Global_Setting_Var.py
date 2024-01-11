# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 07:41:23 2022

@author: AZucker
"""
# input: none
# what does it do: read data for setting file and create global variable for general use
# output: none

global texthere
global TopLeft_X
global TopLeft_Y
global ButtomRight_X
global ButtomRight_Y
global ParentDirTest
global ParentDirResu
global SettingF
global TestListF
global GeneralResult
global versionFile
global Notifile
global RSN
global TRSl_X
global TRSl_Y
global WindowWidth
global WindowHeight
global diffrence
global diffrence_static
global diffrence_dynamic
global diffrence_extreme
global progressBar_Timing
global terminate
global TestAPP
global site2open
global chromedriver
global chromepath
global userSellector
global toRec
global Start_time
global image_treshold
global docFolder
global Lasttime
global Start_time
global f6_TopLeft_X
global f6_TopLeft_XTopLeft_Y
global f6_ButtomRight_X
global f6_ButtomRight_Y
global PicOption
global Remote_window_location
global window_size
global F7_IP
global F8_IP
global F9_IP
global RecordVsRun
global stop_flag
global PIDNotifWin
global wordAppPath
global Web_GUI
global Web_user_test_name
global Web_user_test_summary
global Web_diff
global Web_stepProcess
global Web_stepResult
global Web_stepComment
global Web_Critic
global scriptPath
global listA

import tkinter as tk

texthere = "Magniv"
userSellector = 0
toRec=0
Lasttime=0
Testtime=0
Start_time =0
PicOption=0
Remote_window_location = (100, 100)
Remote_window_size = (1366, 768)
RecordVsRun = 1
stop_flag = False
Web_GUI = False
Web_user_test_name = ""
Web_user_test_summary = ""
Web_diff = 0
Web_stepProcess = ""
Web_stepResult = ""
Web_stepComment = ""
Web_Critic = ""
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


#with open("D:/ElbitProjects/ATH/GIT/AutoTest/Setup/Setting.txt", "r") as SettingFile:  # read the setting parameters

with open("D:/ATH-AutoTestingSystem/AutoTestingSystem_Backend/Setup/Setting.txt", "r") as SettingFile:  # read the setting parameters
    # snapoint dimintion
    Lines = SettingFile.readlines()
    TopLeft_X = int(Lines[1].split(" ")[0])
    TopLeft_Y = int(Lines[2].split(" ")[0])
    ButtomRight_X = int(Lines[3].split(" ")[0])
    ButtomRight_Y = int(Lines[4].split(" ")[0])

    # files name and path
    ParentDirTest = Lines[8].split(" ")[0]
    ParentDirResu = Lines[9].split(" ")[0]
    SettingF = Lines[10].split(" ")[0]
    TestListF = Lines[11].split(" ")[0]
    GeneralResult = Lines[12].split(" ")[0]
    versionFile = Lines[13].split(" ")[0]
    Notifile = Lines[14].split(" ")[0]
    RSN = Lines[15].split(" ")[0]
    scriptPath = Lines[16].split(" ")[0]

    # Status Window dimintion and location
    TRSl_X = int(Lines[18].split(" ")[0])
    TRSl_Y = int(Lines[19].split(" ")[0])
    WindowWidth = int(Lines[20].split(" ")[0])
    WindowHeight = int(Lines[21].split(" ")[0])

    # diffrence to define fail
    diffrence_static = int(Lines[25].split(" ")[1])
    diffrence_dynamic = int(Lines[26].split(" ")[1])
    diffrence_extreme = int(Lines[27].split(" ")[1])

    progressBar_Timing = int(Lines[31].split(" ")[1])
    mouse_scroll = int(Lines[32].split(" ")[1])
    # data for the installation
    site2open = Lines[36].split(" ")[0]
    chromedriver = Lines[37].split(" ")[0]
    chromepath = Lines[38].split("    ")[0]
    # image treshold  in the greyscale images compare
    image_treshold = int(Lines[40].split(" ")[0])

    # image treshold  in the greyscale images compare
    docFolder = Lines[43].split(" ")[0]

    f6_TopLeft_X = int(Lines[47].split(" ")[0])
    f6_TopLeft_Y = int(Lines[48].split(" ")[0])
    f6_ButtomRight_X = int(Lines[49].split(" ")[0])
    f6_ButtomRight_Y = int(Lines[50].split(" ")[0])

    F7_IP = Lines[53].split(" ")[0]
    F8_IP = Lines[54].split(" ")[0]
    F9_IP = Lines[55].split(" ")[0]

    wordAppPath = Lines[57].split(" ")[0]

    genaralSimilarity = Lines[59].split(" ")[0]

def main():
    print("Runing Global_SettingV_Var.py directly")


if __name__ == "__main__":
    main()