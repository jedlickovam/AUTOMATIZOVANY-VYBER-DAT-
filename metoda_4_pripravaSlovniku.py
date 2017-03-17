# -*- coding: cp1250 -*-

# Požadavky :
#
# Adresář tia a v něm soubory manualni.scp, train.scp, 10_SCORE_train.scp
# z pradchozi metody (manualni_10_realna.scp) pro lepsi porovnani metod
# Data

import funkce_DP

def vytvorSlovnik(promluva):
   promluvaNew = "";

   while promluva and promluva.find("<")!=-1 :
      zacatek = promluva.find("<");
      konec = promluva.find(">");
      promluva = promluva.replace(promluva[zacatek:konec+1],"");
         
   while promluva and promluva.find("  ")!=-1 :
      promluva = promluva.replace("  "," ");
        
   while promluva and promluva.find('\t')!=-1 :  # while promluva znamena zda retezec neni prazdny (luxusni podminka)
      promluva = promluva.replace('\t',"");

   while promluva and promluva.find('\n')!=-1 :
      promluva = promluva.replace('\n',"");

   # dle mezer vytvoř slovník

   if promluva:
      promluvaNew = promluva.split(' ');

      while "" in promluvaNew: promluvaNew.remove("")

      # print promluvaNew
      # print " "
   return promluvaNew

# PŘIPRAVA DAT PRO VÝBĚR NOVÝCH TRÉNOVACÍCH DAT
# vezmeme 10% testovacich dat pro natrénovaní modelu 90% trenovacich

metoda_text=['best','metoda4/best','metoda4']

funkce_DP.prepare_data(metoda_text)

nazev3 = 'tia/metoda4/10_SCORE_train.scp'
nazev4 = 'tia/metoda4/90_SCORE_test.scp'

# Nyní spočteme slovník pro 10% trénovacich dat

prepisy = 'tia/manualni_realna.txt'

s=list()
for line in open(nazev3,'r'):
  s.append(line)

t=list()
for line in open(prepisy,'r'):
  t.append(line)

slovnikV = list();
idxSlovniku = 0;

for line in s:
      stred = line.find('/')
      
      prvni = line[0:stred]            
      druhy = line[stred+1:len(line)-1]

      idx = 0;
      for radek in t:
         idx = idx+1;
         if radek.find(prvni) != -1:
            while idx < len(t) and t[idx].find(druhy) ==-1: # podmnínka idx < len(t) pro opakujici se ID ale jine podsloupnosti ID
              idx = idx + 1;

            if idx < len(t):
              promluva = t[idx+1]

              # print promluva
            
              promluvaSlovnik = vytvorSlovnik(promluva)
              
              # vytvori velkej slovnik
              for k in xrange(len(promluvaSlovnik)):
                if promluvaSlovnik[k] not in slovnikV :
                  slovnikV.append(promluvaSlovnik[k]);

# print slovnikV;
print 'Slovnik V vytvořen'

# Pro každou promluvu ze zbytku spočítám její malý slovníček Vi

nazev5 = 'tia/metoda4/90_slovnik.txt'
zapis  = file(nazev5,'w')

p90 =list()
for line in open(nazev4,'r'):
  p90.append(line)

for line in p90:
      stred = line.find('/')
      
      prvni = line[0:stred]            
      druhy = line[stred+1:len(line)-1]

      idx = 0;
      for radek in t:
         idx = idx+1;
         if radek.find(prvni) != -1:
            while idx < len(t) and t[idx].find(druhy) ==-1: # podmnínka idx < len(t) pro opakujici se ID ale jine podsloupnosti ID
              idx = idx + 1;

            if idx < len(t):
              promluva = t[idx+1]

              # print promluva
            
              promluvaSlovnik = vytvorSlovnik(promluva)
            
              # zkontroluj kolik jich je ve slovniku spocti cislo a vytvor přehlednej seznam 
              pocet = 0
                  
              for k in xrange(len(promluvaSlovnik)):
                if promluvaSlovnik[k] in slovnikV:
                  pocet = pocet+1;

              if len(promluvaSlovnik)>0:
                  cisloVi = pocet/float(len(promluvaSlovnik))
               
                  newLine = prvni + '/' + druhy + ' ' + str(cisloVi) + '\n'
                  zapis.write(newLine)
zapis.close()
print 'Slovnik90 vytvoren'
