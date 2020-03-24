# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:40:04 2020

@author: Lebas Bastien
"""
import os
import numpy as np
import pandas as pd
import datetime
year=2020
chatlog=[]
with open('../data/chatlog_complet.txt', encoding="utf8") as f1:
    for (i,line) in enumerate(f1):
        tmp = []
        if 'BAN: ' in line:
            tmp.append(line.split('BAN: ')[1].split(' (')[0])
            tmp.append(datetime.datetime.strptime(line.split('] ')[0].split('[')[1] + ":" + str(year), '%H:%M:%S:%Y').timestamp())
            temps_ban=line.split('(')[-1].split('s)')[0]
            try:
                temps_ban=int(temps_ban)
            except:
                temps_ban=-1
            tmp.append(temps_ban)
            chatlog.append(tmp)