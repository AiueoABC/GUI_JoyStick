import PySimpleGUI as sg
import math
import GUI_JoyStick

js = GUI_JoyStick.JoyStick()

layout = [
    [sg.Graph(canvas_size=(750, 750),
              graph_bottom_left=(0, 0),
              graph_top_right=(750, 750),
              change_submits=True,
              drag_submits=True,
              key='graph')],
    [sg.Button('BACK TO THE CENTER'),
     sg.Text('RobotRotation:                    ', key='rotation'),
     sg.Text('RobotTheta:                    ', key='theta')],
]

window = sg.Window('SmallRobotExample', layout, finalize=True)
graph = window['graph']

robotwidth = 20
robotlength = 30
robotcenter = (375, 375)
robotleftcenter = (robotcenter[0] - robotwidth / 2, robotcenter[1])
robotrightcenter = (robotcenter[0] + robotwidth / 2, robotcenter[1])
robotrotation = 0

mainBody = graph.DrawLine(robotleftcenter, robotrightcenter, color='cyan', width=10)
leftBody = graph.DrawLine(robotleftcenter, (robotleftcenter[0], robotleftcenter[1] + robotlength), color='cyan', width=3)
rightBody = graph.DrawLine(robotrightcenter, (robotrightcenter[0], robotrightcenter[1] + robotlength), color='cyan', width=3)
reddot = graph.DrawPoint((robotcenter[0], robotcenter[1] + robotlength), size=robotwidth, color='red')


def cmdcontrol(l_value, r_value, k=0.3):
    global robotleftcenter, robotrightcenter, robotcenter, robotrotation, mainBody, leftBody, rightBody, reddot
    l_dl, r_dl = l_value * k / 99, r_value * k / 99
    theta = (r_dl - l_dl) / robotwidth
    t = '{:.5f}'.format(theta)
    window['theta'].update(f'RobotTheta: {t}')
    if -0.001 <= theta <= 0.001:
        if l_value == 0. or r_value == 0.:
            pass
        else:
            l_dx, l_dy = l_dl * (-math.sin(robotrotation)), l_dl * math.cos(robotrotation)
            graph.MoveFigure(leftBody, l_dx, l_dy)
            graph.MoveFigure(rightBody, l_dx, l_dy)
            graph.MoveFigure(mainBody, l_dx, l_dy)
            graph.MoveFigure(reddot, l_dx, l_dy)
            robotleftcenter = l_dx + robotleftcenter[0], l_dy + robotleftcenter[1]
            robotrightcenter = l_dx + robotrightcenter[0], l_dy + robotrightcenter[1]
            robotcenter = (robotleftcenter[0] + robotrightcenter[0]) / 2, (robotleftcenter[1] + robotrightcenter[1]) / 2

    else:
        robotrotation = robotrotation + theta
        if abs(r_value) >= abs(l_value):
            origin = robotleftcenter[0] + (robotleftcenter[0] - robotrightcenter[0]) * l_value / (r_value - l_value), \
                     robotleftcenter[1] + (robotleftcenter[1] - robotrightcenter[1]) * l_value / (r_value - l_value)
        else:
            origin = robotrightcenter[0] + (robotrightcenter[0] - robotleftcenter[0]) * r_value / (l_value - r_value), \
                     robotrightcenter[1] + (robotrightcenter[1] - robotleftcenter[1]) * r_value / (l_value - r_value)

        robotleftcenter = (robotleftcenter[0] - origin[0]) * math.cos(theta) - \
                          (robotleftcenter[1] - origin[1]) * math.sin(theta) + origin[0], \
                          (robotleftcenter[0] - origin[0]) * math.sin(theta) + \
                          (robotleftcenter[1] - origin[1]) * math.cos(theta) + origin[1]
        robotrightcenter = (robotrightcenter[0] - origin[0]) * math.cos(theta) - \
                           (robotrightcenter[1] - origin[1]) * math.sin(theta) + origin[0], \
                           (robotrightcenter[0] - origin[0]) * math.sin(theta) + \
                           (robotrightcenter[1] - origin[1]) * math.cos(theta) + origin[1]
        robotcenter = (robotleftcenter[0] + robotrightcenter[0]) / 2, (robotleftcenter[1] + robotrightcenter[1]) / 2
        dx_top, dy_top = - robotlength * math.sin(robotrotation), robotlength * math.cos(robotrotation)
        # rewrite robot
        graph.erase()
        mainBody = graph.DrawLine(robotleftcenter, robotrightcenter, color='cyan', width=10)
        leftBody = graph.DrawLine(robotleftcenter,
                                  (robotleftcenter[0] + dx_top, robotleftcenter[1] + dy_top),
                                  color='cyan', width=3)
        rightBody = graph.DrawLine(robotrightcenter,
                                   (robotrightcenter[0] + dx_top, robotrightcenter[1] + dy_top),
                                   color='cyan', width=3)
        reddot = graph.DrawPoint((robotcenter[0] + dx_top, robotcenter[1] + dy_top), size=robotwidth, color='red')


def calculate_lrPow(r, theta):
    pow_level = r * 99 / 250
    rot = math.cos(theta)
    lin = math.sin(theta)
    lPow = int((rot + lin) * pow_level)
    rPow = int((-rot + lin) * pow_level)
    lPow = 99 if lPow > 99 else -99 if lPow < -99 else lPow
    rPow = 99 if rPow > 99 else -99 if rPow < -99 else rPow
    return (lPow, rPow)


if __name__ == '__main__':
    dotmode = False
    automove = False
    dots = []
    while True:
        js.update()
        rt = js.rt_coordinates
        cmd = calculate_lrPow(rt[0], rt[1])
        cmdcontrol(cmd[0], cmd[1], k=1)
        event, values = window.read(timeout=1)
        rot = '{:.3f}'.format(robotrotation)
        window['rotation'].update(f'RobotRotation: {rot}')
        if event == sg.WIN_CLOSED:
            break
        elif event == 'BACK TO THE CENTER':
            robotcenter = (375, 375)
            robotleftcenter = (robotcenter[0] - robotwidth / 2, robotcenter[1])
            robotrightcenter = (robotcenter[0] + robotwidth / 2, robotcenter[1])
            robotrotation = 0
            # rewrite robot
            graph.erase()
            mainBody = graph.DrawLine(robotleftcenter, robotrightcenter, color='cyan', width=10)
            leftBody = graph.DrawLine(robotleftcenter, (robotleftcenter[0], robotleftcenter[1] + robotlength),
                                      color='cyan', width=3)
            rightBody = graph.DrawLine(robotrightcenter, (robotrightcenter[0], robotrightcenter[1] + robotlength),
                                       color='cyan', width=3)
            reddot = graph.DrawPoint((robotcenter[0], robotcenter[1] + robotlength), size=robotwidth, color='red')

        if js.close:
            break

    window.close()
