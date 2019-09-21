# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:39:36 2019

@author: IMGADMIN
"""

import pandas as pd
dados = pd.read_csv('mercado2.csv', header = None)


transacoes = []
for i in range (0,7501):  
    transacoes.append([str(dados.values[i, j]) for j in range (0,20)])
    
from apyori import apriori
regras = apriori(transacoes, min_support = 0.003, min_confidence = 0.5, min_lift = 3, min_length = 2)

resultados = list(regras)
resultados

resultados2 = [list(x) for x in resultados]
resultadoFormatado = []

for j in range(0,28):
    resultadoFormatado.append([list(x) for x in resultados2[j][2]])
    
resultadoFormatado