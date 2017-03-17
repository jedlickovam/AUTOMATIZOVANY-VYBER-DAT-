# -*- coding: cp1250 -*-
# Modul vykresleni dat
# "Modul draw_graph vykreslí graf dle vložených dat"

import matplotlib.pyplot as plt
import numpy as np
import os
import scipy
import random
import paramiko
import operator

## STRATEGIE
## ---------
## Funkce pro spuštění strategií jednotlivých metod

def strategy_random(metoda_text,procenta,manual,real):
  if not os.path.exists('tia/' + metoda_text[1]):
    os.makedirs('tia/' + metoda_text[1])

  # Vytvoří list manuálních a reálných dat
  if (manual==True) and (real==True):
    s = manual_and_real_data()
  else:
    if (manual==True):
      s = manual_data()
    else:
      s = real_data()

  # Náhodně vybere data a zapíše je
  for i in procenta[:]:
    nazev= 'tia/' + metoda_text[1]+ '/'+str(i)+'_' + metoda_text[0] + '.scp'
    zapis=file(nazev,'w')
  
    chosen = random.sample(s,int((float(i)/100)*len(s)))
    print chosen
    for x in s:
      if x in chosen:
        zapis.write(x)
    zapis.close()

def strategy_P(metoda_text, procenta, sestupne, orez7, orez50):
  ## Najde F a seřadí jej
  P = find_P(metoda_text, sestupne)

  if(orez7 == True):
    P = P[len(P)/12:]
    #print P[1]

  if(orez50 == True):
    P = P[len(P)/2:]
  
  if not os.path.exists('tia/' + metoda_text[1]):
    os.makedirs('tia/' + metoda_text[1])
    
  ## Vyber data 
  choosen = choosen_data_P(procenta, P, metoda_text)


def strategy_V(metoda_text, procenta, sestupne,orez):
  ## Otevri slovnik s hodnotami Vi
  sorted_Vi = open_Dict()

  if(orez == True):
    sorted_Vi = sorted_Vi[len(sorted_Vi)/4:]
  
  if not os.path.exists('tia/' + metoda_text[1]):
    os.makedirs('tia/' + metoda_text[1])
    
  ## Vyber data 
  choosen = choosen_data_V(procenta, sorted_Vi, metoda_text,sestupne)
  

def strategy_F(metoda_text, procenta, sestupne):
  ## Najde F a seřadí jej
  F = find_F(metoda_text, sestupne)

  ## Najde cislo promluvy a nejpravdepodobnejsi semanticky strom a vytvori seznam
  seznam_promluv = create_list_of_trees(metoda_text)
  
  F_score = count_F_score(seznam_promluv, F)

  sorted_F = sorted(F_score, key=getKey, reverse = sestupne)
  
  ## Vyber data a přidej je k 10% trénovacích dat využitých v první fázi trénování (použita stejná funkce jako pro ppst)
  choosen = choosen_data_P(procenta, sorted_F, metoda_text)
  
def getKey(item):
   return item[0]


## PRÁCE S DATY
## ------------
## Funkce na úpravu dat

def count_F_score(seznam_promluv, F):
  count = 0
  F_score = 0
  count_F = 0
  for promluva in seznam_promluv:
      retezec = promluva[3]
      for koncept in F:
        hledanyKoncept = koncept[2]
        hledanyTzavorky = '(T)'
        if retezec.find(hledanyKoncept)>-1 and len(hledanyKoncept)>1:
           #print str(count) + ": Koncept: " + hledanyKoncept + ", Promluva: " + retezec
           F_score = F_score + koncept[0];
           count_F = count_F + 1; 
        elif retezec.find('('+koncept[2]+')')>-1 or retezec.find('('+koncept[2]+'(')>-1 or retezec.find(', '+koncept[2])>-1 or retezec.find(koncept[2]+',')>-1 or retezec.find(koncept[2])==0:
           #print str(count) + ": Koncept: " + hledanyKoncept + ", Promluva: " + retezec
           F_score = F_score + koncept[0];
           count_F = count_F + 1;
      count = count+1
      hodnotaFscore = F_score/count_F;
      #print hodnotaFscore
      F_score = 0
      count_F = 0
      promluva[0] = hodnotaFscore

  return seznam_promluv
  
def choosen_data_P(procenta, P, metoda_text):
  train10 = 'tia/'+metoda_text[1]+'/10_SCORE_train.scp'
  
  pocetPrvku = 1
  for radek in open(train10,'r'):
    pocetPrvku = pocetPrvku+1

  for i in procenta[:]:
    choosen = P[0:(pocetPrvku*(i-10)/10)]
    print choosen[0]
    print choosen[len(choosen)-1]
 
    print '---Vybráno '+ str(i-10) +'% dat---'

    add_data_seznam(choosen,metoda_text,i)
    
def prepare_data(metoda_text):
  # PŘIPRAVA DAT PRO VÝBĚR NOVÝCH TRÉNOVACÍCH DAT
  # Vezmeme 10% testovacích dat pro natrénovaní modelu 90% trénovacích
 
  print 'Příprava dat pro vyběr nových trénovacích dat'

  if not os.path.exists('tia/' + metoda_text[1]):
     os.makedirs('tia/'+ metoda_text[1])

  # Vytvoří list manuálních a reálných dat
  s = manual_and_real_data()
 
  train10 = 'tia/' + metoda_text[1] + '/10_train_SCORE.scp'
  test90 = 'tia/' + metoda_text[1] + '/90_test_SCORE.scp'
  zapis  = file(test90,'w')
   
  t=list()
  for line in open(train10,'r'):
    t.append(line)
  
  count = 1
  count2 = 1

  for x in s:
    count = count+1
    if x not in t:
       zapis.write(x)
       count2 = count2+1
  zapis.close()
  
  print 'Data připravena ' + str(count-count2) +' trénovacích dat a ' + str(count2) + ' testovacích dat'


def find_F(metoda_text,sestupne):
  F = []
  index = 1
  
  heldout = 'tmp_tia_baseline/' + metoda_text[1] + '/10_SCORE/heldout.Ydec.tia.transcribed_trns.hdm-3_10_SCORE.cdc.txt'
  ## Najdi F hodnoty a seřaď je
  for radek in open(heldout,'r'):
    if radek.find("F")>15 and radek.find("F")<20:
       index = radek.find("F")
       konec = radek.find(" ")
       if float(radek[index+3:index+7])>-0.01:
          F = F + [[float(radek[index+3:index+7]), str("'")+str(radek[0:konec])+str("'"), str(radek[0:konec]) ]]
  F.sort(reverse = sestupne)
  return F

def open_Dict():
  viSlovnik = 'tia/metoda4/90_slovnik.txt'
  
  Vi = {}
  for line in open(viSlovnik,'r'):
     stred = line.find(" ");
     prvni = line[0:stred]
     druhy = line[stred+1:len(line)]
     Vi[prvni] = druhy;
  
  sorted_Vi = sorted(Vi.iteritems(), key=operator.itemgetter(1))
  return sorted_Vi


def add_data(metoda_text,choosen,i):
  radky = []

  train10 = 'tia/' + metoda_text[2] + '/10_SCORE_train.scp'
  pripsani = 'tia/' + metoda_text[1] + '/'+str(i)+'_' + metoda_text[0] + '.scp'
  pripis = file(pripsani,'w')

  for radek in open(train10,'r'):
    pripis.write(radek)

    choosen.sort();
      
    for k in choosen:
       pripis.write(k[0]+'\n')
  print '---Pridano ' + str(len(choosen));

  pripis.close()
  print '---Pridano dalsich '+str((i-10))+'% dat---'

def find_P(metoda_text,sestupne):
  index = 1
  P = []
  
  nazev = 'tmp_tia_baseline/' + metoda_text[1] + '/10_' + metoda_text[0] + '/test.Ydec.tia.transcribed_trns.hdm-3_10_' + metoda_text[0] + '.nbest.py'
  
  for radek in open(nazev,'r'):
    if radek.find("[")!=-1 :
       index = radek.find("[")      
       konec = index-3;      
       P = P + [[float(radek[index+2:index+9]), int(radek[1:index-2])]]
  P.sort(reverse = sestupne)
  #print P
  return P


def manual_data():   
  manualni = 'tia/manualni.scp'

  s = list()
  for radek in file(manualni, 'r'):
    s.append(radek)
  return s

def real_data():   
  realna = 'tia/train.scp'

  s = list()
  for radek in file(realna, 'r'):
    s.append(radek)
  return s

def manual_and_real_data():
  # Vytvoří list manuálních a reálných dat
  manual = 'tia/manualni.scp'
  train = 'tia/train.scp'

  s=list()
  for line in open(manual,'r'):
    s.append(line)
  for line in open(train,'r'):
    s.append(line)
  return s
    
def choosen_data_V(procenta, sorted_Vi, metoda_text,sestupne):
  train10 = 'tia/metoda4/10_SCORE_train.scp'
  
  pocetPrvku = 1
  for radek in open(train10,'r'):
    pocetPrvku = pocetPrvku+1

  for i in procenta[:]:
    if (sestupne == True):
      choosen = sorted_Vi[(len(sorted_Vi)-pocetPrvku*((i-10)/10)): len(sorted_Vi)]
      ##print sorted_Vi[(len(sorted_Vi)-pocetPrvku*((i-10)/10))]
      ##print sorted_Vi[len(sorted_Vi)-1]
    else:
      choosen = sorted_Vi[1:(pocetPrvku*(i-10)/10)]
      ##  print sorted_Vi[1]
      ##  print sorted_Vi[(pocetPrvku*(i-10)/10)]
    print '---Vybráno '+ str(i-10) +'% dat---'

    add_data(metoda_text,choosen,i)
    
def add_data_seznam(choosen, metoda_text,i):
    seznam = []

    train10 = 'tia/'+ metoda_text[1] + '/10_SCORE_train.scp'
    pripsani = 'tia/' + metoda_text[1] + '/'+str(i)+'_train_' + metoda_text[0] + '.scp'
    test = 'tia/'+ metoda_text[1] + '/90_SCORE_test.scp'
    pripis = file(pripsani,'w')

    for radek in open(train10,'r'):
       pripis.write(radek)
   
    for o in choosen:
       seznam = seznam + [o[1]]
    seznam.sort()

    print '---Dat ' + str(len(seznam))      
    counter = 0
    prid = 0;
    for prvek in open(test,'r'):
       if len(seznam)>0 and (counter == int(seznam[0])):
          pripis.write(prvek)
          del seznam[0]
          prid = prid +1
       counter = counter+1
    print '---Pridano ' + str(prid) + ' dat z '  + str(counter) + ' testovacich';
 
    pripis.close()
    print '---Pridano dalsich '+str((i-10))+'% dat---'
    

def choose_data_F(metoda_text, seznam_promluv, F, procenta):
  train10 = 'tia/' + metoda_text[2] + '/10_SCORE_train.scp'

  pocetPrvku = 1   # počet trénovacích dat
  for radek in open(train10,'r'):
    pocetPrvku = pocetPrvku+1
  
  for i in procenta[:]:
    choosen = []

    potreba = pocetPrvku*(i-10)/10  
  
    aktualne = 1
    for h in range(0,len(F)):
      for k in range(0,len(seznam_promluv)):
        if seznam_promluv[k][3].find(F[h][2]) !=-1 and len(F[h][2])>2 and aktualne!=potreba and seznam_promluv[k] not in choosen:
           choosen.append(seznam_promluv[k])
           #print F[h][2] + ' v ' + seznam_promluv[k][3] + ' cislo ' + str(seznam_promluv[k][1])
           aktualne = aktualne + 1
        else:
          if seznam_promluv[k][2].find(F[h][1]) !=-1 and aktualne!=potreba and seznam_promluv[k] not in choosen:
              choosen.append(seznam_promluv[k])
              #print F[h][2] + ' v ' + seznam_promluv[k][3] + ' cislo ' + str(seznam_promluv[k][1])
              aktualne = aktualne + 1
    #  print nejhorsi[1]
    #  print nejhorsi[len(choosen)-1]

    ## Přidání vybraných dat k 10% dat vybraných k trénování v 1 fázi trénování
    add_data_seznam(choosen, metoda_text,i)
    
  print '---Vybráno '+ str((i-10)) +'% trénovacích dat---' 


def create_list_of_trees(metoda_text):
  test = 'tmp_tia_baseline/' + metoda_text[1] + '/10_SCORE/test.Ydec.tia.transcribed_trns.hdm-3_10_SCORE.nbest.py'
  index = 1
  seznam_promluv = []
  in_file = open(test,'r')
  for radek in in_file:
    if radek.find("[")!=-1:
       index = radek.find("[")
       ppst = float(radek[index+2:index+9]);
       ID = int(radek[1:index-2]);
       apostrof = radek.find("'")
       apostrof2 = radek.find("')")
       konec = index-3;
       if (apostrof == -1):
         radek = next(in_file)
         apostrof = radek.find("'")
         apostrof2 = radek.find("')")  
       # print 'radek' + radek
       seznam_promluv = seznam_promluv + [[ppst, ID, str(radek[apostrof:apostrof2+1]), str(radek[apostrof+1:apostrof2])]]
  #cisla = sorted(cisla,key=sort_key)
  #print cisla[0:20]     
  return seznam_promluv


def metacentrum(metoda_text,procenta,test):
  ##Vytvoření konfigurací
  create_configs(metoda_text,procenta,test)

  ## Vytvoření spouštěcích skriptů
  create_skripts(metoda_text,procenta)

  ## Reálné spuštění skriptů
  run(metoda_text,procenta)
  

def create_configs(metoda_text,procenta,test):
  if not os.path.exists('conf/' + metoda_text[1]):
    os.makedirs('conf/' + metoda_text[1])
    
  for i in procenta[:]:
    confNazev= 'conf/' + metoda_text[1] + '/tia.transcribed_trns.hdm-3_'+str(i)+'_' + metoda_text[0] + '.sh'
    conf=file(confNazev,'w')
    conf.write('TMP=tmp_tia_baseline/' + metoda_text[1] + '/'+str(i)+'_' + metoda_text[0] + ' \n \n')
    conf.write('PREP_FUNC=tia/prep.py \n \n')
    conf.write('ACT_CLSF=clsf/svc_precomputed_1C.py \n')
    conf.write('STC_CLSF=clsf/svc_precomputed_1C.py \n \n')
    conf.write('GEN_ARGS="--max-tuple-len=5 --max-ngram-len=3 --prune-tuples=30 --dim=normalized" \n \n')
    conf.write('DATA_PREFIX=tia/manualni_realna.txt \n \n')
    conf.write('TRAIN=tia/' + metoda_text[1] + '/'+str(i)+'_train_' + metoda_text[0] + '.scp \n \n') # pridano 10%dat
    conf.write('HELDOUT=tia/heldout.scp \n')
    conf.write('TEST='+test+'\n \n')
    conf.write('KERNEL_ARGS="--kernel-type=ngram_word --kernel-order=1 --kernel-min-order=1 --normalize" \n \n')
    conf.write('HDM_MODE=\'hdm-3\' \n \n')
    conf.write('EXP=tia.transcribed_trns.hdm-3_'+str(i)+'_' + metoda_text[0] + ' \n \n')
    conf.write('KERNEL=kernel.$EXP.mat \n \n')
    conf.write('RULE_THRESH=4 \n \n')
    conf.close() 
  print '---Konfigurace vytvořeny---'


def create_skripts(metoda_text,procenta):
  if not os.path.exists('pbs/' + metoda_text[1]):
    os.makedirs('pbs/' + metoda_text[1])
    
  for i in procenta[:]:
    pbsNazev= 'pbs/' + metoda_text[1] + '/hdm-3_transcribed_trns_' + str(i)+'_'+metoda_text[0]+'.sh'
    pbs=file(pbsNazev,'w')
    pbs.write('#!/bin/bash \n \n')
    pbs.write('#PBS -j oe \n \n')
    pbs.write('#PBS -l mem=2gb -l nodes=1:ppn=4:x86:linux:data-kky -l walltime=24h \n \n')
    pbs.write('module add intelcdk-12 \n \n')
    pbs.write('cd /data-kky/home/marketaj/hdm/ \n \n')
    pbs.write('export NJOBS=$PBS_NUM_PPN \n \n')
    pbs.write('CFG=conf/' + metoda_text[1] + '/tia.transcribed_trns.hdm-3_'+str(i)+'_'+metoda_text[0]+'.sh \n \n')
    pbs.write('./run.sh $CFG || exit 1 \n \n')
    pbs.close()
  print '---Spouštěcí skripty vytvořeny---'


def run(metoda_text,procenta):
  for i in procenta[:]: 
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='nympha.zcu.cz', username='marketaj', password='enjoystein24')
    stdin, stdout, stderr = ssh.exec_command('qsub hdm/pbs/'+ metoda_text[1] +'/hdm-3_transcribed_trns_'+str(i)+'_'+metoda_text[0]+'.sh') 
    for line in stdout:
          print '... ' + line.strip('\n')
    ssh.close()


## GRAFY
## -----
## Vykreslení grafů

def draw_graph(metoda_text, popisek_graph):
  procenta = [20,30,50]
  index_b = 1;
  index_m = 1;
  Acc_b = [];
  Acc_m = [];

  # ziskani hodnot z vyslednych souboru
  for i in procenta[:]:
    baseline = 'tmp_tia_baseline/metoda1/manualni_realna/'+str(i)+'_manualni_realna/test.Ydec.tia.transcribed_trns.hdm-3_' + str(i) +'_manualni_realna.cdc.txt'
    metoda = 'tmp_tia_baseline/'+ metoda_text[1] +'/'+str(i)+ '_' + metoda_text[0] + '/test.Ydec.tia.transcribed_trns.hdm-3_'+str(i)+ '_'+ metoda_text[0]+'.cdc.txt'
    
    for radek_b in file(baseline,'r'):
      if radek_b.find("Acc")!=-1 and radek_b.find("Acc")<24 :
        index_b = radek_b.find("Acc")
        print "Acc (baseline):", radek_b[index_b+4:index_b+9], "Procenta:", i
        Acc_b = Acc_b + [float(radek_b[index_b+4:index_b+9])]
        index_b = index_b + 1
       
    for radek_m in file(metoda,'r') :
      if radek_m.find("Acc")!=-1 and radek_m.find("Acc")<24 :
        index_m = radek_m.find("Acc")
        print "Acc (metoda):", radek_m[index_m+4:index_m+9], "Procenta:", i
        Acc_m = Acc_m + [float(radek_m[index_m+4:index_m+9])]
        index_m = index_m + 1
       
  x = np.array([10,20,30])
  y = np.array(Acc_m)
  z = np.array(Acc_b)

  names = ['10% +', '10','20','40']

  # sloupcovy graf
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.bar(x-1.25, y,width=2.5,color='#5ac3b6',align='center',label= popisek_graph)
  ax.bar(x+1.25, z,width=2.5,color='#bfdb79',align='center',  label='Baseline', hatch='//')
  ax.set_xticks([5,10,20,30])
  ax.set_xticklabels(names)

  # specifikace grafu
  plt.hold(True)
  plt.axis([5,30+3, 72.2, 85])
  plt.xlabel(u'Množství dat [%]')
  plt.ylabel(u'cAcc')
  plt.grid(True, which='both',axis='both')
  plt.legend(loc='upper left', numpoints = 1, prop={'size':16})
  plt.annotate(str(round(Acc_m[0],1)), xy=(7.7,  Acc_m[0]+0.2),fontsize = 16)
  plt.annotate(str(round(Acc_b[0],1)), xy=(10.2, Acc_b[0]+0.2),fontsize = 16)
  plt.annotate(str(round(Acc_m[1],1)), xy=(17.7, Acc_m[1]+0.2),fontsize = 16)
  plt.annotate(str(round(Acc_b[1],1)), xy=(20.2, Acc_b[1]+0.2),fontsize = 16)
  plt.annotate(str(round(Acc_m[2],1)), xy=(27.7, Acc_m[2]+0.2),fontsize = 16)
  plt.annotate(str(round(Acc_b[2],1)), xy=(30.2, Acc_b[2]+0.2),fontsize = 16)

  for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(16)
    
  plt.show()


def draw_graph_lines_single(metoda_text,popisek_graph,procenta):
  minimum = procenta[0]
  maximum = procenta[len(procenta)-1]

  Acc = []
  index = 1;

  for i in procenta[:]:
    nazev = 'tmp_tia_baseline/' + metoda_text[1]+ '/'+str(i)+'_' + metoda_text[0]+ '/test.Ydec.tia.transcribed_trns.hdm-3_' + str(i) +'_' + metoda_text[0]+ '.cdc.txt'
    soubor = file(nazev,'r') 
    for radek in soubor:
      if radek.find("Acc")!=-1 and radek.find("Acc")<24 :
         index = radek.find("Acc")
         print "Acc (baseline, " + metoda_text[0]+ ") : ", radek[index+4:index+9], "Procenta:", i
         Acc = Acc + [float(radek[index+4:index+9])]
         index = index + 1
    soubor.close()

  x = np.array(procenta)
  y = np.array(Acc)

  # calculate polynomial
  fit = np.polyfit(x, y, 4)
  poly = np.poly1d(fit)

  xp = np.linspace(minimum, maximum, 12)

  # vykresleni dat s logaritmickou stupnici
  plt.plot(procenta, Acc, 'o',color = '#bfdb79',label =popisek_graph)
  plt.plot(xp, poly(xp), '-', color = '#bfdb79', linewidth=2,)
  plt.xscale('log')
  plt.axis([minimum, maximum, (Acc[0]-3), Acc[(len(Acc)-1)]+5])
  plt.xlabel('Amount of real data [%]')
  plt.ylabel('Accuracy (Acc)')
  #plt.title('The dependence of Acc on the amount of real data (with manual data)')
  plt.legend(loc='best', numpoints = 1, prop={'size':16})
  plt.grid(True, which='both',axis='both')  
  plt.show()

