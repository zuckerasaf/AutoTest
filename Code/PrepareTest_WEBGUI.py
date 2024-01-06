import Global_Setting_Var
import Util


def crteateFile(string):
    TestLog = open(Global_Setting_Var.TestListF, "w")  # open the test list
    TestLog.write(
        "# this file contain the list of Test_Name (similar name to the one in test folder). Add space + ""Test"" after the test name \n")
    TestList = string.split(',')
    for i in range(len(TestList)):
        TestLog.write(TestList[i] + " Test\n")
    TestLog.write("*********************************************EOF**************************************\n")
    TestLog.close()

def arangeTheData(string):
    Income_data = "D:\ATH-AutoTestingSystem\AutoTestingSystem_TempData\Income_data.ini"
    crteateFile(string)
    Util.replace_line(Income_data, 2, "CurrectCommand      =4")
