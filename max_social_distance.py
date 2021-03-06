import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd

#import sys
#sys.stdout = open('report_social_distance_max_72hr.txt', 'w')

#import os
#os.chdir('C:/Users/Lara/Documents/Fall_2020/_Decision_Analytics/_project')

#read data
population = pd.read_csv('Pop_centroid_allegheny_county.csv')
POD_sites = pd.read_excel('POD Sites.xlsx')

households = np.array(population['Households'])
capacity = np.array(POD_sites['Max population accomodated in 72 hours'].astype(int))
distance = np.loadtxt('distance_matrix_miles.csv', delimiter=',')
distance=distance.T

#set up model object
m = gp.Model()

### Setting up Decision Variables ###

#set indices for variables
areas = range(0,402)
pods = range(0,47)

# Define variables
x = m.addVars(pods, vtype=GRB.BINARY, name ="PODs") # 1 if shelter j is built
y = m.addVars(areas,pods, vtype=GRB.BINARY, name ="i assigned to j") # 1 if i assigned to j
max_dis = m.addVars(1,1,lb=0.0)

#### Constraints

#Minimax constraint:
m.addConstrs(((x[j] * y[i,j] * distance[i,j]) <= max_dis[0,0] for i in areas for j in pods), name = "Minimax constraint")

for j in pods:
     m.addConstr(sum(households[i]*y[i,j] for i in areas) <= x[j]*capacity[j])

# Do not assign j if j does not exist
m.addConstrs((y[i,j] <= x[j] for i in areas for j in pods), name = "Assign if Exists")

# Every area gets a shelter
m.addConstrs((sum(y[i,j] for j in pods ) == 1 for i in areas), name = "One shelter for each area")
       
# Sensitivity Analysis - limit max number of PODs through all possibilities
max_dist =[]
results = []

for k in range(47, 0, -1):
    print("Max Number of PODs = ", k)
    #Only 10 shelters build
    m.addConstr((sum(x[j] for j in pods)<= k), name = "Max PODs")
    
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

           
df2 = pd.DataFrame(results) #[31:])
df2.to_csv('assignments_max_social_distancing.csv', index=False)

df = pd.DataFrame(max_dist, columns=['k','Maximum Distance'])
df.to_csv('objval_max_social_distancing.csv', index=False)

print("\n")
print("\n")
