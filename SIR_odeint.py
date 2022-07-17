import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import csv
import random


N = 3e8 #population

I0 = 1 #Initial number of infected
R0 = 0 #Initial number of recovered
S0 = N - I0 - R0 #initial number of recovered
y0 = S0, I0, R0


#parameters (to determine)
beta = 0.5 #contact rate
gamma = 1./10 #recovered rate

n=175 #number of days
t = np.linspace(0, n, n) #timeseries (\days)

#SIR model
def deriv(y, t, N, beta, gamma): 
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

#simple function to add noise
def noise(S,I,R,val,n,N): 
    for i in range(n):
        ni = I[i]*(val/100)*random.random()
        frac1 = random.random()
        ns = ni * frac1
        nr = ni * (1 - frac1)
        I[i] = I[i] + ni
        S[i] = S[i] - ns
        R[i] = R[i] - nr
    return abs(S) , I , abs(R)


#using odeint to intigrate and solve
res = odeint(deriv, y0, t, args=(N, beta, gamma)) 
S, I, R = res.T

noise_name = "" #define the name of the output file if there is noise

#user input for noise
if int(input("Do you want to add noise ? (yes = 1) : ")) == 1 :
    S, I, R = noise(S,I,R,4,n,N)
    noise_name = "_n"

#to generate datasheets
if int(input("Do you want to generate data ? (yes = 1) : ")) == 1 :
    #txt dile
    size=int(input("How many data do you want to generate ? (number of days) : "))
    print("Simulated number fo days : "+str(size))

    if int(input("Enter 1 for a .txt, 0 for a .csv : ")) == 1 :
        #txt file
        ficname="data_SIR_"+str(size)+noise_name+".txt"
        fic = open("data/"+ficname,"w")
        for i in range(size):
            fic.write(str(i+1)+","+str(int(S[i]))+","+str(int(I[i]))+","+str(int(R[i]))+"\n")
        fic.close()

    else : 
    #csv file
        header = ['Day','Suspected', 'Infected','Recovered']
        ficnamecsv="data_SIR_"+str(size)+noise_name+".csv"

        with open("data/"+ficnamecsv, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for i in range(size):
                data = [int(i+1),int(S[i]),int(I[i]),int(R[i])]
                writer.writerow(data)
    print("Data succesfully created")


#display
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number ')
ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()
