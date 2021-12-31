import serial
import time
import pandas as pd
import numpy as np
import multiprocessing
#import logging

"""
input("Start?")
n = 0
start_time = time.time()
while True:
    ser.readline(30)
    current_time = time.time()
    n += 1
    if ((current_time - start_time) > 100):
        break
print(f"Sample frequency: {n/(current_time - start_time)}")
"""

def control_overflow():
    while True:
        cutoff = float(time.time()) - 50
        if stop:
            break
        for i in data:
            if i[0] < cutoff:
                print(data[0])
                data.pop(0)
            else:
                break

def accept():
    start_time = float(time.time())
    n = 0
    while True:
        datum = ser.readline(30).decode("utf-8").strip().split(",")
        if (len(datum) < 3) or "" in datum:
            continue
        current_time = float(time.time())
        datum[len(datum)-1] = (datum[len(datum)-1])[:-1]
        datum = [int(i) for i in datum]
        data_list = [current_time]
        data_list.extend(datum)
        #print(data_list)
        data.append(data_list)
        #print(len(data))
        n += 1
        if ((current_time - start_time) > 60):
            stop = True
            global sample_frequency
            sample_frequency = n/(current_time - start_time)
            break

def process_data():
    optimal = 1/sample_frequency
    stream_data_one = [data[i][1] for i in range(len(data))]
    info = []
    pro_data = []
    ooi = False
    """
    for index, element in enumerate(data):
        print(index, element)
        if index == 0:
            pro_data.append(element)
        else:
            new_time = optimal + pro_data[index-1][0]
            time_delta = (element[0] - pro_data[index-1][0])
            print(time_delta)
            slopes = [((element[i+1] - pro_data[index-1][i+1])/time_delta) for i in range(len(element)-1)]
            print(slopes)
            xs = new_time - pro_data[index-1][0]
            print(xs)
            new_signals = [((slopes[i] * xs) + pro_data[index-1][i+1]) for i in range(len(slopes))]
            new_signals.insert(0, new_time)
            pro_data.append(new_signals)
    """
    #The above does the wrong thing entirely
    
    for index, element in enumerate(data):
        if not index == 0:
            time_delta = (element[0] - data[index-1][0])
            if time_delta == 0:
                time_delta = 0.00000000001
            slopes = [((element[i+1] - data[index-1][i+1])/time_delta) for i in range(len(element)-1)]
            info.append([data[index-1][0], element[0], time_delta, slopes])

    n = 0
    while not ooi:
        if n == 0:
            pro_data.append(data[n])
            n += 1
        else:
            new_time = pro_data[n-1][0] + optimal
            found = False
            for correct_range in info:
                #print(correct_range[0], new_time, correct_range[1])
                if correct_range[0] <= new_time and correct_range[1] >= new_time:
                    found = True
                    break
            if not found:
                print("backup")
                for i in range(len(info)):
                    if (i-1) == 0:
                        continue
                    if info[i-2][1] <= new_time and info[i-1][0] >= new_time:
                        l = i + 1
                        time_delta = (data[l][0] - data[l-1][0])
                        slopes = [((data[l][i+1] - data[l-1][i+1])/time_delta) for i in range(len(data[l])-1)]
                        correct_range = [data[l-1][0], data[l][0], time_delta, slopes]
                        found = True
                        break
            if not found:
                print("L")
                ooi = True
                break
            xs = new_time - correct_range[0]
            new_signals = [round((correct_range[3][i] * xs) + data[info.index(correct_range)][i+1]) for i in range(len(data[info.index(correct_range)])-1)]
            for index, element in enumerate(new_signals):
                if element < 0:
                    new_signals[index] = 0
            new_signals.insert(0, new_time)
            pro_data.append(new_signals)
            n += 1

    return pro_data

if __name__ == "__main__":
    input("Start?")
    ser = serial.Serial('COM3', 9800, timeout=1)
    data = []
    sample_frequency = 20
    start_time = float(time.time())
    while True:
        datum = ser.readline(30).decode("utf-8").strip().split(",")
        if (len(datum) < 3) or "" in datum:
            continue
        current_time = float(time.time())
        datum[len(datum)-1] = (datum[len(datum)-1])[:-1]
        datum = [int(i) for i in datum]
        data_list = [current_time]
        data_list.extend(datum)
        data.append(data_list)
        if ((current_time - start_time) > 20):
            break

    stop = False
    delete = multiprocessing.Process(target=control_overflow)
    paccept = multiprocessing.Process(target=accept)
    paccept.start()
    delete.start()

    paccept.join()
    delete.join()
    
    print(f"Difference in time between first and last element: {data[len(data)-1][0] - data[0][0]}")

    print(np.array(data))
    pro_data = process_data()
    print(len(pro_data))
    print(np.array(pro_data))
    #print(np.fft.fft(np.array(pro_data)))
    #ser.readline()
    #print(ser.readline(30))
    ser.close()
    #exit()
