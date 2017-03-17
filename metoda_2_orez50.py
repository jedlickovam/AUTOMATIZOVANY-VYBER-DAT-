# -*- coding: cp1250 -*-

# Po�adavky :
#
# 1. Vstup: Adres�� tia a v n�m soubory manualni.scp a train.scp
# 2. P��stup k modelu HDM v datov�m �lo�i�ti metacentrum

# V�stup: Graf z�vislosti Acc na mnozstvi trenovacich dat

import funkce_DP

metoda_text = ['exp2','metoda2/exp2','metoda2']

##procenta = [10]

#### P��PRAVA DAT
#### -----------
#### 10% test, 90% train
##funkce_DP.prepare_data(metoda_text)

#### SPUS� �LOHU
#### -----------
#### Vytvo�en� konfigurac�, spou�t�c�ch skript� a odesl�n� �loh do metacentra
##funkce_DP.metacentrum(metoda_text,procenta)


procenta = [20,30,50]

#### PROVE� STRATEGII
#### ----------------
#### �azen� vzestupn�, orez
##
##sestupne = False
##orez7 = False
##orez50 = True
##funkce_DP.strategy_P(metoda_text, procenta, sestupne, orez7, orez50)

#### SPUS� �LOHY
#### -----------
#### Vytvo�en� konfigurac�, spou�t�c�ch skript� a odesl�n� �loh do metacentra
##funkce_DP.metacentrum(metoda_text,procenta)

## VYHODNOCEN� DAT 
## ---------------
popisek_graph = u'Selekce neur�it�ch dat (50%)'
funkce_DP.draw_graph(metoda_text,popisek_graph)





