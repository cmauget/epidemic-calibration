import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from lmfit import minimize, Parameters
from sklearn.metrics import mean_absolute_error

#-------------------SIR model----------------------#
class SIRModel:

    def __init__(self):
        pass

    def load_config(self, config_name):

        with open("data/"+config_name, "r") as f:
            data = f.readlines()
        f.close()

        for i in range(8):
            data[i]=data[i].rstrip("\n")
        
        N = float(data[0])
        I0 = float(data[1])
        S0 = N-I0
        y0 = S0, I0, float(data[2])
        data_info = data[3:6]

        guess = [float(x) for x in data[6:8]]
        
        return N, y0, guess, data_info

    def init(self, data_info):
    
        data_nr = pd.read_csv("data/"+data_info[0])[data_info[1]].to_numpy()
        data = np.resize(data_nr,int(data_info[2]))
        t_train = np.linspace(0, int(data_info[2]), int(data_info[2])) #time series for the training
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
        X = I 

        err = X - data

        return err

    def fit(self , config_name, methods='leastsq', max_nfev=100000):

        N, y0, guess, data_info = self.load_config(config_name)

        params = Parameters()
        params.add('beta',value=guess[0],min=0, max = 10, vary=True)
        params.add('gamma',value=guess[1],min=0, max=2, vary=True)
        params.add('N', value=N, vary=False)

        data_nr, data, t_train, t = self.init(data_info)

        out = minimize(self.err, params, method=methods, args=(t_train, data, y0, ),max_nfev=max_nfev)
        beta_fit=out.params['beta'].value
        gamma_fit=out.params['gamma'].value
        fitted_parameters=([beta_fit, gamma_fit])
        fitted_curve=self.SIRSolve(y0, t, N, beta_fit, gamma_fit)
        mae = mean_absolute_error(data_nr, fitted_curve[:][1])

        return t, out, data_nr, fitted_parameters, fitted_curve, mae

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