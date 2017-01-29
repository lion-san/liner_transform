# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 00:47:07 2017

@author: yokoi
"""

import math
import matplotlib.pyplot as plt

#vecA = -1.2
vecA = 0.8

out = []
x = []

c = 18.0
c2 = 15.0

while vecA <= 1.2:
    #tmp = (1 / math.pow(1 + math.pow(c- c*math.sqrt(vecA*vecA), 2), 2) + 1 / math.pow(1 + math.pow(c2- c2*math.sqrt(vecA*vecA), 2), 2)) / 2
    tmp = 1 / math.pow(1 + math.pow(c- c*math.sqrt(vecA*vecA), 2), 2)
    out.append(tmp)
    x.append(vecA)
    #print(vecA)
    print(tmp)
    vecA += 0.001
    
#Generate Graph
plt.figure(figsize=(10, 5), dpi=80, facecolor='w', edgecolor='k')
plt.title("Test Accelarate")
plt.xlabel("vecter")
plt.ylabel("val")

plt.grid(True)
plt.plot(x, out, label="ke-su")

plt.show()
