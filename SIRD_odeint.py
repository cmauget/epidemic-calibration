#wip

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import csv
import random


N = 3e8 #population

I0 = 1 #Initial number of infected
R0 = 0 #Initial number of recovered
D0 = 0 #Initial number of quarantined
S0 = N - I0 - R0 #initial number of susceptible
y0 = S0, I0, R0, D0


#parameters (to determine)
beta = 0.75 #contact rate
gamma = 1./10 #recovered rate
k = 1./100 #chance of dying


n=175 #number of days
t = np.linspace(0, n, n) #timeseries (\days)

#SIR model
def deriv(y, t, N, beta, gamma, k) : 
    S, I, R, D = y
    dSdt = -beta * S * I / N 
    dIdt = beta * S * I / N - gamma * I - k * I 
    dRdt = gamma * I 
    dDdt = k * I 
    return dSdt, dIdt, dRdt, dDdt

#simple function to add noise
def noise(S,I,R,D,val,n,N): 
    for i in range(n):
        noise1 = (val/100)*N*random.random()
        frac1 = random.random()
        frac2 = random.random()
        ni = noise1
        ns = ni * frac1
        nr = ni * (1 - frac1)*frac2
        nx = ni * (1 -frac1)*(1-frac2)
        I[i] = I[i] + ni
        S[i] = S[i] - ns
        R[i] = R[i] - nr
        D[i] = D[i] - nx
    return abs(S) , I , abs(R) , abs(D)


#using odeint to intigrate and solve
res = odeint(deriv, y0, t, args=(N, beta, gamma, k)) 
S, I, R, D = res.T
print(I)
#user input for noise
if int(input("Do you want to add noise ? (yes = 0) : ")) == 0 :
    S, I, R, D = noise(S,I,R,D,4,n,N)

#to generate datasheets
if int(input("Do you want to generate data ? (yes = 0) : ")) == 0 :
    #txt dile
    size=int(input("How many data do you want to generate ? (number of days) : "))
    print(size)

    if int(input("Enter 1 for a .txt, 0 for a .csv : ")) == 1 :
        #txt file
        ficname="data_SIRD_"+str(size)+".txt"
        fic = open("data/"+ficname,"w")
        for i in range(size):
            fic.write(str(i+1)+","+str(int(S[i]))+","+str(int(I[i]))+","+str(int(R[i]))+","+str(int(D[i]))+"\n")
        fic.close()

    else : 
    #csv file
        header = ['Day','Suspected', 'Infected','Recovered','Death']
        ficnamecsv="data_SIRD_"+str(size)+".csv"

        with open("data/"+ficnamecsv, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for i in range(size):
                data = [int(i+1),int(S[i]),int(I[i]),int(R[i]),int(D[i])]
                writer.writerow(data)


#display
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.plot(t, D, 'y', alpha=0.5, lw=2, label='Death')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number ')
ax.set_ylim(0, N*1.1)
ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()
