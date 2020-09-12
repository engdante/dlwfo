from pynput.keyboard import Listener  as KeyboardListener
from pynput.mouse import Listener  as MouseListener
import numpy as np
import cv2
import pickle
import os
import sys
import time
import threading
import pandas as pd
from PIL import ImageGrab


global file_name
global current_data
global number

def get_screen(x_cor, y_cor, halfsize):
    left_x = x_cor - halfsize
    top_y = y_cor - halfsize
    right_x = x_cor + halfsize
    bottom_y = y_cor + halfsize
    img = ImageGrab.grab(bbox=(left_x, top_y, right_x, bottom_y))  
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    # cv2.imshow('image',frame)
    # cv2.waitKey(0)
    return frame

def on_release(key):
    # print ("Running on_release")
    global number
    number = number + 1
    temp = {"ID" : number, "key_event" : key, "mouse_event" : None, "mousepos_x" : None, "mousepos_y" : None, "pic_area" : None}
    # print (temp)
    global current_data
    for dictkey, value in temp.items():
        current_data[dictkey].append(value)
    return

def on_click(x,y,button, pressed):
    if pressed == False:
        # print ("Running on_click")
        buttonNo = 0
        if button == button.left : buttonNo = 2
        if button == button.right : buttonNo = 3
        if button == button.middle : buttonNo = 4
        global number
        number = number + 1
        img = get_screen(x,y,24)
        temp = {"ID" : number, "key_event" : None, "mouse_event" : buttonNo, "mousepos_x" : x, "mousepos_y" : y, "pic_area" : img}
        # print (temp)
        global current_data
        for dictkey, value in temp.items():
            current_data[dictkey].append(value)
    return

def on_scroll(x, y, dx, dy):
    global number
    number = number + 1
    img = get_screen(x,y,24)
    temp = {"ID" : number, "key_event" : None, "mouse_event" : dy, "mousepos_x" : x, "mousepos_y" : y, "pic_area" : None}
    # print (temp)
    global current_data
    for dictkey, value in temp.items():
        current_data[dictkey].append(value)

def new_file():
    threading.Timer(1800.0, new_file).start()
    global file_name
    global number
    global current_data
    current_data = {"ID" : [0], "key_event" : [0], "mouse_event" : [0], "mousepos_x" : [0], "mousepos_y" : [0], "pic_area" : [None]}
    number = 0
    script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    file_name = time.strftime(script_path + "\\data\\" + "%Y%m%d-%H%M" + ".ple")
    return

def out_file():
    threading.Timer(60.0, out_file).start()
    # print ("Running out_fdsfewfweile")
    pickle_out = open(file_name, 'wb')
    pickle.dump(current_data,pickle_out)
    pickle_out.close()
    print ("File {0} is write in disk!".format(file_name))

    # print (current_data)
    # data = pd.read_pickle(file_name)
    # data = pd.DataFrame.from_dict(current_data)
    # print (data)
    return

new_file()
out_file()

with MouseListener(on_click=on_click,on_scroll=on_scroll) as listener:
    with KeyboardListener(on_release=on_release) as listener:
        listener.join()
