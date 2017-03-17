# -*- coding: cp1250 -*-

# Po�adavky :
#
# 1. Vstup: Adres�� tia a v n�m soubory manualni.scp a train.scp
# 2. P��stup k modelu HDM v datov�m �lo�i�ti metacentrum

# V�stup: Graf z�vislosti Acc na mnozstvi trenovacich dat

import funkce_DP

metoda_text = ['realna','metoda1/realna','metoda1']
procenta = [5,10,20,30,40,50,60,70,80,90,100]
Acc = []

###### PROVE� STRATEGII
###### ----------------
##manual = False
##real = True
##funkce_DP.strategy_random(metoda_text,procenta,manual,real)

#### SPUS� �LOHY
#### -----------
#### Vytvo�en� konfigurac�, spou�t�c�ch skript� a odesl�n� �loh do metacentra
##funkce_DP.metacentrum(metoda_text,procenta)

## VYHODNOCEN� DAT 
## ---------------
popisek_graph = 'Baseline, real data'

funkce_DP.draw_graph_lines_single(metoda_text,popisek_graph,procenta)

