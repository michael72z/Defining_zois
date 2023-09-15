import re
import matplotlib.pyplot as plt
import numpy as np
import random

pattern = r"normalized vector is \[(-?\d+\.\d+), (-?\d+\.\d+)\]"
pattern2 = r"ctrl\|(-?\d+)\|(-?\d+)\|(-?\d+)\|(-?\d+)\|(-?\d+)"
pattern3 = r'set detection pid \[(.*?)\]'

log_file_path = 'info168.log'
with open(log_file_path, 'r') as log_file:
    lines = log_file.readlines()

x_list = []
y_list = []

x_ctrl_list = []
y_ctrl_list = []

pid_list = []

for i in range(len(lines)):
    matches = re.findall(pattern, lines[i])
    if matches:
        normalized_vector_values = matches[0]
        x_value = float(normalized_vector_values[0])
        y_value = float(normalized_vector_values[1])
        matches2 = re.findall(pattern2, lines[i + 1])
        if matches2:
            ctrl_msg = matches2[0]
            x_ctrl = int(ctrl_msg[1])
            y_ctrl = int(ctrl_msg[2])
            x_ctrl_list.append(x_ctrl)
            y_ctrl_list.append(y_ctrl)
            x_list.append(x_value)
            y_list.append(y_value)
    pid_matches = re.findall(pattern3, lines[i])
    if pid_matches:
        pid = pid_matches[0]
        tmp_pid = {'index': len(x_ctrl_list) - 1 if len(x_ctrl_list) else 0,
                   'pid': pid}
        pid_list.append(tmp_pid)
        # pid = pid_matches[0].split(',')
        # pid = [float(x) for x in pid]
        # # pid_num = [float(match) if '.' in match else int(match) for match in pid_matches]

time_list = np.arange(1, len(x_list) + 1, 1)

fig1, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
fig2, (ax3, ax4) = plt.subplots(2, 1, sharex=True)

ax1.plot(time_list, x_list, label='x deviation')
ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax1.set_title('Deviation')
ax1.grid()


ax2.plot(time_list, x_ctrl_list, label='x output')
for j in range(len(pid_list)):
    pid_ = pid_list[j]

    if j == len(pid_list) - 1:
        x2 = len(x_list) - 1
    else:
        x2 = pid_list[j + 1].get('index')

    random_color = (random.random(), random.random(), random.random())
    ax2.axvline(x=pid_.get('index'), color=random_color, linestyle='--', label="PID:" + pid_.get('pid'))
    ax1.axvline(x=pid_.get('index'), color=random_color, linestyle='--')
    ax2.fill_betweenx(y=[min(x_ctrl_list), max(x_ctrl_list)], x1=pid_.get('index'), x2=x2,
                      color=random_color, alpha=0.2)
    ax1.fill_betweenx(y=[min(x_list), max(x_list)], x1=pid_.get('index'), x2=x2,
                      color=random_color, alpha=0.2)
ax2.set_xlabel('time')
ax2.set_title('PID')
ax2.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax2.grid()

ax3.plot(time_list, y_list, label='y deviation')
ax3.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax3.set_title('Deviation')
ax3.grid()

ax4.plot(time_list, y_ctrl_list, label='y output')
for j in range(len(pid_list)):
    pid_ = pid_list[j]

    if j == len(pid_list) - 1:
        x2 = len(x_list) - 1
    else:
        x2 = pid_list[j + 1].get('index')

    random_color = (random.random(), random.random(), random.random())
    ax4.axvline(x=pid_.get('index'), color=random_color, linestyle='--', label="PID:" + pid_.get('pid'))
    ax3.axvline(x=pid_.get('index'), color=random_color, linestyle='--')
    ax4.fill_betweenx(y=[min(y_ctrl_list), max(y_ctrl_list)], x1=pid_.get('index'), x2=x2,
                      color=random_color, alpha=0.2)
    ax3.fill_betweenx(y=[min(y_list), max(y_list)], x1=pid_.get('index'), x2=x2,
                      color=random_color, alpha=0.2)
ax4.set_xlabel('time')
ax4.set_title('PID')
ax4.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax4.grid()

plt.tight_layout()
plt.show()
