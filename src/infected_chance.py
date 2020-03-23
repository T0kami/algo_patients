#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd
import datetime
from datetime import timedelta

day = 20
month = 3
year = 2020
chatlog = []




def main():
    # Parsing
    with open('../data/chatlog_complet_firstpart.txt', encoding="utf8") as f1:
        for (i,line) in enumerate(f1):
            tmp = []
            tmp.append(line.split(': ')[0].split('] ')[1].split(' ')[0])
            tmp.append(datetime.datetime.strptime(line.split('.')[0].split('[')[1] + "-" + str(year) + "-" + str(month) + "-" + str(day), '%H:%M:%S-%Y-%m-%d') + timedelta(hours=18,minutes=7,seconds=32))
            tmp.append(' '.join(line.split(' ')[2:]))
            
            #tmp.append(datetime.datetime.strptime(line.split('.')[0].split('[')[1] + "-" + str(year) + "-" + month + "-" + day, '%H:%M:%S-%Y-%M-%D').timestamp())
            chatlog.append(tmp)
    





if __name__ == "__main__":
    main()


