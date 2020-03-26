# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:18:48 2020

@author: Lebas Bastien
"""

import os
import numpy as np
import pandas as pd
#import datetime
import matplotlib.pyplot  as plt
import time
import pylab

# Message, stockes dans une liste
class Message:
    def __init__(self, date, name, content):
        self.date = date
        self.name = name
        self.content = content

def importation_part_1():
    year=2020
    time_debut=None
    chatlog=[]
    with open('../../data/avant_2h.txt', encoding="utf8") as f1:
        for (i,line) in enumerate(f1):
            if '/me' not in line:
                date=time.strptime(line.split('] ')[0].split('[')[1].split('.')[0]+':'+str(year), '%H:%M:%S:%Y')
                if time_debut==None:
                    time_debut=time.mktime(date)
                name=line.split(': ')[0].split('] ')[1].split(' ')[0]
                date=time.mktime(date)-time_debut
                chatlog.append(Message(date,name,line))
    return(chatlog)

def importation_part_2():
    year=2020
    day=1
    check_pre=24
    time_debut=None
    list_pseudo=[]
    with open('../../data/apres_2h.txt', encoding="utf8") as f1:
        for (i,line) in enumerate(f1):
            if '<' in line and '/me' not in line:
                if check_pre>int(line.split('[')[1].split(':')[0]):
                    day+=1
                name=line.split('<')[1].split('>')[0]
                date2=time.strptime(line.split('] ')[0].split('[')[1]+':'+str(year), '%H:%M:%S:%Y')
                if time_debut==None:
                    time_debut=time.mktime(date2)
                date=(time.mktime(date2)-time_debut)/3600#date[2]*24*3600+date[3]*3600+date[4]*60+date[5]
                check_pre=int(line.split('[')[1].split(':')[0])
                list_pseudo.append(Message(date,name,line))
    return(list_pseudo)


def parseur():
    chatlog_part_1=importation_part_1()
    chatlog_part_2=importation_part_2()
    for message in chatlog_part_2:
        message.date+=chatlog_part_1[-1].date
    return(chatlog_part_1+chatlog_part_2)
