import math
from GUI_JoyStick import GUI_JoyStick

'''
To control 2 motors for 2 crawlers, this example will generate a cmd to control them.
In this example, cmd will be like "L+00R+00e", where 
"L+00" indicates power and direction of left crawler, 
"R+00" indicates power and direction of right crawler, and
"e" indicates terminator of cmd.
This format can be useful when you want to use serial communication and udp communication.
'''

cmd = "L+00R+00e"  # Range of power is from -99 to +99 for each L and R.
lPow = 0
rPow = 0


def calculate_lrPow(r, theta):
    pow_level = r * 99 / 250
    rot = math.cos(theta)
    lin = math.sin(theta)
    lPow = int((rot + lin) * pow_level)
    rPow = int((-rot + lin) * pow_level)
    lPow = 99 if lPow > 99 else -99 if lPow < -99 else lPow
    lcmd = f'+{str(lPow).zfill(2)}' if lPow >= 0 else f'{str(lPow).zfill(3)}'
    rPow = 99 if rPow > 99 else -99 if rPow < -99 else rPow
    rcmd = f'+{str(rPow).zfill(2)}' if rPow >= 0 else f'{str(rPow).zfill(3)}'
    cmd = f'L{lcmd}R{rcmd}e'
    return cmd


js = GUI_JoyStick.JoyStick()

while not js.close:
    js.update()
    rt = js.rt_coordinates
    cmd = calculate_lrPow(rt[0], rt[1])
    print(cmd)
    "It's easy to send this cmd via serial communication"
