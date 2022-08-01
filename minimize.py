import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from lmfit import minimize, Parameters


#-------------------SIR model----------------------#
class SIRModel:

    def __init__(self):
        pass

    def init(self, data_name='', train_size='0', i_name=''):

        data_nr = pd.read_csv("data/"+data_name)[i_name].to_numpy()
        data = np.resize(data_nr,train_size)
        t_train = np.linspace(0, train_size, train_size) #time series for the training
        t = np.linspace(0, int(len(data_nr)), int(len(data_nr))) #timeseries (\days)

        return data_nr, data, t_train, t




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

    def fit(self , data_name, i_name, train_size, guess, y0, N, methods='leastsq', max_nfev=100000):

        params = Parameters()
        params.add('beta',value=guess[0],min=0, max = 10, vary=True)
        params.add('gamma',value=guess[1],min=0, max=2, vary=True)
        params.add('N', value=N, vary=False)

        data_nr, data, t_train, t = self.init(self, data_name='', train_size='0', i_name='')

        out = minimize(self.err, params, method=methods, args=(t, data, y0, ),max_nfev=max_nfev)
        return out, data_nr


#-------------------SIRD model----------------------#
class SIRDModel:

    def __init__(self):
        pass

    #SIR EDO
    def deriv(self, y0, t, N, beta, gamma, kappa, alpha): 

        S, I, R, D = y0
        #print(y0)
        
        dy = np.zeros(4)
        dy[0] = -beta * S * I / N #dSdt 
        dy[1] = beta * S * I / N - gamma * I - kappa * I #dIdt 
        dy[2] = gamma * I + alpha * D #dRdt 
        dy[3] = kappa * I - alpha * D #dDdt
        return dy

    def SIRSolve(self, y0, t, N, beta, gamma, kappa, alpha):

        res = odeint(self.deriv, y0, t, args=(N, beta, gamma, kappa, alpha)) 
        S, I, R, D = res.T

        return S, I, R, D

    def err(self, params, t,  data_i, data_d, y0):


        beta = params["beta"]
        gamma = params["gamma"]
        kappa = params["kappa"]
        alpha = params["alpha"]
        N = params["N"]

        S, I, R, D  = self.SIRSolve(y0, t, N, beta, gamma, kappa, alpha)

        err = (I - data_i + D - data_d)/2

        return err

    def fit(self , t, data, guess, y0, N, max_nfev=100000, params=None ):

        if params is None:
            params = Parameters()
            params.add('beta',value=guess[0],min=0, max = 10, vary=True)
            params.add('gamma',value=guess[1],min=0, max=2, vary=True)
            params.add('kappa',value=guess[2],min=0, max=2, vary=True)
            params.add('alpha',value=guess[3],min=0, max=2, vary=True)
            params.add('N', value=N, vary=False)

        out = minimize(self.err, params, args=(t, data, y0, ),max_nfev=max_nfev)
        return out
