# -*- coding: cp1250 -*-

# Po�adavky :
#
# 1. Adres�� tia a v n�m soubory manualni.scp a train.scp
# 2. P��stup k modelu HDM v datov�m �lo�i�ti metacentrum

# V�stup: Graf z�vislosti Acc na mnozstvi trenovacich dat

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

#### PROVE� STRATEGII
#### ----------------
##manual = True
##real = False
##funkce_DP.strategy_random(metoda_text,procenta,manual,real)

#### SPUS� �LOHY
#### -----------
#### Vytvo�en� konfigurac�, spou�t�c�ch skript� a odesl�n� �loh do metacentra
##funkce_DP.metacentrum(metoda_text,procenta)

## VYHODNOCEN� DAT 
## ---------------
popisek_graph = 'Baseline, manual data'

funkce_DP.draw_graph_lines_single(metoda_text,popisek_graph,procenta)




