import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from lmfit import minimize, Parameters
import scipy

data = pd.read_csv("data/data_SIR_54_n.csv")

N = 3e8 #population

I0 = 1 #Initial number of infected
R0 = 0 #Initial number of recovered
S0 = N - I0 - R0 #initial number of recovered
y0 = S0, I0, R0

n=54 #number of days
t = np.linspace(0, n, n) #timeseries (\days)

size = len(data["Day"])
sum = [size]
temp = 0

a = np.zeros((3,len(t)+1))
a[0] = S0
a[1] = I0
a[2] = R0

for i in range(size):
    temp = temp + data.Infected[i]
    sum.append(temp)

#SIR model
class SIRModel:

    def __init__(self):
        pass

    #SIR EDO
    def deriv(self, a, t, N, beta, gamma): 
        S = a[0]
        I = a[1]
        R = a[2]
        
        dy = np.zeros(3)
        dy[0] = -beta * S * I / N #dSdt 
        dy[1] = beta * S * I / N - gamma * I #dIdt 
        dy[2] = gamma * I #dRdt 
        return dy

    def SIRSolve(self, y0, t, N, beta, gamma):

        res = odeint(self.deriv, y0, t, args=(N, beta, gamma)) 
        S, I, R = res.T

        result = np.zeros((3,len(t)))
        result[:,0] = y0
        result[0,:] = S
        result[1,:] = I
        result[2,:] = R

        return result

    def err(self, params, t,  data):


        beta = params["beta"]
        gamma = params["gamma"]
        N = params["N"]

        res = self.SIRSolve(y0, t, N, beta, gamma)
        X = res[0,:]

        err = X - data["Suspected"]

        return err

    def fit(self , t, data, max_nfev=100000, params=None):

        if params is None:
            params = Parameters()
            beta = 0.3
            gamma = 1./9
            params.add('beta',value=beta,min=0, max = 10, vary=True)
            params.add('gamma',value=gamma,min=0, max=2, vary=True)
            params.add('N', value=3e8, vary=False)

        out = minimize(self.err, params, args=(t, data, ),max_nfev=max_nfev)
        return out

model = SIRModel()

beta = 0.4
gamma = 1./10


fit = model.fit(t, data, max_nfev=100000, params=None)
print(fit.params)
