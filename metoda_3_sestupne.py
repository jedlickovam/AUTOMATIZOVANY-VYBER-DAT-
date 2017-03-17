# -*- coding: cp1250 -*-

# Požadavky :
#
# 1. Vstup: Adresář tia a v něm soubory manualni.scp a train.scp
# 2. Přístup k modelu HDM v datovém úložišti metacentrum

# Výstup: Graf závislosti Acc na mnozstvi trenovacich dat

import funkce_DP

metoda_text = ['worst3','metoda3/worst','metoda3']

procenta = [10]

#### PŘÍPRAVA DAT
#### -----------
#### 10% test, 90% train
##funkce_DP.prepare_data(metoda_text)

#### SPUSŤ ÚLOHU
#### -----------
#### Vytvoření konfigurací, spouštěcích skriptů a odeslání úloh do metacentra
##metoda_text_priprava = ['SCORE','metoda3/worst']
##test = 'tia/metoda3/worst/90_test_SCORE.scp'
##funkce_DP.metacentrum(metoda_text_priprava,procenta,test)

procenta = [20,30,50]

## PROVEĎ STRATEGII
## ----------------
## řazení sestupně

sestupne = True 
funkce_DP.strategy_F(metoda_text,procenta,sestupne)

#### SPUSŤ ÚLOHY
#### -----------
#### Vytvoření konfigurací, spouštěcích skriptů a odeslání úloh do metacentra
##test = 'tia/test.scp'
##funkce_DP.metacentrum(metoda_text,procenta,test)


## VYHODNOCENÍ DAT 
## ---------------
popisek_graph = u'Selekce dle F-skóre'
funkce_DP.draw_graph(metoda_text,popisek_graph)

