# GUI_JoyStick
Simple GUI JoyStick using PySimpleGUI.

# How To Use
Make sure you have installed PySimpleGUI in your Python3.  
To check, simply run `python GUI_JoyStick.py`

To use coordinates in your own code, do like following;  
```
import GUI_JoyStick

js = GUI_JoyStick.JoyStick()

while True:
    js.update()
    print(js.xy_coordinates)
    print(js.rt_coordinates)
    
    if js.close:
        break
```
