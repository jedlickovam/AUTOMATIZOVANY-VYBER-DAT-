# -*- coding: cp1250 -*-
# Modul vykresleni dat

import matplotlib.pyplot as plt
import numpy as np

procenta = [5,10,20,30,40,50,60,70,80,90,100]
Acc = []
Acc2 = []

index = 1;
for i in procenta:
  nazev = 'tmp_tia_baseline/metoda1/realna/'+str(i)+'_realna/test.Ydec.tia.transcribed_trns.hdm-3_' + str(i) +'_realna.cdc.txt'
  nazev2 = 'tmp_tia_baseline/metoda1/manualni_realna/'+str(i)+'_manualni_realna/test.Ydec.tia.transcribed_trns.hdm-3_' + str(i) +'_manualni_realna.cdc.txt'
  soubor = file(nazev,'r')
  soubor2 = file(nazev2,'r') 
  for radek in soubor:
    if radek.find("Acc")!=-1 and radek.find("Acc")<24 :
       index = radek.find("Acc")
       print "Best Acc :", radek[index+4:index+9], "Procenta:", i
       Acc = Acc + [float(radek[index+4:index+9])]
       index = index + 1
  soubor.close()

  for radek2 in soubor2:
    if radek2.find("Acc")!=-1 and radek2.find("Acc")<24 :
       index2 = radek2.find("Acc")
       print "Best Acc :", radek2[index2+4:index2+9], "Procenta:", i
       Acc2 = Acc2 + [float(radek2[index2+4:index2+9])]
       index2 = index2 + 1
  soubor2.close()

names = ['404','808','1616','3231','4847','7639']

xp = np.linspace(5, 100, 11)

fig = plt.figure()
ax = fig.add_subplot(111)

procentaPosunuta = [4.73, 9.46, 18.92, 28.38, 37.84, 47.30, 56.76 ,66.22, 75.68,85.14,94.6]

plt.hold(True)  
# vykresleni dat s logaritmickou stupnici
plt.plot(procentaPosunuta, Acc2, '-o',color='#bfdb79', linewidth = 3, label =u'Baseline, reálná a manuální data')
plt.plot(procenta, Acc, '-o',color='#5ac3b6', linewidth = 3, label =u'Baseline, reálná data')
plt.xscale('log')
plt.axis([5, 94.6, 53, 86])
plt.xlabel(u'Počet vybraných vět')
plt.ylabel(u'cAcc')
plt.legend(loc='best', numpoints = 1, prop={'size':16})
plt.grid(True, which='both',axis='both')

ax.set_xticks([5,10,20,40,60,94.6])
ax.set_xticklabels(names)

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
  item.set_fontsize(16)
    
plt.show()
