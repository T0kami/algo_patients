#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd
import datetime
from datetime import timedelta



chatlog = []




def main():
    # Parsing
    day = 20
    month = 3
    year = 2020
    with open('../data/chatlog_complet_firstpart.txt', encoding="utf8") as f1:
        for (i,line) in enumerate(f1):
            tmp = []
            tmp.append(line.split(': ')[0].split('] ')[1].split(' ')[0])
            tmp.append(datetime.datetime.strptime(line.split('.')[0].split('[')[1] + "-" + str(year) + "-" + str(month) + "-" + str(day), '%H:%M:%S-%Y-%m-%d') + timedelta(hours=18,minutes=7,seconds=32))
            tmp.append(' '.join(line.split(' ')[2:]))
            chatlog.append(tmp)
    with open('../data/chatlog_complet.txt', encoding="utf8") as f1:
        for (i,line) in enumerate(f1):
            tmp = []
            if (line.find(" <") != -1 and line.find(">") != -1):
                tmp.append(line.split('>')[0].split(' <')[1])
                tmp.append(datetime.datetime.strptime(line.split('[')[1].split('] ')[0] + "-" + str(year) + "-" + str(month) + "-" + str(day), '%H:%M:%S-%Y-%m-%d'))
                if (tmp[1] < chatlog[-1][1]):
                    day = day + 1
                    tmp[1] += timedelta(days=1)
                tmp.append(line.split('>')[1])
                chatlog.append(tmp)
    print(chatlog)


if __name__ == "__main__":
    main()


