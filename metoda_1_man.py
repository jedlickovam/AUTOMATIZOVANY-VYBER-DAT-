# -*- coding: cp1250 -*-

# Požadavky :
#
# 1. Adresář tia a v něm soubory manualni.scp a train.scp
# 2. Přístup k modelu HDM v datovém úložišti metacentrum

# Výstup: Graf závislosti Acc na mnozstvi trenovacich dat

import matplotlib.pyplot as plt
import numpy as np
import scipy
import random
import os
import paramiko
import funkce_DP

metoda_text = ['manualni','metoda1/manualni','metoda1']

procenta = [30,40,50,60,70,80,90,100]
Acc = []

#### PROVEĎ STRATEGII
#### ----------------
##manual = True
##real = False
##funkce_DP.strategy_random(metoda_text,procenta,manual,real)

#### SPUSŤ ÚLOHY
#### -----------
#### Vytvoření konfigurací, spouštěcích skriptů a odeslání úloh do metacentra
##funkce_DP.metacentrum(metoda_text,procenta)

## VYHODNOCENÍ DAT 
## ---------------
popisek_graph = 'Baseline, manual data'

funkce_DP.draw_graph_lines_single(metoda_text,popisek_graph,procenta)




