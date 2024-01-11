# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 13:41:25 2022

@author: AZucker
"""
import tkinter
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random
import sys
import Global_Setting_Var
#from Code import MainAutoTest
import MainAutoTest
from Util import *
import Util
from datetime import date
import CreateDoc
import UpdateImages
from DuplicateTest import getNewtestName
from PIL import Image, ImageDraw, ImageFont
import ImageProcess


#import TranslateUserDifftoValue from Util
#subprocess imort Popen

# input: strings
# what does it do: update variables from GUI window to global
# output: none
def Setoutstep(text1, text2, text3 ,text4):
    global stepProcess
    global stepResult
    global stepComment
    global critic
    stepProcess = text1
    stepResult = text2
    stepComment = text3
    critic = text4
    # print(stepProcess + " # " + stepResult + " # " + stepComment)


# input:
#   ATPFileName = string - path for the relevant ATP.txt file 
#   StepProcess = string - from UI form  
#   StepResult = string - from UI form 
#   Stepnumber = integer - number of the current picture \ control press in this test  
#   fileNameImage = string - the path of the current snapshot image 
# what does it do: add line with all the data for the ATP.txt file
# output: none
def UpdateATP(ATPFileName, StepProcess, StepResult, Stepnumber, fileNameImage):
    ATPFileName.writelines(str(Stepnumber) + '\t' + StepProcess + '\t' + StepResult + '\t' + fileNameImage + 'P\n')


# input:
#   CommentFileName = string - path for the relevant comment.txt file 
#   StepProcess = string - from UI form  
#   StepResult = string - from UI form 
#   Stepnumber = integer - number of the current picture \ control press in this test  
#   StepComment = string - from UI form 
#   fileNameImage = string - the path of the current snapshot image 
# what does it do: add line with all the data for the comment.txt file
# output: none
def UpdateComnetATP(CommentFileName, StepProcess, StepResult, Stepnumber, StepComment, fileNameImage):
    CommentFileName.writelines(
        str(Stepnumber) + '\t' + StepProcess + '\t' + StepResult + '\t' + StepComment + '\t' + fileNameImage + 'P\n')

# input:
#   CommentFileName = string - path for the relevant comment.txt file
#   critics = string - if the step is critic
#   StepProcess = string - from UI form
# what does it do: add line with all the data for the comment.txt file
# output: none
def UpdateLog(LogFileName,critics,StepProcess):
    LogFileName.writelines( critics + '\t' + StepProcess +  '\n')

def add_text_to_image(input_image_path, output_image_path, text_to_add):
    # Open the image file
    image = Image.open(input_image_path)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Choose a font and size
    font = ImageFont.truetype("arial.ttf", 136)


    # Choose a color for the text
    text_color = (0, 0, 0)  # White color in RGB

    # Choose the position to place the text (x, y)
    text_position = (300, 300)

    # Add text to the image
    draw.text(text_position, text_to_add, font=font, fill=text_color)

    # Save the modified image
    image.save(output_image_path)

# input:
#   ATPFileName = string - path for the relevant ATP.txt file
#   CommentFileName = string - path for the relevant comment.txt file  
#   fileNameImage = string - the path of the current snapshot image 
#   TestName = string -current test name   
# what does it do:
#   Step 1 build UI form for collect the data for the current step
#   Step 2 callSetout() - update global data 
#   Step 3 UpdateATP() - update the ATP file 
#   Step 4 UpdateComnetATP() - update the comment file 
#   Step 5 close() - terminate the UI form  
# output:
#   stepProcess = string - from UI form
#   stepResult = string - from UI form  
#   stepComment = string - from UI form
def getinput(Logfile, ATPFileName, CommentFileName, fileNameImage, TestName, Stepnumber):
    Stepnumber = Stepnumber
    StepProcess = TestName + "_" + str(Stepnumber)
    StepResult = TestName + "_" + str(Stepnumber) + "_done"
    fileNameImage = fileNameImage + "_step_" + str(Stepnumber)
    Critic =""

    Stepinput = Tk()
    Stepinput.configure(background='light blue')
    Stepinput.title("Auto Test - step information ")
    Stepinput.option_add('*Font', '19')

    # create a UI form o out it on top the other open windows
    Stepinput.geometry("600x300")
    Stepinput.attributes("-topmost", True)

    Test_Name_Label = Label(Stepinput, text=TestName, bg="light blue")  # create a Step Process label
    Step_Number_Label = Label(Stepinput, text=" Step number - " + str(Stepnumber),
                              bg="light blue")  # create a Step Process label
    Step_Process_Label = Label(Stepinput, text="Step Process", bg="light blue")  # create a Step Process label
    Step_Result_Label = Label(Stepinput, text="Step Result", bg="light blue")  # create a Step Result label

    # placing the widgets at respective positions in table like structure .
    Test_Name_Label.place(x=10, y= 10)
    Step_Number_Label.place(x=300, y= 10)
    Step_Process_Label.place(x=10, y= 50)
    Step_Result_Label.place(x=10, y= 100)

    # create a text entry box
    Step_Process = Entry(Stepinput, width=30)
    Step_Process.insert(0, StepProcess)
    Step_Result = Entry(Stepinput, width=30)
    Step_Result.insert(0, StepResult)

    # placing the widgets at respective positions in table like structure .
    Step_Process.place(x=150, y= 50)
    Step_Result.place(x=150, y= 100)

    # terminate the UI form
    def Closestep():
        Stepinput.destroy()

    # On button press does step 2 - 5 
    def Myclick():
        StepProcess = Step_Process.get()
        StepResult = Step_Result.get()
        Critic = dropritic.get()
        Setoutstep(StepProcess, StepResult, "none", Critic)
        UpdateATP(ATPFileName, StepProcess, StepResult, Stepnumber, fileNameImage)
        Closestep()

    # get user comment for tis test
    def commentclick():
        commentWin = Tk()
        commentWin.configure(background='light green')
        commentWin.title("Auto Test")
        commentWin.option_add('*Font', '19')
        commentWin.geometry("550x150")
        commentWin.attributes("-topmost", True)
        Comment_Label = Label(commentWin, text="Add comment for this step", bg="light green")  # create a Step comment label
        Comment_Label.pack() #grid(row=1, column=1)
        Comment = Entry(commentWin, width=50)
        Comment.pack()#.grid(row=2, column=1, ipadx="100")

        def Closecommnet():
            commentWin.destroy()

        def Savecomment():
            StepComment = Comment.get()
            UpdateComnetATP(CommentFileName, "", "", Stepnumber, StepComment, fileNameImage)
            text_to_add = "failed step \n "+ StepComment  + "\n" + Util.CreateRandTestName(Global_Setting_Var.RSN)
            fullfileNameImage = fileNameImage + "P.jpg"
            add_text_to_image(fullfileNameImage, fullfileNameImage, text_to_add)
            Closecommnet()
        SavecommentButton = Button(commentWin, text="save comment", height=2, width=12, command=Savecomment)
        SavecommentButton.pack() #grid(row=3, column=0)

        commentWin.protocol("WM_DELETE_WINDOW", Closecommnet)

        commentWin.mainloop()

    # placing the widgets at respective positions in table like structure .
    myButton = Button(Stepinput, text="save", height=2, width=7, command=Myclick)
    myButton.place(x=50, y= 200)

    commentButton = Button(Stepinput, text="comment", height=2, width=7, command=commentclick)
    commentButton.place(x=200, y= 200)

    linkButton = Button(Stepinput, text="link", height=2, width=7)
    linkButton.place(x=350, y= 200)

    Criticoption = ["normal", "show stopper"]

    # dactatype of menu text
    dropritic = StringVar(Stepinput)
    # initial menu text
    dropritic.set(Criticoption[0])
    # Create Dropdown menu
    drop = OptionMenu(Stepinput, dropritic, *Criticoption)
    drop.place(x=50, y= 150)

    # Bind the on_close function to the window close event
    Stepinput.protocol("WM_DELETE_WINDOW", Myclick)

    Stepinput.mainloop()
    return (stepProcess, stepResult, stepComment, critic)


# input: strings
# what does it do: update variables from GUI window to global
# output: none
def SetoutTest(text1, text2, num1):
    global testName
    global testSummary
    global diffrencevalue
    testName = text1
    testSummary = text2
    diffrencevalue = num1


# input: none
# what does it do:
#   Step 1 build UI form for collect the name of the test 
#   Step 2 callSetout() - update global data 
#   Step 3 close() - save ot terminate the UI form  
# output:
#   test name  = string - from UI form

def gettestinput():
    Env = ""
    TestName = "Test_" + str(random.randint(1, 9999))  # create default test name
    TypeDiffrenceTest = 9 
    
    Testinput = Tk()
    Testinput.configure(background='light blue')
    Testinput.title("Auto Test  - Create ")
    Testinput.option_add('*Font', '19')

    # def open_WebIOS():
    #     Popen("webIOS.py")

    # create a UI form o out it on top the other open windows
    Testinput.geometry("820x360")
    Testinput.lift()

    # create a text entry box and  placing the widgets at respective positions in table like structure .
    Test_Name_Label = Label(Testinput, text="Insert test name below - use only letters or numbers or spaces",
                            bg="light blue")  # create a test name label
    Test_Name_Label.grid(row=1, column=1)
    Test_Summary_Label = Label(Testinput, text="Insert test Prerequisite",
                               bg="light blue")  # create a test name label
    Test_Summary_Label.grid(row=3, column=1)

    Test_Space_Label = Label(Testinput, text="******************************************",
                                  bg="light blue")  # create a test name label
    Test_Space_Label.grid(row=5, column=1)

    Test_Trash_hold_Label = Label(Testinput, text="Test trash hold: Static, Dynamic or Extreme",
                               bg="light blue")  # create a test name label
    Test_Trash_hold_Label.grid(row=6, column=1)

    Test_Environment_Label = Label(Testinput, text="Test environment",
                               bg="light blue")  # create a test name label
    Test_Environment_Label.grid(row=8, column=1)



    # create a text entry box and  placing the widgets at respective positions in table like structure .
    Test_Name = Entry(Testinput, width=20)
    Test_Name.insert(0, TestName)
    Test_Name.grid(row=2, column=1, ipadx="100")

    Test_Summary = Entry(Testinput, width=20)
    Test_Summary.insert(0, TestName)
    Test_Summary.grid(row=4, column=1, ipadx="100")


    # terminate the UI form
    def CloseTest():
        Testinput.destroy()

    # On button press does step 2 - 3 
    def Myclick_2save():
        TestName = Test_Name.get()
        TestSummary = Test_Summary.get()
        selDiffrence()
        selenvirumnet()
        SetoutTest(TestName+Global_Setting_Var.TestAPP, TestSummary,Global_Setting_Var.diffrence)
        CloseTest()

    # terminate the procedure of the testing
    def exitTheprocess():
        TestName = "terminate"
        TestSummary = "terminate"
        SetoutTest(TestName, TestSummary, 5000)
        CloseTest()
        #sys.exit()
        
    def selDiffrence():
        diffrenceType = var.get()
        Global_Setting_Var.diffrence = _TranslateUserDifftoValue(diffrenceType)

    def selenvirumnet():
        envirumnetType = var_env.get()
        if envirumnetType == 0:
            Global_Setting_Var.TestAPP = "_Desktop"
        elif envirumnetType == 1:
            Global_Setting_Var.TestAPP = "_IOS_WEB"
        elif envirumnetType == 2:
            Global_Setting_Var.TestAPP =  "_Other1"
        else:
            Global_Setting_Var.TestAPP = "_Other1"


    def _TranslateUserDifftoValue(num):

        if num == 0:
            difference = Global_Setting_Var.diffrence_static
        elif num == 1:
            difference = Global_Setting_Var.diffrence_dynamic
        elif num == 2:
            difference = Global_Setting_Var.diffrence_extreme
        else:
            difference = 0
        return difference

        

    # placing the widgets at respective positions in table like structure .
    myButton = Button(Testinput, text="save", height=2, width=8, command=Myclick_2save)
    myButton.grid(row=3, column=0)

    # placing the widgets at respective positions in table like structure .
    myButton = Button(Testinput, text="terminate", height=2, width=8, command=exitTheprocess)
    myButton.grid(row=3, column=2)
    
      
    var = IntVar()

    R1 = Radiobutton(Testinput, text="Static", bg="light blue", variable=var, value=0, command=selDiffrence)
    R1.grid(row=7, column=0, padx="10", pady="10", sticky="W")
    R2 = Radiobutton(Testinput, text="Dynamic", bg="light blue",variable=var, value=1, command=selDiffrence)
    R2.grid(row=7, column=1, padx="200", pady="10", sticky="W")
    R3 = Radiobutton(Testinput, text="Extreme",bg="light blue", variable=var, value=2, command=selDiffrence)
    R3.grid(row=7, column=2, sticky="W")

    #Testinput.mainloop()

    var_env = IntVar()

    R1_E1 = Radiobutton(Testinput, text="Desktop", bg="light blue",variable=var_env, value=0, command=selenvirumnet)
    R1_E1.grid(row=9, column=0, padx="10", pady="10", sticky="W")
    R2_E2= Radiobutton(Testinput, text="IOS_WEB", bg="light blue",variable=var_env, value=1, command=selenvirumnet)
    R2_E2.grid(row=9, column=1, padx="200", pady="10", sticky="W")
    R3_E3 = Radiobutton(Testinput, text="Other1",bg="light blue", variable=var_env, value=2, command=selenvirumnet)
    R3_E3.grid(row=9, column=2, sticky="W")

    # Bind the on_close function to the window close event
    Testinput.protocol("WM_DELETE_WINDOW", exitTheprocess)

    Testinput.mainloop()

    return (testName, testSummary,diffrencevalue)


def startupprocedure():

    startupform = tk.Tk()
    #startupform.configure(background='yellow')
    startupform.title("Auto Test start up")
    startupform.option_add('*Font', '19')
    startupform.geometry("1300x950+50+50")

    #
    startupform_Label = Label(startupform, text="what would you like to do? ,  Create new test,  Run tests plan from Library or Create report  ")  # create a test name label
    startupform_Label.place(x=10, y= 10)
    Library_Label = Label(startupform, text="Test Library")  # create a test name label
    Library_Label.place(x=100, y= 50)
    Library_Result_Label = Label(startupform, text="Test Result Library")  # create a test name label
    Library_Result_Label.place(x=870, y= 50)

    myTestList = os.listdir(Global_Setting_Var.ParentDirTest)
    myTestListBox = Listbox(startupform, height=10, selectmode=MULTIPLE)
    #myTestListBox.pack(padx=20,pady=150, expand=TRUE, fill=BOTH, side=LEFT)
    myTestListBox.place(x=30, y=80, width=500, height=500)

    scrollbarTest = Scrollbar(startupform, orient=VERTICAL, command=myTestListBox.yview)
    myTestListBox['yscrollcommand'] = scrollbarTest.set
    #scrollbarTest.pack(padx=20,pady=75,side=LEFT, expand=TRUE, fill=Y)
    scrollbarTest.place(x=520, y=80, width=10, height=500)

    myResList = os.listdir(Global_Setting_Var.ParentDirResu)
    myResListBox = Listbox(startupform, height=10, selectmode=MULTIPLE)
    #myResListBox.pack(padx=20,pady=150, expand=TRUE, fill=BOTH, side=RIGHT)
    #myResListDocBox = Listbox(startupform, height=10, selectmode=MULTIPLE)
    myResListBox.place(x=750, y=80, width=500, height=500)

    scrollbarRes = Scrollbar(startupform, orient=VERTICAL, command=myResListBox.yview)
    myResListBox['yscrollcommand'] = scrollbarRes.set
    #scrollbarRes.pack(padx=20,pady=75,side=RIGHT, expand=TRUE, fill=Y)
    scrollbarRes.place(x=1270, y=80, width=10, height=500)



    def ts_to_dt(ts):
        date_time = datetime.datetime.fromtimestamp(ts)
        str_date_time = date_time.strftime(" %d-%m-%y, %H:%M")
        return str_date_time

    #created by list box of the tests sorted by time
    testlist =[]
    for file in myTestList:
        if not("." in file):
            i = (os.path.getctime(Global_Setting_Var.ParentDirTest+file), file)
            testlist.append(i)
    testlist.sort(reverse=TRUE,key=lambda x: x[0])

    for i in range(len(testlist)):
        fulldata = str(ts_to_dt(testlist[i][0])) + "    " + testlist[i][1]
        myTestListBox.insert(END, fulldata)

    # created by list box of the tests resualt  sorted by time
    ResList = []
    for Resfile in myResList:
        if not("." in Resfile):
            i = (os.path.getctime(Global_Setting_Var.ParentDirResu+Resfile), Resfile)
            ResList.append(i)
    ResList.sort(reverse=TRUE,key=lambda x: x[0])

    for i in range(len(ResList)):
        fulldata = str(ts_to_dt(ResList[i][0])) + "    " + ResList[i][1]
        myResListBox.insert(END, fulldata)



    def createTest():
        Global_Setting_Var.userSellector = 1
        startupform.destroy()

    def clearLoogger():
        text_widget.delete('1.0', tk.END)
        with open((Global_Setting_Var.ParentDirResu + "/currentresult.txt"), 'w') as file:
            pass
        with open(Global_Setting_Var.ParentDirResu + "/currentresult.txt") as file:
            content = file.read()
            text_widget.insert(tk.END, content)
            # Insert new content
            new_content = "Report review was deleted."
            text_widget.insert(tk.END, new_content)


    def presentpreview(event):
        # Get the index of the clicked position
        index = text_widget.index(tk.CURRENT)

        # Find the start and end indices of the current line
        line_start = text_widget.index(f"{index} linestart")
        line_end = text_widget.index(f"{index} lineend")

        # Get the raw data of the entire line
        raw_line_data = text_widget.get(line_start, line_end)
        stepname = raw_line_data.split(' ')
        folderName = stepname[0][1:]
        fileName = stepname[9][1:-4]
        Diffimage_path = (Global_Setting_Var.ParentDirResu + folderName + "/" + fileName+"_N_Diff.jpg")
        Cutimage_path = (Global_Setting_Var.ParentDirResu + folderName + "/" + fileName+ "_Cut.jpg")
        concatenate_path = (Global_Setting_Var.ParentDirResu + folderName + "/" + "concatenate.jpg")

        ImageProcess.concatenate_images_vertically(Diffimage_path,Cutimage_path,concatenate_path)

        # Use the default associated program to open the file
        try:
            os.startfile(concatenate_path)
        except FileNotFoundError:
            messagebox.showinfo("Error", "the DIff file and \ or the cut file weren't found .")
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")



    def runTests():
        Global_Setting_Var.userSellector = 2
        selected_indices = myTestListBox.curselection()
        tempList = []
        for i in selected_indices:
            t_selected = myTestListBox.get(i).split(" ")[-1:]
            tempList = tempList + t_selected

        selected = ",".join(tempList)
        #selected = ",".join([myTestListBox.get(i).split(" ")[-1:].sp for i in selected_indices])
        if selected !="":
            crteateFile(selected)
            startupform.destroy()
        else:
            messagebox.showinfo('Auto Test', 'you need to define at least one test')

    def reportATP():
        T = date.today().strftime("%B%d%Y")
        fileName = Global_Setting_Var.docFolder + "\ATP_" + str(T)+".docx"
        CreateDoc.createDocx(myTestListBox,"ATP",fileName)

    def reportATR():
        T = date.today().strftime("%B%d%Y")
        fileName = Global_Setting_Var.docFolder + "\ATR_" + str(T) + ".docx"
        CreateDoc.createDocx(myResListBox, "ATR", fileName)

    def DuplicateTest():
        getNewtestName(myTestListBox)
    def UpdatePic():
        UpdateImages.copy_jpg_files(myResListBox)

    def close():
        Global_Setting_Var.userSellector = 0
        startupform.destroy()
        sys.exit()

    def crteateFile(string):
        TestLog = open(Global_Setting_Var.TestListF, "w")  # open the test list
        TestLog.write(
            "# this file contain the list of Test_Name (similar name to the one in test folder). Add space + ""Test"" after the test name \n")
        TestList = string.split(',')
        for i in range(len(TestList)):
            TestLog.write(TestList[i] + " Test\n")
        TestLog.write("*********************************************EOF**************************************\n")
        TestLog.close()

    def PicStatus():
       PicStatus = var_doc.get()
       Global_Setting_Var.PicOption= PicStatus
       #print(Global_Setting_Var.PicOption)

    def set_scroll_to_end():
        text_widget.insert("end", "---------->\n")
        text_widget.see("end")

    # placing the widgets at respective positions in table like structure .
    createButon = Button(startupform, text="Create", fg='green',  height=1, width=12, command=createTest)
    createButon.place(x=580, y= 120)

    # placing the widgets at respective positions in table like structure .
    runButton = Button(startupform, text="Run",  fg='green', height=1, width=12, command=runTests)
    runButton.place(x=580, y= 180)

    # placing the widgets at respective positions in table like structure .
    reportATPButton = Button(startupform, text="ATP",  fg='blue', height=1, width=12, command=reportATP)
    reportATPButton.place(x=580, y= 280)

    # placing the widgets at respective positions in table like structure .
    reportATRButton = Button(startupform, text="ATR",  fg='blue', height=1, width=12, command=reportATR)
    reportATRButton.place(x=580, y= 340)

    DuplicateTestButton = Button(startupform, text="Duplicate Test",  fg='black', height=1, width=12, command=DuplicateTest)
    DuplicateTestButton.place(x=580, y= 480)

    UpdatePicButton = Button(startupform, text="Update Pic",  fg='black', height=1, width=12, command=UpdatePic)
    UpdatePicButton.place(x=580, y= 540)

    # placing the widgets at respective positions in table like structure .
    closeButton = Button(startupform, text="Close",  fg='red', height=1, width=12, command=close)
    closeButton.place(x=580, y= 620)

    # placing the widgets at respective positions in table like structure .
    clearLooggerButton = Button(startupform, text="Clear",  fg='red', height=1, width=12, command=clearLoogger)
    clearLooggerButton.place(x=1100, y= 750)

    var_doc = IntVar()

    R1 = Radiobutton(startupform, text="0-Pic",  variable=var_doc, value=0, command=PicStatus)
    R1.place(x=600, y= 410)

    R1 = Radiobutton(startupform, text="1-Pic", variable=var_doc, value=1, command=PicStatus)
    R1.place(x=550, y= 440)

    R1 = Radiobutton(startupform, text="2-Pic", variable=var_doc, value=2, command=PicStatus)
    R1.place(x=670, y= 440)


    startupform_ReportLabel = Label(startupform, text="Report Viewer - click on the step to open review ")
    startupform_ReportLabel.place(x=50, y=660)

    text_widget = tk.Text(startupform, wrap="word", width=120, height=10)
    text_widget.place(x=50, y=700, width= 1000, height= 210)
    text_widget.bind("<Button-1>", presentpreview)

    scrollbartext_widget = Scrollbar(startupform, orient=VERTICAL, command=text_widget.yview)
    text_widget['yscrollcommand'] = scrollbartext_widget.set
    scrollbartext_widget.place(x=1070, y=700, width=20, height=195)

    with open(Global_Setting_Var.ParentDirResu + "/currentresult.txt", 'r') as file:
        content = file.read()
        text_widget.insert(tk.END, content)

    set_scroll_to_end()

    # Bind the on_close function to the window close event
    startupform.protocol("WM_DELETE_WINDOW", close)

    startupform.mainloop()

    return (Global_Setting_Var.userSellector)


def endmsg():

    messagebox.showinfo('Auto Test', 'End of procedure')

def main():
    print("Runing DataWindow.py directly")

if __name__ == "__main__":
    main()

