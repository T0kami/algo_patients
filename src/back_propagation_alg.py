#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd
import datetime

year = 2020
chatlog=[]
time_propagation = []
Liste_plus_probable=[]

def back_propagation(pseudo, place, timemax, result):
    #print("pseudo : " + pseudo + ", place : " + str(place))
    for log in result:
        if (pseudo == log):
            return
    result.append(pseudo)
    timemin = 0
    keep = 0

    for i in range(len(time_propagation) - 1):
        if (time_propagation[i][1] < place and time_propagation[i + 1][1] >= place):
            if (timemax == 0):
                timemax = time_propagation[i + 1][0]
            keep = time_propagation[i][0]


    
    rec = False
    # Récursivité
    for i in range(len(chatlog) - 1):
        if (chatlog[i][1] > timemax):
            break

        if (chatlog[i][0] == pseudo and chatlog[i][1] > timemin):
            rec = True
            back_propagation(chatlog[i - 1][0], place - 1, chatlog[i][1], result)
            back_propagation(chatlog[i + 1][0], place - 1, chatlog[i][1], result)
    
    if (rec == False and timemax <= time_propagation[0][0]):
        print(pseudo)
        #print(result)
        Liste_plus_probable.append(pseudo)
        fichier=open('../data/Sarakzite.csv', 'a')
        fichier.write(pseudo+"\n")
        return


def main():
    # Parsing
    with open('../data/chatlog.txt', encoding="utf8") as f1:
        for (i,line) in enumerate(f1):
            tmp = []
            tmp.append(line.split(': ')[0].split('] ')[1].split(' ')[0])
            tmp.append(datetime.datetime.strptime(line.split('] ')[0].split('[')[1] + ":" + str(year), '%H:%M:%S.%f:%Y').timestamp())
            chatlog.append(tmp)
    with open('../data/time_propagation.txt', encoding="utf8") as f1:
        for (i,line) in enumerate(f1):
            tmp = []
            tmp.append(datetime.datetime.strptime(line.split('\t')[0] + ":" + str(year), '%H:%M:%S:%Y').timestamp())
            tmp.append(int(line.split('\t')[1]))
            time_propagation.append(tmp)

    # Start
    result = []
    back_propagation('Sarakzite',7, 0, result)




if __name__ == "__main__":
    main()



