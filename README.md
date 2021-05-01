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
In this case, `js.xy_coordinates` has (X [pxls], Y [pxls]) data, and `js.rt_coordinates` has (r [pxls], theta [rad]) data.

# Example
This is an example to generate a cmd to control 2 wheels, left and right wheels, vehicle.  
To do this, we need to tell directions and powers to apply for both wheels.  
Run below to check how it works;  
```
python ./example/ControlCrawlerMotor.py
```

# HELP WANTED
I need your support, pls feed me.  
<a href="https://www.buymeacoffee.com/aiueoabc" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
