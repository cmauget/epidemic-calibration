import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from lmfit import Model

ficdata = "data/data_SIRX_54.csv"
data = pd.read_csv(ficdata)

print("Loading "+ficdata+"...")

size = len(data["Day"])
sum = [size]
temp = 0

train_size = 42

for i in range(size):
    temp = temp + data.Infected[i]
    sum.append(temp)



#----------------different function------------------#

def funcS(beta, sum , t):
    return int(3e8*np.exp(((-beta) * t * sum[t])/3e8))

def funcI(beta, gamma, t):
    return np.exp((beta - gamma )*t)

def funcIC(delta, t):
    return 1 + np.exp(delta*t)

def funcIClm(t, delta):
    return 1 + np.exp(delta*t)

def funcICO(delta, org, t):
    return org + np.exp(delta*t)

def funcSlog(beta, data, t):
    return int(np.log(3)+8+((-beta * t * sum[t])/3e8))

guess = [0.5,1./10]
g = 0.3

#----------------------------------------------------#

mymodel = Model(funcIClm)
params = mymodel.make_params(delta = g)

res=0#params['sum'].vary = False

y = np.empty(size)
y2 = np.empty(size)
y3 = np.empty(size)
ysolv = np.empty(size)
ysolv2 = np.empty(size)

for i in range(size):
    y[i]=funcS(guess[0], sum, i)
    y2[i]=funcSlog(guess[0], sum, i)
    y3[i]=funcI(guess[0],guess[1],i)
    #print(y[i])

xdata = data["Day"].to_numpy().copy()
ydata = data["Infected"].to_numpy().copy()

xdata = np.resize(xdata,train_size)
ydata = np.resize(ydata,train_size)


c,cov = curve_fit(funcIC,xdata, ydata)
print(c)

c2,cov2 = curve_fit(funcICO, xdata , ydata )
print(c2)


for i in range(size):
    ysolv[i]=funcIC(c,i)
    ysolv2[i]=funcICO(c2[1],c2[0],i)





result = mymodel.fit(ydata, params, t=xdata)
print(result.fit_report())


print(data["Infected"])
#display
#plt.plot(data["Day"],data["Infected"],"r.",label="Data")
#plt.plot(xdata ,ydata,"b.",label="Data used to train")
plt.plot(xdata, result.best_fit, ydata,"y.",label="Lmfit")
#plt.plot(data["day"],np.log(data["suspected"]))
#plt.plot(data["day"],data["Infected"])
#plt.plot(data["Day"],y3,'b.')
plt.plot(data["Day"],ysolv,label="predicted")
#plt.plot(data["Day"],ysolv2,label="predicted with origin compensation")
plt.legend()
plt.ylim(0, 3e8)
plt.show()

