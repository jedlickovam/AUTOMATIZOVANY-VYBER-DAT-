# -*- coding: cp1250 -*-

# Požadavky :
#
# 1. Vstup: Adresář tia a v něm soubory manualni.scp a train.scp
# 2. Přístup k modelu HDM v datovém úložišti metacentrum

# Výstup: Graf závislosti Acc na mnozstvi trenovacich dat

import funkce_DP

metoda_text = ['slovnik3','metoda4/selekce','metoda4']

procenta = [20,30,50]

#### PROVEĎ STRATEGII
#### ----------------
#### řazení vzestupně, orez
##
##orez = True
##sestupne = False
##funkce_DP.strategy_V(metoda_text,procenta,sestupne,orez)

#### SPUSŤ ÚLOHY
#### -----------
#### Vytvoření konfigurací, spouštěcích skriptů a odeslání úloh do metacentra
##funkce_DP.metacentrum(metoda_text,procenta)


## VYHODNOCENÍ DAT 
## ---------------
popisek_graph = u'Selekce dle míry ' + r'$V_{u}$'

funkce_DP.draw_graph(metoda_text,popisek_graph)



