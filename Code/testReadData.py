import time
import os

def whereIsIT(string, LineList):
    count = 0
    for line in LineList:
        count = count+1
        if string in line:
            return count
    return  0



def bringData(File):
    my_dict = {"TestID" : "v1", "MainVersion" : " v2", "Name": "v3", "Summary" : "v4", "ResultThreshold" : " v5 ", "RunTimeout" : "v6", "Prerequisite" : "v7", "StartPoint" : "v8", }
    create_time = os.path.getctime(File)
    try:
        TestLog = open(File,"r")  # open the test list
        TestLine = TestLog.readlines()
        if len(TestLine)<2:
            return ("none")
        my_dict["TestID"] = hex(int(create_time))[2:]
        my_dict["MainVersion"] ='NA'
        count = whereIsIT("*******", TestLine)
        my_dict["Name"] =TestLine[count-1].split(" ")[1]
        my_dict["Summary"] =TestLine[1].split("\n")[0]
        count = whereIsIT("Test difference", TestLine)
        my_dict["ResultThreshold"] = TestLine[count-1].split(":")[1][:-1]
        my_dict["RunTimeout"] = 'NA'
        my_dict["Prerequisite"] ='NA'
    except:
        return ("none")

    if "IOS_WEB"in( my_dict["Name"]):
        my_dict["StartPoint"] = 'IOS_WEB'
    elif "Desktop"in( my_dict["Name"]):
        my_dict["StartPoint"] = 'Desktop'
    else:
        my_dict["StartPoint"] = 'Other'

    #print(my_dict)
    return (my_dict)


#
# temp ={}
# temp = bringData("D:\ATH-AutoTestingSystem\AutoTestingSystem_Backend\Tests\Test_3011_IOS_WEB\Test_3011_IOS_WEB_ATP.txt")
# print (temp)

# Replace 'your_folder_path' with the actual path to your main folder
def returnDic(folder_path):
    new_dict =[]
    # Walk through the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file has a .txt extension
            if file.endswith("_ATP.txt") or file.endswith("_ATR.txt"):
                # Print the full path to the txt file
                txt_file_path = os.path.join(root, file)
                #print(txt_file_path)
                temp = bringData(txt_file_path)
                if temp!= "none":
                    #print (temp)
                    new_dict.append(temp)
    return (new_dict)


def bringLoggerData(File):
    log_data_list = []

    with open(File, "r") as TestLog:
        for line in TestLog:
            if line.startswith("#"):
                temp = {
                    "TestName": line.split("#")[1].strip(),
                    "StepName": line.split("#")[3].strip(),
                    "StepDescription": line.split("#")[6].split("\t")[1].strip(),
                    "StepType": line.split("#")[5].strip(),
                    "StepStatus": line.split("#")[7].strip(),
                    "Time": line.split("#")[9].strip(),  # Convert to float or another appropriate type
                    "PicName": line.split("#")[8].strip(),
                    "Spare": line.split("#")[10].strip()
                }
                # print(temp)
                log_data_list.append(temp)

    return log_data_list


temp ={}
temp = bringLoggerData("D:\ATH-AutoTestingSystem\AutoTestingSystem_Backend\Results\currentresult.txt")
print (temp)
# folder_path = "C:\D\ATH-AutoTestingSystem\AutoTestingSystem_Backend\Tests"
# temp = returnDicTest(folder_path)
# print(temp)