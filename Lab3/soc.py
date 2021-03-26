import socket
import numpy as np
import json
import time
import random
import matplotlib.pyplot as plt

def live_plotter(x_vec,y1_data,line1,identifier='',pause_time=0.1):
    if line1==[]:
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)        
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()
    line1.set_ydata(y1_data)
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    plt.pause(pause_time)
    return line1


HOST='192.168.0.145'
PORT=65432
count = 0
count_lst = np.linspace(0,1,11)[0:-1]
x_lst = []
y_lst = []
x_avg = np.zeros(np.shape(count_lst))
y_avg = np.zeros(np.shape(count_lst))
line1 = []
line2 = []
line3 = []
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by ', addr)
        while True:
            data = conn.recv(1024).decode('utf-8')
            print("Recieved from socket:  ", data)
            try:
                j_data = json.loads(data)
                print(j_data)
                count += 1
                x_lst.append(j_data['x'])
                y_lst.append(j_data['y'])
            except:
                print('decode error')
            if count % 10 == 0:
                x_avg[-1] = (sum(x_lst)/10)
                x_lst.clear()
                y_avg[-1] = (sum(y_lst)/10)
                y_lst.clear()
                line1 = live_plotter(count_lst, x_avg, line1)
                line2 = live_plotter(count_lst, y_avg, line2)
                x_avg = np.append(x_avg[1:],0.0)
                y_avg = np.append(y_avg[1:],0.0)

                
