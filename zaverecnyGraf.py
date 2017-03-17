#-*- coding: cp1250 -*-
# Modul vykresleni dat

import matplotlib.pyplot as plt
import numpy as np
import scipy
import random
import os
import paramiko
import operator
from matplotlib.ticker import FormatStrFormatter

# VYHODNOCENÍ DAT srovnání první a druhe best
# -------------------
# získání hodnot Acc
index = 1;
index2 = 1;
index3 =1;
Acc = [];
Acc2 = [];
Acc3 = [];

procenta = [20,30,50]

# ziskani hodnot z vyslednych souboru
for i in procenta[:]:
  nazev = 'tmp_tia_baseline/metoda4/selekce/'+str(i)+'_slovnik3/test.Ydec.tia.transcribed_trns.hdm-3_' + str(i) +'_slovnik3.cdc.txt'
  nazev2 = 'tmp_tia_baseline/metoda1/manualni_realna/'+str(i)+'_manualni_realna/test.Ydec.tia.transcribed_trns.hdm-3_' + str(i) +'_manualni_realna.cdc.txt'
  nazev3 = 'tmp_tia_baseline/metoda2/best/'+str(i)+'_SCORE_final/test.Ydec.tia.transcribed_trns.hdm-3_' + str(i) +'_SCORE_final.cdc.txt'
  soubor = file(nazev,'r') 
  for radek in soubor:
    if radek.find("Acc")!=-1 and radek.find("Acc")<24 :
       index = radek.find("Acc")
       print "Best Acc :", radek[index+4:index+9], "Procenta:", i
       Acc = Acc + [float(radek[index+4:index+9])]
       index = index + 1
  soubor.close()
  
  soubor2 = file(nazev2,'r')
  for radek2 in soubor2:
    if radek2.find("Acc")!=-1 and radek2.find("Acc")<24 :
       index2 = radek2.find("Acc")
       print "Best Acc :", radek2[index2+4:index2+9], "Procenta:", i
       Acc2 = Acc2 + [float(radek2[index2+4:index2+9])]
       index2 = index2 + 1
  soubor2.close()

  soubor3 = file(nazev3,'r')
  for radek3 in soubor3:
    if radek3.find("Acc")!=-1 and radek3.find("Acc")<24 :
       index3 = radek3.find("Acc")
       print "Best Acc :", radek3[index3+4:index3+9], "Procenta:", i
       Acc3 = Acc3 + [float(radek3[index3+4:index3+9])]
       index3 = index3 + 1
  soubor3.close()

x = np.array([10,20,30])
y = np.array(Acc)
z = np.array(Acc2)
w = np.array(Acc3)

names = ['10% +', '10','20','40']

# sloupcovy graf
fig = plt.figure()
ax = fig.add_subplot(111)
ax.bar(x-4.05, w,width=2.7,color='#23a4a6',align='center', label=u'Selekce neurčitých dat')
ax.bar(x-1.35, y,width=2.7,color='#5ac3b6',align='center', label=u'Selekce dle míry '+r'$V_{u}$' + u' (25%)')
ax.bar(x+1.35, z,width=2.7,color='#bfdb79',align='center', label=u'Baseline',  hatch='//')
ax.set_xticks([3,10,20,30])
ax.set_xticklabels(names)

# specifikace grafu
plt.hold(True)
#plt.xscale('log')
plt.axis([3,30+4.5, 70.2, 87])
plt.xlabel(u'Množství dat [%]')
plt.ylabel(u'cAcc')
plt.grid(True, which='both',axis='both')
plt.legend(loc='upper left', numpoints = 1, prop={'size':16})
plt.annotate(str(round(Acc3[0],1)), xy=(4.85,  Acc3[0] +0.2),fontsize = 16)  # +1
plt.annotate(str(round(Acc[0],1)),  xy=(7.55,  Acc[0] +0.2 ),fontsize = 16)  
plt.annotate(str(round(Acc2[0],1)), xy=(10.25, Acc2[0] +0.2),fontsize = 16)
plt.annotate(str(round(Acc3[1],1)), xy=(14.85, Acc3[1] +0.2),fontsize = 16) 
plt.annotate(str(round(Acc[1],1)),  xy=(17.55, Acc[1] +0.2 ),fontsize = 16)
plt.annotate(str(round(Acc2[1],1)), xy=(20.25, Acc2[1] +0.2),fontsize = 16)
plt.annotate(str(round(Acc3[2],1)), xy=(24.85, Acc3[2] +0.2),fontsize = 16) 
plt.annotate(str(round(Acc[2],1)),  xy=(27.55, Acc[2] +0.2 ),fontsize = 16)
plt.annotate(str(round(Acc2[2],1)), xy=(30.25, Acc2[2] +0.2),fontsize = 16)

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(16)
plt.show()
