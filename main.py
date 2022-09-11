from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

from kivymd.app import MDApp
from kivymd.toast.kivytoast.kivytoast import toast

from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.base import EventLoop
from kivy.graphics import Color, Rectangle

from functools import partial
from copy import deepcopy as copy
from time import sleep
from threading import Thread
from cube import Cube


INPUT_CUBE = []
INPUT = [False, False]


class MainWindow(Screen):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        def add_btn(btn_id, text="", bg=(1,1,1,.7)):
            btn = Button(text=text,
                         size_hint=(None, None),
                         background_normal='',
                         background_down=''
                         )
            self.ids[btn_id] = btn
            self.add_widget(btn)

        def get_btn(text):
            return Button(text=text,
                          font_size=30,
                          size_hint=(None, None),
                          background_normal='',
                          background_down='',
                          background_color=(0,0,0,1)
                          )

        self.cube = Cube()

        with self.canvas.before:
            Color(.3, .3, .3, 1)
            Rectangle(size=(1280, 720), pos=(0, 0))

        for i in range(54):
            add_btn(i)

        self.reset_btn = get_btn("Reset")
        self.input_btn = get_btn("Input")
        self.solve_btn = get_btn("Solve")
        self.random_btn = get_btn("Random Cube")

        for i in range(9):
            self.ids[i].background_color = (0, 1, 0, 1)
            self.ids[45 + i].background_color = (0, 0, 1, 1)

        colors = [(1,0,0,1), (1,1,1,1), (1,165/255,0,1), (1,1,0,1)]
        for i in range(36):
            self.ids[9 + i].background_color = colors[(i % 12) // 3]

        self.reset_btn.bind(on_release=self.reset)
        self.input_btn.bind(on_release=self.change_screen)
        self.solve_btn.bind(on_release=self.solve)
        self.random_btn.bind(on_release=self.random)
        self.add_widget(self.reset_btn)
        self.add_widget(self.input_btn)
        self.add_widget(self.solve_btn)
        self.add_widget(self.random_btn)
        self.update_cube()

        self.bind(pos=self.update, size=self.update)

    def update_cube(self):
        l = copy(self.cube.cube['L'])
        f = copy(self.cube.cube['F'])
        u = copy(self.cube.cube['U'])
        d = copy(self.cube.cube['D'])
        r = copy(self.cube.cube['R'])

        self.cube.B()
        self.cube.B()
        b = copy(self.cube.cube['B'])
        self.cube.B_()
        self.cube.B_()

        colors = {2: (1, 0, 0, 1),
                  4: (0, 0, 1, 1),
                  0: (1, 1, 1, 1),
                  1: (0, 1, 0, 1),
                  3: (1, 165 / 255, 0, 1),
                  5: (1, 1, 0, 1)}

        for i in range(3):
            for j in range(3):
                self.ids[j + (i * 3)].background_color = colors[u[i][j]]
                self.ids[9 + j + (i * 12)].background_color = colors[l[i][j]]
                self.ids[12 + j + (i * 12)].background_color = colors[f[i][j]]
                self.ids[15 + j + (i * 12)].background_color = colors[r[i][j]]
                self.ids[18 + j + (i * 12)].background_color = colors[b[i][j]]
                self.ids[45 + j + (i * 3)].background_color = colors[d[i][j]]

    def rotate(self, side, *args):
        self.cube.rotate(side)
        self.update_cube()

    def random(self, *args):
        self.cube.generate_random_cube()
        self.update_cube()

    def reset(self, *args):
        self.cube.reset()
        self.update_cube()

    def change_screen(self, *args):
        self.reset(None)
        Thread(target=self.wait).start()
        self.manager.current = 'input'

    def wait(self):
        global INPUT
        INPUT = [False, False]
        while not INPUT[0]:
            sleep(0.01)
        if INPUT[1]:
            for i, j in enumerate("FULRDB"):
                self.cube.cube[j] = INPUT_CUBE[i]
            self.update_cube()

    def solve(self, *args):
        if self.cube.cube == {'F': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                              'U': [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                              'L': [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
                              'R': [[3, 3, 3], [3, 3, 3], [3, 3, 3]],
                              'D': [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
                              'B': [[5, 5, 5], [5, 5, 5], [5, 5, 5]]}:
            return
        scrambled = copy(self.cube.cube)
        rotations = copy(self.cube.solve())
        self.cube.cube = scrambled

        Thread(target=self.solve_thread, args=(rotations,)).start()

    def solve_thread(self, rotations):
        direction = {1: 'F', -1: 'F_',
                     2: 'U', -2: 'U_',
                     3: 'L', -3: 'L_',
                     4: 'R', -4: 'R_',
                     5: 'D', -5: 'D_',
                     6: 'B', -6: 'B_'}
        t = 0.0075
        for i in rotations:
            self.cube.rotate(direction[i])
            self.update_cube()
            sleep(t)

    def update(self, *args):
        self.solve_btn.size = (250, 60)
        self.solve_btn.pos = (950, 280)
        self.random_btn.size = (250, 60)
        self.random_btn.pos = (950, 200)
        self.input_btn.size = (250, 60)
        self.input_btn.pos = (950, 120)
        self.reset_btn.size = (250, 60)
        self.reset_btn.pos = (950, 40)

        b = 65
        s1 = 30 + b*3 + 12
        s2 = 30
        h = 600

        for i in range(54):
            self.ids[i].size = (b, b)

        n = 0
        for i in range(3):
            for j in range(3):
                self.ids[n].pos = (s1 + ((b + 3) * j), h)
                n += 1
            h -= b + 3
        h -= 3

        for i in range(3):
            t = 0
            for j in range(12):
                if j % 3 == 0 and j != 0:
                    t += 3
                self.ids[n].pos = (s2 + ((b + 3) * j) + t, h)
                n += 1
            h -= b + 3
        h -= 3

        for i in range(3):
            for j in range(3):
                self.ids[n].pos = (s1 + ((b + 3) * j), h)
                n += 1
            h -= b + 3


class InputWindow(Screen):
    def __init__(self, **kwargs):
        super(InputWindow, self).__init__(**kwargs)

        def add_btn(func, btn_id, text="", bg=(1,1,1,.7)):
            btn = Button(text=text,
                         font_size=35,
                         color=(0,0,0,1),
                         size_hint=(None, None),
                         background_normal='',
                         background_down='',
                         background_color=bg
                         )
            btn.bind(on_press=partial(func, btn_id))
            self.ids[btn_id] = btn
            self.add_widget(btn)

        with self.canvas.before:
            Color(.3, .3, .3, 1)
            Rectangle(size=(1280, 720), pos=(0, 0))

        with self.canvas.after:
            Color(0,0,0,.4)
            self.pointer = Rectangle()

        self.original_cube = []
        self.pre_clicked = 0
        self.fixed = {4: (0, 1, 0, 1),  # GREEN
                      22: (1, 0, 0, 1),  # RED
                      25: (1, 1, 1, 1),  # WHITE
                      28: (1, 165 / 255, 0, 1),  # ORANGE
                      31: (1, 1, 0, 1),  # YELLOW
                      49: (0, 0, 1, 1)}  # BLUE

        for i in range(54):
            add_btn(func=self.clicked, btn_id=i)

        keys = {4: 'G', 22: 'R', 25: 'W', 28: 'O', 31: 'Y', 49: 'B'}
        for i in self.fixed:
            self.ids[i].background_color = self.fixed[i]
            add_btn(self.get_color, str(i), keys[i], self.fixed[i])

        self.reset_btn = Button(text="Reset",
                                font_size=30,
                                size_hint=(None, None),
                                background_normal='',
                                background_down='',
                                background_color=(0,0,0,1)
                                )

        self.done_btn = Button(text="Done",
                               font_size=30,
                               size_hint=(None, None),
                               background_normal='',
                               background_down='',
                               background_color=(0,0,0,1)
                               )

        self.reset_btn.bind(on_release=self.reset)
        self.done_btn.bind(on_release=self.done)
        self.add_widget(self.reset_btn)
        self.add_widget(self.done_btn)

        self.bind(pos=self.update, size=self.update)

    def on_pre_enter(self, *args):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *args):
        if self.manager.current != 'input':
            return True

        colors = {98: (0, 0, 1, 1), 103: (0, 1, 0, 1), 111: (1, 165/255, 0, 1),
                  114: (1, 0, 0, 1), 119: (1, 1, 1, 1), 121: (1, 1, 0, 1)}
        if key in colors:
            self.ids[self.pre_clicked].background_color = colors[key]

        if key == 27 or key == 8:
            global INPUT
            INPUT[0] = True
            self.manager.current = 'main'
            return True

        if key == 13:
            return self.done()

        if key == 276:  # LEFT
            if self.pre_clicked > 0:
                self.pre_clicked -= 1
                if self.pre_clicked in self.fixed:
                    self.pre_clicked -= 1
        elif key == 275:  # RIGHT
            if self.pre_clicked < 53:
                self.pre_clicked += 1
                if self.pre_clicked in self.fixed:
                    self.pre_clicked += 1
        elif key == 273:  # UP
            if self.pre_clicked > 2:
                if 44 < self.pre_clicked <= 47:
                    self.pre_clicked -= 9
                elif 20 < self.pre_clicked < 47:
                    self.pre_clicked -= 12
                    if self.pre_clicked in self.fixed:
                        self.pre_clicked -= 12
                elif 8 < self.pre_clicked < 13:
                    self.pre_clicked = 6
                elif self.pre_clicked == 13:
                    self.pre_clicked = 7
                elif 13 < self.pre_clicked < 21:
                    self.pre_clicked = 8
                else:
                    self.pre_clicked -= 3
                    if self.pre_clicked in self.fixed:
                        self.pre_clicked -= 3
        elif key == 274:  # DOWN
            if self.pre_clicked < 51:
                if 5 < self.pre_clicked <= 8:
                    self.pre_clicked += 6
                elif 8 < self.pre_clicked <= 32:
                    self.pre_clicked += 12
                    if self.pre_clicked in self.fixed:
                        self.pre_clicked += 12
                elif 32 < self.pre_clicked < 37:
                    self.pre_clicked = 45
                elif self.pre_clicked == 37:
                    self.pre_clicked = 46
                elif 37 < self.pre_clicked < 45:
                    self.pre_clicked = 47
                else:
                    self.pre_clicked += 3
                    if self.pre_clicked in self.fixed:
                        self.pre_clicked += 3

        self.pointer.pos = self.ids[self.pre_clicked].pos

    def clicked(self, index, instance):
        if index in self.fixed:
            return
        self.pre_clicked = index
        self.pointer.pos = self.ids[self.pre_clicked].pos

    def get_color(self, n, instance):
        self.ids[self.pre_clicked].background_color = self.fixed[int(n)]

    def done(self, *args):
        colors = [''.join(str(k) for k in self.ids[x].background_color) for x in range(54)]
        if '1110.7' in colors:
            toast("Enter All Colors", background=[0,0,0,1])
            return True
        counts = {}
        for i in colors:
            if i in counts:
                counts[i] += 1
            else:
                counts[i] = 1
        for i in counts.values():
            if i > 9:
                toast("Enter a Valid Cube", background=[0,0,0,1])
                return True

        cti = {}
        values = {4: 1, 22: 2, 25: 0, 28: 3, 31: 5, 49: 4}
        for c in self.fixed:
            cti[''.join(str(x) for x in self.fixed[c])] = values[c]
        data = []
        for i in colors:
            data.append(cti[i])
        self.original_cube = []
        for i in range(6):
            self.original_cube.append([])
            for j in range(3):
                self.original_cube[i].append([])

        white = [[12, 13, 14], [24, 25, 26], [36, 37, 38]]
        green = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        red = [[9, 10, 11], [21, 22, 23], [33, 34, 35]]
        orange = [[15, 16, 17], [27, 28, 29], [39, 40, 41]]
        blue = [[45, 46, 47], [48, 49, 50], [51, 52, 53]]
        yellow = [[44, 43, 42], [32, 31, 30], [20, 19, 18]]

        temp_cube = [white, green, red, orange, blue, yellow]

        for i, a in enumerate(temp_cube):
            for j, b in enumerate(a):
                for c in b:
                    self.original_cube[i][j].append(data[c])

        global INPUT_CUBE, INPUT
        INPUT_CUBE = self.original_cube
        INPUT = [True, True]

        self.manager.current = 'main'

    def reset(self, instance):
        for i in range(54):
            if i in self.fixed:
                self.ids[i].background_color = self.fixed[i]
                continue
            self.ids[i].background_color = (1, 1, 1, 0.7)

    def update(self, *args):
        self.done_btn.size = (120, 60)
        self.done_btn.pos = (970, 40)
        self.reset_btn.size = (120, 60)
        self.reset_btn.pos = (1100, 40)

        b = 65
        s1 = 30 + b*3 + 12
        s2 = 30
        h = 600

        for j, i in enumerate(self.fixed):
            self.ids[str(i)].size = (70, 70)
            self.ids[str(i)].pos = (970 + (90 * (j % 3)), (h - b*3.5 - 5) - (90 * (j // 3)))

        for i in range(54):
            self.ids[i].size = (b, b)

        n = 0
        for i in range(3):
            for j in range(3):
                self.ids[n].pos = (s1 + ((b + 3) * j), h)
                n += 1
            h -= b + 3
        h -= 3

        for i in range(3):
            t = 0
            for j in range(12):
                if j % 3 == 0 and j != 0:
                    t += 3
                self.ids[n].pos = (s2 + ((b + 3) * j) + t, h)
                n += 1
            h -= b + 3
        h -= 3

        for i in range(3):
            for j in range(3):
                self.ids[n].pos = (s1 + ((b + 3) * j), h)
                n += 1
            h -= b + 3

        self.pointer.size = (b, b)
        self.pointer.pos = self.ids[0].pos


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)


class MyApp(MDApp):
    def build(self):
        self.title = "Rubik's Cube Solver"
        sm = ScreenManagement(transition=FadeTransition())
        sm.add_widget(MainWindow(name='main'))
        sm.add_widget(InputWindow(name='input'))
        return sm


if __name__ == '__main__':
    MyApp().run()
