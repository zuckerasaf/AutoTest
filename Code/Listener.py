import pyautogui
import runTest
import time
import Global_Setting_Var
from pynput.keyboard import Key

# input:
#   x = integer - mouse X location
#   y = integer - mouse Y location
#   button = string - type of button
#   press = bool - press= true , release = false
# what does it do: write the "file" the mouse location + button type + if press or release with running time
# output: none
def Listener_mouse_click(x, y, button, pressed, starttime, filepoinetr):

    if pressed:
        #total_time = round((time.time() - starttime), 2)
        total_time = time.time() - starttime
        gap_time = round(total_time - Global_Setting_Var.Lasttime,4)
        filepoinetr.writelines(str(gap_time) + ' mouse down at ({0},{1}) with {2} \n'.format(x, y, button))

    if not pressed:
        #total_time = round((time.time() - starttime), 2)
        total_time = time.time() - starttime
        gap_time = round(total_time - Global_Setting_Var.Lasttime,4)
        filepoinetr.writelines(str(gap_time) + ' mouse up at ({0},{1}) with {2} \n'.format(x, y, button))

    Global_Setting_Var.Lasttime  = total_time

# input:
#   x = integer - mouse X location
#   y = integer - mouse Y location
#   dx = integer - number of click in scroll
#   dy = integer - scroll direction 1 = up , -1 = down  with running time
# what does it do: write the "file" the mouse scroll operation
# output: none
def Listener_mouse_scroll(x, y, dx, dy,starttime, filepoinetr):
    #total_time = round((time.time() - starttime), 2)
    total_time = time.time() - starttime
    gap_time = round(total_time - Global_Setting_Var.Lasttime, 4)
    filepoinetr.writelines(str(gap_time) + ' scrolled at ({0},{1}), ({2},{3}) \n'.format(x, y, dx, dy))
    Global_Setting_Var.Lasttime = total_time

# input: key = string - keyboard mouse X operation
# what does it do: in case ESC was p press change the Global_Setting_Var.terminate to 1 else
# write the "ATRLogfilePointer" the keyboard click with running time output: none
def Listener_keyboard_press(key,starttime, filepoinetr):


    #total_time = round((time.time() -starttime), 2)
    total_time = time.time() - starttime
    gap_time = round(total_time - Global_Setting_Var.Lasttime, 4)
    filepoinetr.writelines(str(gap_time) + ' keyboard pressed with {0} \n'.format(key))
    Global_Setting_Var.Lasttime = total_time

