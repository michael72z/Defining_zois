import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

zoi_range = 0.2
zoi_list = []
choices = []

data = pd.read_csv('drone6.csv')
x = data['x_value']
y1 = data['total_1']
y2 = data['total_2']

plt.xlabel('time(seconds)')
plt.ylabel('SP & PV (angle)')
plt.title('Behaviour of drone while controlling ')

main_ax = plt.gca()
main_ax.plot(x, y2, label='ProcessVariable', color='r', linewidth=3)
main_ax.plot(x, y1, label='SetPoint', linewidth=3, color='y')
main_ax.plot([], [], 'r', label='ZOI', color='b', linewidth=3)
main_ax.legend(loc='lower left')


plt.subplots_adjust(left=0.35)


class ZoneOfInterest:
    def __init__(self, length, position, name):
        self.length = length
        self.position = position
        self.name = name
        self.lines = None
        self.ax = None

    def draw_subplot(self):
        fig, ax = plt.subplots()
        offset_l = 5000
        offset_r = 5000
        if self.position < offset_l:
            offset_l = self.position

        ax.plot(x[self.position - offset_l: self.position + self.length + 1 + offset_r],
                y1[self.position - offset_l: self.position + self.length + 1 + offset_r],
                color='y', linewidth=3)
        ax.plot(x[self.position - offset_l: self.position + self.length + 1 + offset_r],
                y2[self.position - offset_l: self.position + self.length + 1 + offset_r],
                color='r', linewidth=3)

        ax.plot(x[self.position: self.position + self.length + 1],
                y1[self.position: self.position + self.length + 1],
                color='b', linewidth=3)
        ax.plot(x[self.position: self.position + self.length + 1],
                y2[self.position: self.position + self.length + 1],
                color='b', linewidth=3)

        self.ax = plt.gcf()

    def close_subplot(self):
        plt.close(self.ax)

    def draw_lines(self):
        l1, = main_ax.plot(x[self.position: self.position + self.length + 1],
                           y1[self.position: self.position + self.length + 1],
                           color='b', linewidth=3)
        l2, = main_ax.plot(x[self.position: self.position + self.length + 1],
                           y2[self.position: self.position + self.length + 1],
                           color='b', linewidth=3)

        self.lines = l1, l2

    def change_visibility(self, state=None):
        if not state:
            self.lines[0].set_visible(not self.lines[0].get_visible())
            self.lines[1].set_visible(not self.lines[1].get_visible())
        else:
            self.lines[0].set_visible(state)
            self.lines[1].set_visible(state)


i = 0
while i < len(x):

    position = i

    if abs(y1[i] - y2[i]) > zoi_range:
        for j in range(i + 1, len(x)):
            if abs(y1[j] - y2[j]) > zoi_range:
                if j == len(x) - 1:
                    zoi = ZoneOfInterest(length=j - i, position=i, name=f'zoi {round(x[position], 2)}')
                    zoi.draw_lines()
                    zoi_list.append(zoi)

                else:
                    continue
            else:
                zoi = ZoneOfInterest(j - i, i, f'zoi {round(x[position], 2)}')
                zoi_list.append(zoi)
                zoi.draw_lines()
                i = j - 1
                break

    i += 1


def open_subplots(option_index):  # zoi 0.03, zoi3.05 etc.
    z = zoi_list[option_index]

    if check_win[option_index]:
        z.draw_subplot()
    else:
        z.close_subplot()

    plt.draw()
    plt.show()


def zooming(option_index):
    fig, ax = plt.subplots(1, 2)
    z = zoi_list[option_index]
    x_min = x[z.position] - 0.3
    x_max = x[z.position + z.length + 1] + 0.3
    ax.set_xlim(x_min, x_max)
    ax.set_xlim(x_min, x_max)
    plt.show()


def set_tobe_visible(option_index):
    z = zoi_list[option_index]
    z.change_visibility()
    plt.draw()


def combined_function(Label_name):
    option_index = choices.index(Label_name)
    check_win[option_index] = not check_win[option_index]
    set_tobe_visible(option_index)
    open_subplots(option_index)


for zoi in zoi_list:
    choices.append(zoi.name)

check_state = [False for i in range(len(choices))]
check_win = check_state.copy()

ax_checkbox = plt.axes([0.05, 0.4, 0.20, 0.25])

checkbox = CheckButtons(ax_checkbox, choices, check_state)
checkbox.on_clicked(combined_function)

for i, zone in enumerate(zoi_list):
    zone.change_visibility(check_state[i])

plt.show()
