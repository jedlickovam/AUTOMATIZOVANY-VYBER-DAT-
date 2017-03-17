# -*- coding: cp1250 -*-

# Požadavky :
#
# 1. Vstup: Adresář tia a v něm soubory manualni.scp a train.scp
# 2. Přístup k modelu HDM v datovém úložišti metacentrum

# Výstup: Graf závislosti Acc na mnozstvi trenovacich dat

import funkce_DP

metoda_text = ['realna','metoda1/realna','metoda1']
procenta = [5,10,20,30,40,50,60,70,80,90,100]
Acc = []

###### PROVEĎ STRATEGII
###### ----------------
##manual = False
##real = True
##funkce_DP.strategy_random(metoda_text,procenta,manual,real)

#### SPUSŤ ÚLOHY
#### -----------
#### Vytvoření konfigurací, spouštěcích skriptů a odeslání úloh do metacentra
##funkce_DP.metacentrum(metoda_text,procenta)

## VYHODNOCENÍ DAT 
## ---------------
popisek_graph = 'Baseline, real data'

funkce_DP.draw_graph_lines_single(metoda_text,popisek_graph,procenta)

