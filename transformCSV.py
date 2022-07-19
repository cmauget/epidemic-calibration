import pandas as pd
import numpy as np

"""
RMQ A CLEM: 
J ai crée test pour vérifier que ça marche et c'est bon mais quand je fais tourner les algos avec les données 
réelles les résultats sont incohérents. C'est sans doute parce qu'il ya trop de données.
"""

ficdata = "covid-19/test.csv"
data = pd.read_csv(ficdata)
nbPara=4

day = data.head(0)
lday=list(day)
del lday[0:nbPara]
#print(lday)

infected = []
for i in lday :
	temp = data[i]
	tempp = list(temp)
	infected.append(sum(tempp))
#print(infected)

df = pd.DataFrame({'DAY':lday,'CASE_COUNT':infected})
df.to_csv('data/test.csv', index=False)
#print(df['CASE_COUNT'])
