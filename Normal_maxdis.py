# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 17:21:46 2020

@author: ajyis
"""


import gurobipy as gp
from gurobipy import GRB
import sys
import numpy as np
import pandas as pd
sys.stdout = open('new_Normal_max_72hr.txt', 'w')
import sys

import matplotlib.pyplot as plt


#read data
population = pd.read_csv('Pop_centroid_allegheny_county.csv')
POD_sites = pd.read_excel('POD Sites.xlsx')


households = np.array(population['Households'])
capacity = np.array(POD_sites['Capacity accomodated in 72 hours'].astype(int))
distance = np.loadtxt('distance_matrix_miles.csv', delimiter=',')
distance=distance.T



m = gp.Model()

### Setting up Decision Variables ###

#set indices for variables
areas = range(0,402)
PODS = range(0,47)

# Define variables
x = m.addVars(PODS, vtype=GRB.BINARY, name ="shelter") # 1 if shelter j is built
y = m.addVars(areas,PODS, vtype=GRB.BINARY, name ="i assigned to j") # 1 if i assigned to j 
max_dis = m.addVars(1,1,lb=0.0)




#Minimax constraint:
m.addConstrs(((x[j] * y[i,j] * distance[i,j]) <= max_dis[0,0] for i in areas for j in PODS), name = "Minimax constraint")


for j in PODS:
     m.addConstr(sum(households[i]*y[i,j] for i in areas) <= x[j]*capacity[j])

# All residential areas are alloted a shelter site
# Do not assign j if j does not exist
#m.addConstrs((y[i,j] <= x[j] for i in areas for j in PODS), name = "Assign if Exists") 
m.addConstr(sum(sum(y[i,j] for j in PODS) for i in areas) >= 402)  

# Every area gets a shelter
m.addConstrs((sum(y[i,j] for j in PODS ) == 1 for i in areas), name = "One shelter for each area")
    
# Sensitivity Analysis - limit max number of PODs through all possibilities   
max_dist =[]
results = []


for k in range(47, 0, -1):
    print("Max Number of PODs = ", k)
    #k PODS build
    m.addConstr((sum(x[j] for j in PODS)<= k), name = "Max PODS")
    
    
    ### Set Objective
    m.setObjective(max_dis[0,0])
    m.modelSense = GRB.MINIMIZE
    
    #set model time limit to 5 min
    m.Params.TimeLimit = 300    

    #optimize
    m.optimize()
    print("\n")
    
    if hasattr(m, 'objVal'):
        max_dist.append((k, m.objVal))
        for v in m.getVars():
            if v.X > 0:
                indicies = v.varName.split('[')
                #ind = indicies[1].rstrip(']')
                results.append(indicies)
        print("\n")
        
    else:
        max_dist.append((k, "Infeasible"))
        results.append((k, "Infeasible"))        
        print("\n")
    

           


df = pd.DataFrame(max_dist, columns=['k','Maximum Distance'])
df.to_csv('objval_normal_max_distancing.csv', index=False)

df2 = pd.DataFrame(results)
df2.to_csv('assignments_max_normal_distancing.csv', index=False)

print("\n")
print("\n")
    

