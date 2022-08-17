#FIRST PARAMETER MUST BE FROM S TO I

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import csv


def init(test): #initialise the data

    if test:
        size = 5
        name_tab = ["Suspected", "Infected", "Recovered", "Vacinated", "Death"]
        cor_tab = np.array([[0,1,0,1,0], [0,0,1,0,1], [0,0,0,0,0], [0,1,0,0,0], [0,0,0,0,0]])
        params = np.array([0.5, 1./500, 1./10, 1./100, 0])

        N = 3e8 #population
        I0 = 1 #Initial number of infected
        R0 = 0 #Initial number of recovered
        S0 = N - I0 - R0 #initial number of recovered
        y0 = S0, I0, R0, 0, 0

        n=175

        t = np.linspace(0, n, n) #timeseries (\days)

    else:

        size=int(input("Enter the number of compartment wanted : "))
        cor_tab = np.zeros(shape=(size,size))
        name_tab = []
        for i in range(size):
            name_tab.append(input("Enter the name of the "+str(i+1)+" compartment : "))

    return name_tab, cor_tab, size, params, y0, N, n, t
    

def model_deriv(y , t, N, params, cor_tab, size):
    
    #print(y)
    dy = np.zeros(size)
    ind=0
    
    for i in range(size):
        for j in range(size):
            if cor_tab[i][j]==1: 
                if ((i==0) and (j==1)):
                    dy[i]=dy[i]-params[ind]*y[i]*y[1]/N
                    dy[j]=dy[j]+params[ind]*y[i]*y[1]/N
                else:
                    dy[i]=dy[i]-params[ind]*y[i]
                    dy[j]=dy[j]+params[ind]*y[i]
                ind+=1
    return dy


def data_gen(name_tab, size, result, n):

    header = name_tab
    ficnamecsv="data_gen.csv"

    with open("calibration/data/"+ficnamecsv, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
       
        for i in range(n):
            
            data = np.zeros(size)

            for j in range (size):
                data[j] = int(result[j][i])

            writer.writerow(data)


#------------------------Main-----------------------#

test = True #Easier testing removing human input


name_tab, cor_tab, size, params, y0 , N, n, t = init(test)

res = odeint(model_deriv, y0, t, args=(N, params, cor_tab, size)) 
result = res.T

data_gen(name_tab, size, result, n)

for i in range(size):
    plt.plot(t, result[i,:], alpha=0.5, lw=2, label=name_tab[i])
plt.legend()
plt.show()