import time
import threading

import serial
import serial.tools.list_ports
import numpy as np
import matplotlib as plt

"""-------------------Choose COM device-------------------"""
def connect():
    print('Search...')
    ports = serial.tools.list_ports.comports(include_links=False)
    port_dict = {}
    for com, port in enumerate(ports):
        print(f"Find port on index {com}: {port.device}")
        port_dict[com] = port

    def ask(again=False):
        if again:
            print("Com not chosen, please input nothing but an integer.")
        num = input("Choose integer index of device: ")
        try:
            num = int(num)
            return num
        except ValueError:
            return ask(again=True)

    port = port_dict[ask()]
    ser = serial.Serial(port.device)
    if ser.isOpen():
        ser.close()
        
    ser = serial.Serial(port.device, 9600, timeout=1)
    ser.flushInput()
    ser.flushOutput()
    print(f"Connected to: {ser.name}")
    return ser
    
def read():
    inputs = ser.readline(30).decode("utf-8")
    while not inputs == "START":
        inputs = ser.readline(30).decode("utf-8")
    func = threading.Timer(1/samplingRate, fix)
    func.start()
    while not inputs == "END":
        inputs = ser.readline(30).decode("utf-8")
        if inputs == "HIGH":
            global high
            high = True
            """
            global data
            index = len(data)
            datum = [1, float(time.time())]
            data.append(datum)
            if not data[index] == datum:
                index += 1
            """
        if inputs == "LOW":
            global high
            high = False
        if not func.is_alive():
            func = threading.Timer(1/samplingRate, fix)
            func.start()
        
def fix():
    append = 0 if not high else 1
    global data
    data.append(append)
    
def fft():
    global data
    global output
    output = np.fft.fft(np.Array(data))
    plt.plot(output.toList())
    
if __name__ == "__main__":
    samplingRate = 130
    data = []
    high = False
    output = []
    ser = connect()
    read()
    fft()
