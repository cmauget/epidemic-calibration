import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
from lmfit import minimize, Parameters

data = pd.read_csv("data/data_80.csv")

N = 3e8 #population

I0 = 1 #Initial number of infected
R0 = 0 #Initial number of recovered
S0 = N - I0 - R0 #initial number of recovered
y0 = S0, I0, R0

n=175 #number of days
t = np.linspace(0, n, n) #timeseries (\days)

size = len(data["day"])
sum = [size]
temp = 0

for i in range(size):
    temp = temp + data.Infected[i]
    sum.append(temp)

#SIR model
class SIRModel:

    def __init__(self):
        pass

    #SIR EDO
    def deriv(self, y, t, N, beta, gamma): 
        S, I, R = y[O,1,2]

        dy = np.zeros(3)
        dy[0] = -beta * S * I / N #dSdt 
        dy[1] = beta * S * I / N - gamma * I #dIdt 
        dy[2] = gamma * I #dRdt 
        return dy

    def SIRSolve(self, y0, t, N, beta, gamma):

        res = ode(self.deriv)
        res.set_integrator("dopri5")
        res.set_initial_value(y0,t[0])
        res.set_f_params(beta,gamma)

        result = np.zeros((4,len(t)+1))
        result[:,0] = y0

        for it, t_ in enumerate(t):
            y = res.integrate(t_)
            result[:,it+1] = y

        return result

    def err(self, params, x, data):

        beta = params["beta"]
        gamma = params["gamma"]
        N = params["N"]

        res = self.SIRSolve(y0, t, N, beta, gamma)
        X = res[2,:]

        err = X*N - data


