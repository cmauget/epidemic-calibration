import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from lmfit import minimize, Parameters
import scipy


#-------------------SIR model----------------------#
class SIRModel:

    def __init__(self):
        pass

    #SIR EDO
    def deriv(self, y0, t, N, beta, gamma): 

        S, I, R = y0
        #print(y0)
        
        dy = np.zeros(3)
        dy[0] = -beta * S * I / N #dSdt 
        dy[1] = beta * S * I / N - gamma * I #dIdt 
        dy[2] = gamma * I #dRdt 

        return dy

    def SIRSolve(self, y0, t, N, beta, gamma):

        res = odeint(self.deriv, y0, t, args=(N, beta, gamma)) 
        S, I, R = res.T

        return S, I, R

    def err(self, params, t,  data, y0):


        beta = params["beta"]
        gamma = params["gamma"]
        N = params["N"]

        S, I, R  = self.SIRSolve(y0, t, N, beta, gamma)
        X = I #TO CHANGE WHEN CHANGING FIT

        err = X - data

        return err

    def fit(self , t, data, guess, y0, N, max_nfev=100000, params=None ):

        if params is None:
            params = Parameters()
            params.add('beta',value=guess[0],min=0, max = 10, vary=True)
            params.add('gamma',value=guess[1],min=0, max=2, vary=True)
            params.add('N', value=N, vary=False)

        out = minimize(self.err, params, args=(t, data, y0, ),max_nfev=max_nfev)
        return out


#-------------------SIRX model----------------------#
class SIRXModel:

    def __init__(self):
        pass

    #SIR EDO
    def deriv(self, y0, t, N, beta, gamma, kappa, alpha): 

        S, I, R, X = y0
        #print(y0)
        
        dy = np.zeros(4)
        dy[0] = -beta * S * I / N #dSdt 
        dy[1] = beta * S * I / N - gamma * I - kappa * I #dIdt 
        dy[2] = gamma * I + alpha * X#dRdt 
        dy[3] = kappa * I - alpha * X
        return dy

    def SIRSolve(self, y0, t, N, beta, gamma, kappa):

        res = odeint(self.deriv, y0, t, args=(N, beta, gamma, kappa)) 
        S, I, R, X = res.T

        return S, I, R, X

    def err(self, params, t,  data, y0):


        beta = params["beta"]
        gamma = params["gamma"]
        kappa = params["kappa"]
        N = params["N"]

        S, I, R  = self.SIRSolve(y0, t, N, beta, gamma, kappa)
        X = I #TO CHANGE WHEN CHANGING FIT

        err = X - data

        return err

    def fit(self , t, data, guess, y0, N, max_nfev=100000, params=None ):

        if params is None:
            params = Parameters()
            params.add('beta',value=guess[0],min=0, max = 10, vary=True)
            params.add('gamma',value=guess[1],min=0, max=2, vary=True)
            params.add('kappa',value=guess[1],min=0, max=2, vary=True)
            params.add('N', value=N, vary=False)

        out = minimize(self.err, params, args=(t, data, y0, ),max_nfev=max_nfev)
        return out
