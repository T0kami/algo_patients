#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd
import datetime

year = 2020
chatlog=[]
time_propagation = []


def back_propagation(pseudo, place):
    #print("pseudo : " + pseudo + ", place : " + str(place))
    timemax = 0
    timemin = 0
    if (place == 0):
        print("patient 0 : " + pseudo)
        return
    for i in range(len(time_propagation) - 1):
        if (time_propagation[i][1] < place and time_propagation[i + 1][1] >= place):
            timemax = time_propagation[i + 1][0]
            timemin = time_propagation[i][0]
    if (timemax == 0):
        return
    

    # Récursivité
    for i in range(len(chatlog) - 1):
        if (chatlog[i][0] == pseudo and chatlog[i][1] < timemax and chatlog[i][1] > timemin):
            back_propagation(chatlog[i - 1][0], place - 1)
            back_propagation(chatlog[i + 1][0], place - 1)
    print("  pseudo : " + pseudo + ", place : " + str(place))


def main():
    # Parsing
    with open('../data/chatlog.txt', encoding="utf8") as f1:
        for (i,line) in enumerate(f1):
            tmp = []
            tmp.append(line.split(': ')[0].split('] ')[1].split(' ')[0].lower())
            tmp.append(datetime.datetime.strptime(line.split('] ')[0].split('[')[1] + ":" + str(year), '%H:%M:%S.%f:%Y').timestamp())
            chatlog.append(tmp)
    with open('../data/time_propagation.txt', encoding="utf8") as f1:
        for (i,line) in enumerate(f1):
            tmp = []
            tmp.append(datetime.datetime.strptime(line.split('\t')[0] + ":" + str(year), '%H:%M:%S:%Y').timestamp())
            tmp.append(int(line.split('\t')[1]))
            time_propagation.append(tmp)

    # Start
    back_propagation("vidaviya", 93)




if __name__ == "__main__":
    main()



