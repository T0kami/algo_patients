# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 03:29:26 2020

@author: Lebas Bastien
"""

import os
import random
import matplotlib.pyplot  as plt
import numpy as np
import pandas as pd

Liste_pseudo=[]
Liste_timing=[]
data_cas=[]
data_timing=[]
taux_transmission=0.059

with open('pseudo2.txt', encoding="utf8") as f1:
    for (i,line) in enumerate(f1):
        Liste_pseudo.append(line.split(': ')[0].split('] ')[1].split(' ')[0])
        Liste_timing.append(line.split('] ')[0].split('[')[1])

for i in range(len(Liste_timing)):
    time=Liste_timing[i]
    Liste_timing[i]=int(time.split(':')[0])+int(time.split(':')[1])/60+float(time.split(':')[2])/3600


with open('data2.txt', encoding="utf8") as f2:
    for (i,line) in enumerate(f2):
        data_cas.append(int(line.split('\t')[1]))
        time=line.split('\t')[0]
        data_timing.append(int(time.split(':')[0])+int(time.split(':')[1])/60+float(time.split(':')[2])/3600)

#guest3147
#Clu3tik_POGGIES
#Rlcop
#Oonei
# and 'agathoorr' not in Liste_infecte and 'luxime' not in Liste_infecte and 'guest3147' not in Liste_infecte and 'Clu3tik_POGGIES'not in Liste_infecte and 'Rlcop'not in Liste_infecte and  'Oonei' not in Liste_infecte
#Liste_confirmed=[]
#with open('Confirmed.txt', encoding="utf8") as f3:
#    for (i,line) in enumerate(f3):
#        Liste_confirmed.append(line)
#Liste_confirmed=Liste_confirmed[:6]
#
Liste_confirmed=['Saichiko','Sarakzite','Vidaviya','Oonei','guest3147','Clu3tiK_POGGIES','Rlcop','luxime','agathoorr']
#cas_zero='so_ez4ence'
cas_zero='Sarakzite'
#cas_zero='Sarukog'
#cas_zero='Titatitutu'
#cas_zero='Sardbot'
#cas_zero='Saichiko'
def Propagation(cas_zero):
    Liste_infecte=[]
    c=0
    longeur_moyenne=0
    while 'Clu3tiK_POGGIES' not in Liste_infecte:
        c+=1
        Liste_infecte=[cas_zero]
        Liste_timing_infection=[0]
        nb_infectes=[1]
        historique=[]
        for i_pseudo in range(len(Liste_pseudo)-1):
                if Liste_pseudo[i_pseudo-1]in Liste_infecte or Liste_pseudo[i_pseudo+1]in Liste_infecte:
                    if Liste_pseudo[i_pseudo] not in Liste_infecte:
                        if random.uniform(0, 1) < taux_transmission:
                            Liste_infecte.append(Liste_pseudo[i_pseudo])
                            Liste_timing_infection.append(Liste_timing[i_pseudo])
                            historique.append(Liste_pseudo[i_pseudo-1:i_pseudo+2])
                            nb_infectes.append(nb_infectes[-1]+1)
        longeur_moyenne+=len(Liste_infecte)
        for confirmed in Liste_confirmed:
            if confirmed not in Liste_infecte:
                Liste_infecte=[cas_zero]
        try:
            if Liste_infecte.index('guest3147')>Liste_infecte.index('aMa_____'):
                i=0
                while 'guest3147'not in historique[i] and 'aMa_____' not in historique[i]:
                    i+=1
                    if i>=len(historique):
                        Liste_infecte=[cas_zero]
        except ValueError:
            Liste_infecte=[cas_zero]
        try:
            if Liste_infecte.index('Oonei')>Liste_infecte.index('Rlcop'):
                i=0
                while 'Oonei' not in historique[i] and 'Rlcop' not in historique[i]:
                    i+=1
                    if i>=len(historique):
                        Liste_infecte=[cas_zero]
        except ValueError:
            Liste_infecte=[cas_zero]
        try:
            if Liste_infecte.index('luxime')>Liste_infecte.index('agathoorr'):
                i=0
                while 'luxime' not in historique[i] and 'agathoorr' not in historique[i]:
                    i+=1
                    if i>=len(historique):
                        Liste_infecte=[cas_zero]
        except ValueError:
            Liste_infecte=[cas_zero]
            
        try:
            if Liste_infecte.index('Vidaviya')!=93:
                Liste_infecte=[cas_zero]
        except ValueError:
            p=1
    return Liste_infecte, Liste_timing_infection, nb_infectes, historique

def fitting(Liste_timing_infection,x_fitting):
    y_fitting=np.zeros(len(x_fitting))
    for i in range(len(x_fitting)):
        c=0
        for j in range(len(Liste_timing_infection)):
            if Liste_timing_infection[j]<=x_fitting[i]:
                c+=1
        y_fitting[i]=c
    return y_fitting

#%%
dico={}
dico_historique={}
plt.figure()
plt.title('Propagation en prenant comme point de depart: '+cas_zero)
y_fitting=np.zeros((612,5))
for n in range(5):
    print(n)
    Liste_infecte, Liste_timing_infection, nb_infectes, historique=Propagation(cas_zero)
    dico[n]=Liste_infecte
    dico_historique[n]=historique
    Liste_timing_infection=np.asarray(Liste_timing_infection)
    x_fitting=np.linspace(0,6.20,612)
    y_fitting[:,n]=fitting(Liste_timing_infection,x_fitting)

y_final=np.zeros(612)
for i in range(612):
    y_final[i]=np.mean(y_fitting[i,:])

plt.plot(data_timing,data_cas,'r')
plt.plot(x_fitting,y_final,'g')
plt.xlabel('Duree du stream (en h)')
plt.ylabel("Nombre d'infectes")
plt.legend(['Experience','Model'])

pseudo_infecte_list=[]
for n in range(5):
    for pseudo in dico[n]:
        pseudo_infecte_list.append(pseudo)

list_count=[]
list_unique_pseudo=[]
for nbr in pseudo_infecte_list:
    if nbr not in list_unique_pseudo:
        list_unique_pseudo.append(nbr)
 
for pseudo in list_unique_pseudo:
    list_count.append(pseudo_infecte_list.count(pseudo))

Matrice=pd.DataFrame({'Pseudo': list_unique_pseudo, 'Nombre': list_count})
#for i in range (len(Matrice['Pseudo'])):
#    if Matrice['Pseudo'][i]=='guest3147':
#        print(Matrice['Nombre'][i])

Matrice2=Matrice[Matrice.Nombre > 24]

Matrice_position=pd.DataFrame({'Numero_cas': [k+1 for k in range(5)]})
#pd.get_dummies(Matrice_position["keys"])

for i in range(len(list_unique_pseudo)):
    pseudo=list_unique_pseudo[i]
    liste_pseudo=[]
    for n in range(len(dico)):
        try:
            liste_pseudo.append(dico[n].index(pseudo))
        except ValueError:
            liste_pseudo.append(-1)
    Matrice_position[pseudo]=liste_pseudo

#%% fitting

def indicateur(data_timing):
    x_fitting=np.linspace(0,6.20,612)
    y_fitting_data=fitting(data_timing,x_fitting)
    
    indic=0
    for i in range(len(y_fitting_data)):
        indic+=y_fitting_data[i]+y_final[i]
    print(indic)
    return(indic)

#%% Reverse

Liste_infecte=['Vidaviya']
#Liste_timing_infection=[0]
#nb_infectes=[1]
#historique=[]
taux_transmission=0.08

i_start_list=[]
for i_pseudo in range(len(Liste_pseudo)-1):
    if Liste_pseudo[i_pseudo]=='Vidaviya':
        if i_pseudo<20000:#on reduit les possibilites car on sait que la conta arrive avant
            i_start_list.append(i_pseudo)

nb_infectes=0
list_nb_infection=[]
#for start_i in i_start_list:
start_i=i_start_list[122]
for i_pseudo in range(start_i,-1,-1):
    if Liste_pseudo[i_pseudo-1]in Liste_infecte or Liste_pseudo[i_pseudo+1]in Liste_infecte:
        if random.uniform(0, 1) < taux_transmission:
            Liste_infecte.append(Liste_pseudo[i_pseudo])
#                        Liste_timing_infection.append(Liste_timing[i_pseudo])
#                        historique.append(Liste_pseudo[i_pseudo])
            nb_infectes+=1
list_nb_infection.append(nb_infectes)

