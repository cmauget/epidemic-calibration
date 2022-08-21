import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from lmfit import Model

ficdata = "data/data_SIR_54.csv"
data = pd.read_csv(ficdata)

print("Loading "+ficdata+"...")

size = len(data["Day"])
sum = [size]
temp = 0

train_size = 20

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


result = mymodel.fit(ydata, params, t=xdata, method="lbfgsb")
print(result.fit_report())

delta_fit=result.params['delta'].value


for i in range(size):
    ysolv[i]=funcIC(c,i)
    ysolv2[i]=funcIC(delta_fit,i)
   


#display
plt.plot(data["Day"],data["Infected"],"+",label="Data")
plt.axvline(x=train_size,color='gray',linestyle='--', label="End of train dataset")
plt.plot(data["Day"],ysolv,label="predicted")
plt.plot(data["Day"],ysolv2, linestyle='--', label="predicted with lmfit")
plt.legend()
plt.ylim(0, 3e8)
plt.show()

