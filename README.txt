# Point of Dispense (POD) Optimization for Public Health Emergencies in Allegheny County

## Introduction

Our aim is to build a model that helps in finding the best way to choose Point-of-Dispense (POD) sites to reach all the residents in the county in case of a public health emergency.


## Code files

There are three data files that need to be read:
1) Pop_centroid_allegheny_county.csv
2) POD Sites.xlsx
3) distance_matrix_miles.csv

Since we have two scenarios and two different objectives for each, there are a total of 4 python files, one for each objective and scenario.

1) Normal_min_dis.py
    It is the model for full capacity scenario for the total minimum distance objective.

2) Normal_maxdis.py
     It is the model for full capacity scenario for the minmax distance objective.

3) total_social_distance.py
     It is the model for social distancing scenario for the total minimum distance objective.

4) max_social_distance.py
     It is the model for social distancing scenario for the minmax distance objective.

## Prerequisites

The packages you need to run the files:
-gurobipy
-sys
-numpy
-pandas


## Contributers

Ajay Valecha, Akshay Oza, Chetna Bakhshi, & Lara Haase
