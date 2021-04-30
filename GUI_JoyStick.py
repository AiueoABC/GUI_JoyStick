import PySimpleGUI as sg
import math
import threading
# sg.ChangeLookAndFeel('grey')


class JoyStick:
    def __init__(self):
        threading.Thread.__init__(self)
        layout = [
            [sg.Graph(canvas_size=(500, 500), graph_bottom_left=(0,0), graph_top_right=(500, 500), change_submits=True,
                      drag_submits=True, key='graph')],
            [sg.Text('X-Y Coordinates: (0, 0)        ', key='-xy-')],
            [sg.Text('r-θ Coordinates: (0, 0)        ', key='-rt-')]
        ]
        window = sg.Window('JoyStick', layout, finalize=True)
        self.__window = window
        self.__graph = window['graph']
        cir = self.__graph.DrawOval((0, 0), (500, 500))
        cir_half = self.__graph.DrawOval((125, 125), (375, 375))
        self.__cir_joy = self.__graph.DrawOval((240, 240), (260, 260))
        self.__cir_joy_pos = (250, 250)
        line_x = self.__graph.DrawLine((0, 250), (500, 250))
        line_y = self.__graph.DrawLine((250, 0), (250, 500))
        self.__graph.TKCanvas.itemconfig(cir, fill="white")
        self.__graph.TKCanvas.itemconfig(self.__cir_joy, fill="cyan")
        self.xy_coordinates = [0, 0]
        self.rt_coordinates = [0, 0]

    def __joy_pos_setter(self, x_togo, y_togo):
        posx, posy = self.__cir_joy_pos
        dx = x_togo - posx
        dy = y_togo - posy
        self.__graph.MoveFigure(self.__cir_joy, dx, dy)
        self.__cir_joy_pos = (x_togo, y_togo)

    def __show_coordinates(self, position):
        self.xy_coordinates = position[0] - 250, position[1] - 250
        self.rt_coordinates = (self.xy_coordinates[0] ** 2 + self.xy_coordinates[1] ** 2) ** 0.5, \
                              math.atan2(self.xy_coordinates[1], self.xy_coordinates[0])

    def run(self):
        while True:
            event, values = self.__window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'graph+UP':
                self.__joy_pos_setter(250, 250)
                self.__window['-xy-'].update(f'X-Y Coordinates: (0, 0)')
                self.__window['-rt-'].update(f'r-θ Coordinates: (0, 0)')
            elif event == 'graph':
                position = values['graph']
                self.__joy_pos_setter(position[0], position[1])
                self.__show_coordinates(position)
                text1 = f'X-Y Coordinates: ' \
                        f'({self.xy_coordinates[0]}, {self.xy_coordinates[1]})'
                text2 = f'r-θ Coordinates: ' \
                        f'({int(self.rt_coordinates[0])}, {int(180 * self.rt_coordinates[1] / math.pi)})'
                self.__window['-xy-'].update(text1)
                self.__window['-rt-'].update(text2)


if __name__ == '__main__':
    js = JoyStick()
    js.run()
