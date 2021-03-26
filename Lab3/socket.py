import socket
import numpy as np
import json
import time
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

HOST='192.168.0.145'
PORT=65431

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    conn, addr = s.accept()
    count = 0
    count_lst = []
    x_lst = []
    y_lst = []
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    with conn:
        print('Connected by ', addr)
        while True:
            data = conn.recv(1024).decode('utf-8')
            print("Recieved from socket:  ", data)
            try:
                j_data = json.loads(data)
                print(j_data)
                count += 1
                count_lst.append(count)
                x_lst.append(j_data['x'])
                y_lst.append(j_data['y'])

                ax.plt(count_lst, x_lst)
                fig.canvas.draw()
                time.sleep(5)
            except:
                print('decode error')
plt.show()

def animate(i):
    x = count_lst[-1]
    y1 = x_lst[-1]
    y2 = y_lst[-1]

    plt.cla()

    plt.plot(x, y1, label='x')
    plt.plot(x, y2, label='y')

    plt.legend(loc='upper left')
    plt.tight_layout()