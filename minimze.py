import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
from lmfit import minimize, Parameters
import scipy

data = pd.read_csv("data/data_SIR_80.csv")

N = 3e8 #population

I0 = 1 #Initial number of infected
R0 = 0 #Initial number of recovered
S0 = N - I0 - R0 #initial number of recovered
y0 = S0, I0, R0
y0str = str(S0), str(I0), str(R0)



n=175 #number of days
t = np.linspace(0, n, n) #timeseries (\days)
print(t)

print(scipy.__version__)

size = len(data["Day"])
sum = [size]
temp = 0

a = np.zeros((3,len(t)+1))
a[0,0] = S0
a[1,0] = I0
a[2,0] = R0

for i in range(size):
    temp = temp + data.Infected[i]
    sum.append(temp)

#SIR model
class SIRModel:

    def __init__(self):
        pass

    #SIR EDO
    def deriv(self, a, t, N, beta, gamma): 
        S = a[0,:].tolist()
        I = a[1,:]
        R = a[2,:]
        

        dy = np.zeros(3)
        dy[0] = -beta * S * I / N #dSdt 
        dy[1] = beta * S[t] * I[t] / N - gamma * float(I) #dIdt 
        dy[2] = gamma * I[t] #dRdt 
        return dy

    def SIRSolve(self, y0, t, N, beta, gamma):

        res = ode(self.deriv)
        res.set_integrator("dopri5")
        res.set_initial_value(y0,0)
        res.set_f_params(N,beta,gamma)

        result = np.zeros((3,len(t)+1))
        result[:,0] = y0

        for it, t_ in enumerate(t):
            y = res.integrate(t_)
            result[:,it+1] = y

        return result

    def err(self, params, t,  data):

        beta = params["beta"]
        gamma = params["gamma"]
        N = params["N"]

        res = self.SIRSolve(y0, t, N, beta, gamma)
        X = res[2,:]

        err = X*N - data

        return err

    def fit(self , t, data, maxfev=100000, params=None):

        if params is None:
            params = Parameters()
            beta = 0.3
            gamma = 1./9
            params.add('beta',value=beta,vary=True)
            params.add('gamma',value=gamma, vary=True)
            params.add('N', value=3e8, vary=False)

        out = minimize(self.err, params, args=(t, data, ),maxfev=maxfev)
        return out

model = SIRModel()

beta = 0.4
gamma = 1./10

print(type(a))
print(type(a[0,:].tolist()))
#dy = model.deriv(a, t, N, beta, gamma)

fit = model.fit(t, data, maxfev=100000, params=None)