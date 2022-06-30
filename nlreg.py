import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from lmfit import Model

data = pd.read_csv("data/data_80.csv")

size = len(data["day"])
sum = [size]
temp = 0
for i in range(size):
    temp = temp + data.Infected[i]
    sum.append(temp)



#----------------different function------------------#

def funcS(beta, sum , t):
    return int(3e8*np.exp(((-beta) * t * sum[t])/3e8))

def funcI(gamma, t):
    return int(1*np.exp(-gamma*t))

def funcSlog(beta, data, t):
    return int(np.log(3)+8+((-beta * t * sum[t])/3e8))

guess = [0.01,1./10]

#----------------------------------------------------#

mymodel = Model(funcS)


#params = mymodel.make_params(a = guess[0], sum = sum)
#params['sum'].vary = False

res=0

y = np.empty(size)
y2 = np.empty(size)
y3 = np.empty(size)
ysolv = np.empty(size)

for i in range(size):
    y[i]=funcS(guess[0], sum, i)
    y2[i]=funcSlog(guess[0], sum, i)
    y3[i]=funcI(guess[1],i)
    #print(y[i])

#c,cov = curve_fit(inst.funcS, data["day"].values, data["suspected"].values, guess[0])
#print(c)

xdata = data["day"].values
ydata = data["suspected"].values

"""
result = mymodel.fit(ydata, params, x=xdata)
print(result.fit_report())
"""

plt.plot(data["day"],data["suspected"])
#plt.plot(data["day"],np.log(data["suspected"]))
#plt.plot(data["day"],data["Infected"])
plt.plot(data["day"],y,'r.')

"""
for i in range(size):
    ysolv[i]=funcS(c,data,i)
"""

#plt.plot(data["day"],ysolv,'r.')

plt.show()

