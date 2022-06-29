import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import csv


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


def deriv(y, t, N, beta, gamma): #SIR model
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

def noise(X,t,val): #function to add noise in the date
    return X

res = odeint(deriv, y0, t, args=(N, beta, gamma)) #using odeint to intigrate and solve
S, I, R = res.T

#to generate datasheets
size=int(input("How many data do you want to generate ? (number of days) : "))
print(size)

#data file
ficname="data_"+str(size)+".txt"
fic = open("data/"+ficname,"w")
for i in range(size):
    fic.write(str(i+1)+","+str(int(S[i]))+","+str(int(I[i]))+","+str(int(R[i]))+"\n")
fic.close()

#csv file
header = ['day','suspected', 'Infected','Recovered']
ficnamecsv="data_"+str(size)+".csv"

with open("data/"+ficnamecsv, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for i in range(size):
        data = [int(i+1),int(S[i]),int(I[i]),int(R[i])]
        writer.writerow(data)




#display
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number ')
ax.set_ylim(0, N)
ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()
