# -*- coding: cp1250 -*-

# Požadavky :
#
# 1. Vstup: Adresář tia a v něm soubory manualni.scp a train.scp
# 2. Přístup k modelu HDM v datovém úložišti metacentrum

# Výstup: Graf závislosti Acc na mnozstvi trenovacich dat

import matplotlib.pyplot as plt
import numpy as np
import scipy
import random
import os
import paramiko
import funkce_DP

metoda_text = ['SCORE_final','metoda2/best','metoda2']

procenta = [10]

#### PŘÍPRAVA DAT
#### -----------
#### 10% test, 90% train
##funkce_DP.prepare_data(metoda_text)

#### SPUSŤ ÚLOHU
#### -----------
#### Vytvoření konfigurací, spouštěcích skriptů a odeslání úloh do metacentra
##funkce_DP.metacentrum(metoda_text,procenta)


procenta = [20,30,50]

#### PROVEĎ STRATEGII
#### ----------------
#### řazení vzestupně
##
##sestupne = False
##orez7 = False
##orez50 = False
##funkce_DP.strategy_P(metoda_text, procenta, sestupne, orez7, orez50)

#### SPUSŤ ÚLOHY
#### -----------
#### Vytvoření konfigurací, spouštěcích skriptů a odeslání úloh do metacentra
##funkce_DP.metacentrum(metoda_text,procenta)

## VYHODNOCENÍ DAT 
## ---------------
popisek_graph = u'Selekce neurčitých dat'
funkce_DP.draw_graph(metoda_text, popisek_graph)







