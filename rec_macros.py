from pynput.keyboard import Listener  as KeyboardListener
from pynput.mouse import Listener  as MouseListener
import pickle
import os
import threading
import pandas as pd

global current_data
global number
number = 0
current_data = {"ID" : [0], "key_event" : [0], "mouse_event" : [0], "mousepos_x" : [0], "mousepos_y" : [0], "pic_area" : [None]}

def on_release(key):
    # print ("Running on_release")
    global number
    number = number + 1
    temp = {"ID" : number, "key_event" : key, "mouse_event" : None, "mousepos_x" : None, "mousepos_y" : None, "pic_area" : None}
    for dictkey, value in temp.items():
        current_data[dictkey].append(value)
    return

def on_click(x,y,button, pressed):
    if pressed == False:
        # print ("Running on_click")
        global number
        number = number + 1
        temp = {"ID" : number, "key_event" : None, "mouse_event" : button, "mousepos_x" : x, "mousepos_y" : y, "pic_area" : None}
        for dictkey, value in temp.items():
            current_data[dictkey].append(value)
    return

def out_file():
    threading.Timer(5.0, out_file).start()
    # print ("Running out_fdsfewfweile")
    pickle_out = open("data.ple", 'wb')
    pickle.dump(current_data,pickle_out)
    pickle_out.close()

    # print (current_data)

    data = pd.DataFrame.from_dict(current_data)
    print (data)
    return

out_file()

with MouseListener(on_click=on_click) as listener:
    with KeyboardListener(on_release=on_release) as listener:
        listener.join()
