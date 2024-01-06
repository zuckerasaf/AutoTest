import os
import shutil
import time
from tkinter import messagebox

import tkinter as tk
from tkinter import simpledialog
import Global_Setting_Var
from Util import *
import DataWindow

def replace_string_in_file(file_path, old_string, new_string):
    try:
        # Read the contents of the file
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Replace the old string with the new string
        updated_content = file_content.replace(old_string, new_string)

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)

    except Exception as e:
        messagebox.showinfo('Auto Test',
                            f"Error replacing string in {file_path} file:  {e}")
        #print(f"Error replacing string in file: {e}")

def changeFilesName(directory_path,string_to_find, replacement_string):
    # Iterate through the files in the directory
    for filename in os.listdir(directory_path):
        if string_to_find in filename:
            # Construct the new filename with the replacement string
            new_filename = filename.replace(string_to_find, replacement_string)

            # Create the full paths for the old and new filenames
            old_filepath = os.path.join(directory_path, filename)
            new_filepath = os.path.join(directory_path, new_filename)

            # Rename the file
            os.rename(old_filepath, new_filepath)
            #print(f'Renamed: {filename} to {new_filename}')

def duplicate_folder(src, dst):

    fNames=os.listdir(src)

    if not os.path.exists(dst):
        os.makedirs(dst)

    try:
        for fNames in fNames:
            source_path = os.path.join(src, fNames)
            destination_path = os.path.join(dst, fNames)

            # Copy and replace the file
            shutil.copy2(source_path, destination_path)



    except Exception as e:
        messagebox.showinfo('Auto Test', f"Error duplicating folder, make sure the name is stand for the windows file name style: {e}")


def open_input_window(RSN):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Get user input User Input - new test name
    user_input = simpledialog.askstring("Input", "Enter new Test Name \t\t\t\t ", initialvalue=RSN)

    # Display the user input or the default string
    result = user_input if user_input else RSN
    # print("User input:", result)
    if user_input is None:
        result = "cancel"

    return result


def getNewtestName(source_folder):
    selected_indices = source_folder.curselection()

    #envirument = source_folder.split("/")[-1].split("_")[-1]
    NewName = ""

    # check the user enter any test or report to the final report
    if selected_indices.__len__() != 1:
        messagebox.showinfo('Auto Test', 'you need to define one test')
        return


    selected = ",".join([source_folder.get(i).split(" ")[-1] for i in selected_indices])

    # remove the environment suffix from of the name (IOS web, Desktop, none)
    if "_IOS_WEB" in (selected):
        text=selected.replace("_IOS_WEB","")
    elif "_Desktop" in (selected):
        text = selected.replace("_Desktop","")
    else:
        text=selected
    RandScenrioName = text + "_" + CreateRandTestName(Global_Setting_Var.RSN).replace(":", "")
    NewName = open_input_window(RandScenrioName)

    # add the environment suffix to  the name (IOS web, Desktop, none)

    if "IOS_WEB"in(selected):
        NewName = NewName + "_IOS_WEB"
    elif "Desktop"in(selected):
        NewName = NewName + "_Desktop"
    else:
        NewName = NewName


    if NewName == "cancel":
        return

    source_folder = Global_Setting_Var.ParentDirTest + selected
    #print(source_folder)
    destination_folder = Global_Setting_Var.ParentDirTest + NewName
    #print(destination_folder)

    # Ensure the Traget folder doesnt exists
    if os.path.exists(destination_folder):
        messagebox.showinfo('Auto Test', 'you can not use existing name ')
        return
    #
    duplicate_folder(source_folder, destination_folder)

    changeFilesName(destination_folder,selected,NewName)

    ATPfile = destination_folder + "/" + NewName +"_ATP.txt"

    replace_string_in_file(ATPfile,selected,NewName)

    Data_win1 = gw.getWindowsWithTitle('Auto Test start up')[0]
    Data_win1.close()

    runMainAutoScript()

    #
    #
    # messagebox.showinfo('Auto Test', f"Folder '{selected}' successfully duplicated to '{NewName}'.")
    #

