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

        for i in range(10):
            data[i]=data[i].rstrip("\n")
        
        N = float(data[0])
        I0 = float(data[1])
        R0 = float(data[2])
        S0 = N-I0-R0
        y0 = S0, I0, R0
        data_info = data[3:8]
        print(data_info)

        guess = [float(x) for x in data[8:10]]
        
        return N, y0, guess, data_info


    def init(self, data_info):

        temp_load = pd.read_csv("data/"+data_info[0])

        data_nr = np.zeros([3,len(temp_load[data_info[1]])])

        for i in range(3):
            data_nr[i,:] = temp_load[data_info[i+1]].to_numpy()

        data = np.resize(data_nr,(3,int(data_info[4])))
        data[1,:] = np.resize(data_nr[1,:],int(data_info[4])) #wtf ca marche sinon ca bug comprends pas

        t_train = np.linspace(0, int(data_info[4]), int(data_info[4])) #time series for the training
        t = np.linspace(0, int(len(data_nr[0,:])), int(len(data_nr[0,:])) ) #timeseries (\days)
      
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

    def err(self, params, t,  data, y0, data_info):


        beta = params["beta"]
        gamma = params["gamma"]
        N = params["N"]

        S, I, R  = self.SIRSolve(y0, t, N, beta, gamma)

        err = I - data[1,:] 
        

        return err

    def fit(self , config_name, methods='leastsq', max_nfev=100000):

        N, y0, guess, data_info = self.load_config(config_name)

        params = Parameters()
        params.add('beta',value=guess[0],min=0, max = 10, vary=True)
        params.add('gamma',value=guess[1],min=0, max=2, vary=True)
        params.add('N', value=N, vary=False)

        data_nr, data, t_train, t = self.init(data_info)

        print(methods)
        out = minimize(self.err, params, method=methods, args=(t_train, data, y0, data_info, ),max_nfev=max_nfev)
        beta_fit=out.params['beta'].value
        gamma_fit=out.params['gamma'].value
        fitted_parameters=([beta_fit, gamma_fit])
        fitted_curve=self.SIRSolve(y0, t, N, beta_fit, gamma_fit)
        mae = mean_absolute_error(data_nr[1,:], fitted_curve[:][1])

        return out, data_nr, fitted_parameters, fitted_curve, mae, t


#-------------------SIRD model----------------------#
class SIRDModel:

    def __init__(self):
        pass

    def load_config(self, config_name):

        with open("data/"+config_name, "r") as f:
            data = f.readlines()
        f.close()

        for i in range(11):
            data[i]=data[i].rstrip("\n")
        
        N = float(data[0])
        I0 = float(data[1])
        S0 = N-I0
        y0 = S0, I0, float(data[2]), float(data[3])
        data_info = data[4:8]

        guess = [float(x) for x in data[8:11]]

        print(y0)
        print(data_info)
        print(guess)
        
        return N, y0, guess, data_info


    def init(self, data_info):

        data_nr= pd.read_csv("data/"+data_info[0])[data_info[1]].to_numpy()
        data_i = np.resize(data_nr,int(data_info[3]))
        data_nr_d= pd.read_csv("data/"+data_info[0])[data_info[2]].to_numpy()
        data_d = np.resize(data_nr_d,int(data_info[3]))
        t_train = np.linspace(0, int(data_info[3]), int(data_info[3])) #time series for the training
        t = np.linspace(0, int(len(data_nr)), int(len(data_nr))) #timeseries (\days)

        return data_nr, data_i, data_d, t_train, t


    #SIR EDO
    def deriv(self, y0, t, N, beta, gamma, kappa): 

        S, I, R, D = y0
        #print(y0)
        
        dy = np.zeros(4)
        dy[0] = -beta * S * I / N #dSdt 
        dy[1] = beta * S * I / N - gamma * I - kappa * I #dIdt 
        dy[2] = gamma * I #dRdt 
        dy[3] = kappa * I  #dDdt
        return dy

    def SIRSolve(self, y0, t, N, beta, gamma, kappa):

        res = odeint(self.deriv, y0, t, args=(N, beta, gamma, kappa)) 
        S, I, R, D = res.T

        return S, I, R, D

    def err(self, params, t,  data_i, data_d, y0):


        beta = params["beta"]
        gamma = params["gamma"]
        kappa = params["kappa"]
        N = params["N"]

        S, I, R, D  = self.SIRSolve(y0, t, N, beta, gamma, kappa)

        err = pow(I - data_i,2) + pow(D - data_d,2)

        return err

    def fit(self , config_name, methods='leastsq', max_nfev=100000):

        N, y0, guess, data_info = self.load_config(config_name)

        params = Parameters()
        params.add('beta',value=guess[0],min=0, max = 10, vary=True)
        params.add('gamma',value=guess[1],min=0, max=2, vary=True)
        params.add('kappa',value=guess[2],min=0, max=2, vary=True)
        params.add('N', value=N, vary=False)

        data_nr, data_i, data_d, t_train, t = self.init(data_info)

        out = minimize(self.err, params, method=methods, args=(t_train, data_i, data_d, y0, ),max_nfev=max_nfev)
        
        beta_fit=out.params['beta'].value
        gamma_fit=out.params['gamma'].value
        kappa_fit=out.params['kappa'].value
        fitted_parameters=([beta_fit, gamma_fit, kappa_fit])
        fitted_curve=self.SIRSolve(y0, t, N, beta_fit, gamma_fit, kappa_fit)
        mae = mean_absolute_error(data_nr, fitted_curve[:][1])

        return out, data_nr, fitted_parameters, fitted_curve, mae, t 
