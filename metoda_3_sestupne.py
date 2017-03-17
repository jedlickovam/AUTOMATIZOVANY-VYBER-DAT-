# -*- coding: cp1250 -*-

# Po�adavky :
#
# 1. Vstup: Adres�� tia a v n�m soubory manualni.scp a train.scp
# 2. P��stup k modelu HDM v datov�m �lo�i�ti metacentrum

# V�stup: Graf z�vislosti Acc na mnozstvi trenovacich dat

import funkce_DP

metoda_text = ['worst3','metoda3/worst','metoda3']

procenta = [10]

#### P��PRAVA DAT
#### -----------
#### 10% test, 90% train
##funkce_DP.prepare_data(metoda_text)

#### SPUS� �LOHU
#### -----------
#### Vytvo�en� konfigurac�, spou�t�c�ch skript� a odesl�n� �loh do metacentra
##metoda_text_priprava = ['SCORE','metoda3/worst']
##test = 'tia/metoda3/worst/90_test_SCORE.scp'
##funkce_DP.metacentrum(metoda_text_priprava,procenta,test)

procenta = [20,30,50]

## PROVE� STRATEGII
## ----------------
## �azen� sestupn�

sestupne = True 
funkce_DP.strategy_F(metoda_text,procenta,sestupne)

#### SPUS� �LOHY
#### -----------
#### Vytvo�en� konfigurac�, spou�t�c�ch skript� a odesl�n� �loh do metacentra
##test = 'tia/test.scp'
##funkce_DP.metacentrum(metoda_text,procenta,test)


## VYHODNOCEN� DAT 
## ---------------
popisek_graph = u'Selekce dle F-sk�re'
funkce_DP.draw_graph(metoda_text,popisek_graph)

