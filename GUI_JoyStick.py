import PySimpleGUI as sg
import math


class JoyStick:
    def __init__(self, r_max=250, stick_size=20):
        self.r_max = r_max
        self.stick_size = stick_size
        size = int(self.stick_size / 2)
        layout = [
            [sg.Graph(canvas_size=(2 * self.r_max, 2 * self.r_max),
                      graph_bottom_left=(0, 0),
                      graph_top_right=(2 * self.r_max, 2 * self.r_max),
                      change_submits=True,
                      drag_submits=True,
                      key='graph')],
            [sg.Text('X-Y Coordinates: (0, 0)        ', key='-xy-')],
            [sg.Text('r-θ Coordinates: (0, 0)        ', key='-rt-')]
        ]
        window = sg.Window('JoyStick', layout, finalize=True)
        self.__window = window
        self.__graph = window['graph']
        cir = self.__graph.DrawOval((0, 0), (2 * self.r_max, 2 * self.r_max))
        self.__graph.DrawOval((int(self.r_max / 2), int(self.r_max / 2)),
                              (int(self.r_max * 3 / 2), int(self.r_max * 3 / 2)))
        self.__cir_joy = self.__graph.DrawOval((self.r_max - size, self.r_max - size),
                                               (self.r_max + size, self.r_max + size))
        self.__cir_joy_pos = (self.r_max, self.r_max)
        self.__graph.DrawLine((0, self.r_max), (self.r_max * 2, self.r_max))
        self.__graph.DrawLine((self.r_max, 0), (self.r_max, self.r_max * 2))
        self.__graph.TKCanvas.itemconfig(cir, fill="white")
        self.__graph.TKCanvas.itemconfig(self.__cir_joy, fill="cyan")
        self.close = False
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
            self.update()
            if self.close:
                break

    def update(self):
        event, values = self.__window.read()
        if event == sg.WIN_CLOSED:
            self.close = True
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
