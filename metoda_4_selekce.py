# -*- coding: cp1250 -*-

# Po�adavky :
#
# 1. Vstup: Adres�� tia a v n�m soubory manualni.scp a train.scp
# 2. P��stup k modelu HDM v datov�m �lo�i�ti metacentrum

# V�stup: Graf z�vislosti Acc na mnozstvi trenovacich dat

import funkce_DP

metoda_text = ['slovnik3','metoda4/selekce','metoda4']

procenta = [20,30,50]

#### PROVE� STRATEGII
#### ----------------
#### �azen� vzestupn�, orez
##
##orez = True
##sestupne = False
##funkce_DP.strategy_V(metoda_text,procenta,sestupne,orez)

#### SPUS� �LOHY
#### -----------
#### Vytvo�en� konfigurac�, spou�t�c�ch skript� a odesl�n� �loh do metacentra
##funkce_DP.metacentrum(metoda_text,procenta)


## VYHODNOCEN� DAT 
## ---------------
popisek_graph = u'Selekce dle m�ry ' + r'$V_{u}$'

funkce_DP.draw_graph(metoda_text,popisek_graph)



