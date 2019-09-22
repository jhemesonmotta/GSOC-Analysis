# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:39:36 2019

@author: IMGADMIN
"""

import pandas as pd
dadosMale = pd.read_csv('gsoc_male.csv', header = None)

transacoes = []
for i in range (0,5980):  
    transacoes.append([str(dadosMale.values[i, j]) for j in range (0,3)])
    
from apyori import apriori
regras = apriori(transacoes, min_support = 0.005, min_confidence = 0.7, min_lift = 3, min_length = 2)

resultados = list(regras)

resultados2 = [list(x) for x in resultados]
resultadoFormatado = []

for j in range(0,44):
    resultadoFormatado.append([list(x) for x in resultados2[j][2]])

  
for z in range (0,44):
    print("\n")
    print("\n")
    print(resultadoFormatado[z])
    print("\n")
    print("\n")
    
resultadoFormatado