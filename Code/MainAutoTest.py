import pyautogui

import Creattest
import runTest
import DataWindow
#from Code import Global_Setting_Var
import Global_Setting_Var
import time
import Util
from threading import Thread

def Service_Remote_API():
    # Create Test
    print("WEB_API:Create Test")
    Global_Setting_Var.Web_user_test_name = "Boris20ddd05"
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

def main():
    # t = Thread(target=Service_Remote_API)
    # t.start()
    status_data_update = 6

    if Global_Setting_Var.Web_GUI == False:
        selection = DataWindow.startupprocedure()
        if selection == 1:
            Creattest.main_c()
        elif selection == 2:
            runTest.main_r()
        else:
            pass
    else:
        while status_data_update != 10:
            time.sleep(2)
            Income_data = "D:\ATH-AutoTestingSystem\AutoTestingSystem_TempData\Income_data.ini"
            with open(Income_data, "r") as ID:  # open the Income data for decide what to do
                Lines = ID.readlines()
                status_data_update = Lines[1].split("=")[-1][:-1]
                print ("status_data_update " + status_data_update )
                if status_data_update == "2":
                    Util.replace_line(Income_data, 2, "CurrectCommand      =6")
                    ID.close()
                    Creattest.main_c()
                elif status_data_update == "4":
                    Util.replace_line(Income_data, 2, "CurrectCommand      =6")
                    ID.close()
                    runTest.main_r()
                elif status_data_update == "10":
                    ID.close()
                    break

                else:
                    ID.close()
                    pass





if __name__ == "__main__":
    main()
    #Service_Remote_API()