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

    def err(self, params, t,  data):


        beta = params["beta"]
        gamma = params["gamma"]
        N = params["N"]

        S, I, R  = self.SIRSolve(y0, t, N, beta, gamma)
        X = I #TO CHANGE WHEN CHANGING FIT

        err = X - data

        return err

    def fit(self , t, data, guess, N, max_nfev=100000, params=None ):

        if params is None:
            params = Parameters()
            params.add('beta',value=guess[0],min=0, max = 10, vary=True)
            params.add('gamma',value=guess[1],min=0, max=2, vary=True)
            params.add('N', value=N, vary=False)

        out = minimize(self.err, params, args=(t, data, ),max_nfev=max_nfev)
        return out

#Main function

#-----------------Fitting on simulated data-----------------------#
data_br = pd.read_csv("data/data_SIR_175_n.csv")


data_nr = data_br["Infected"].to_numpy() #fitting on Infected data


N = 3e8 #population

I0 = 1 #Initial number of infected
R0 = 0 #Initial number of recovered
S0 = N - I0 - R0 #initial number of recovered
y0 = S0, I0, R0 #initial state vector

n=175 #number of days
t = np.linspace(0, n, n) #timeseries (\days)

#allow quick modification of the number of days to train on
train_size = 40
t_train = np.linspace(0, train_size, train_size) #time series for the training
data = np.resize(data_nr,train_size)



#Initial guess of our parameters
beta = 0.3
gamma = 1./10
guess = (beta, gamma)

#Creating the SIRModel
model = SIRModel()
fitted_model = SIRModel()

#Applying the fit
res = model.fit(t_train, data, guess, N)

print(res.params)

beta_fit=res.params['beta'].value
gamma_fit=res.params['gamma'].value

print(beta_fit)
print(gamma_fit)

fitted_S, fitted_I, fitted_R = fitted_model.SIRSolve(y0, t, N, beta_fit, gamma_fit)

del data_br["Day"]
plt.axvline(x=train_size,color='gray',linestyle='--', label="End of train dataset")
plt.plot(t, data_br, '+', label = "Simulated Data")
plt.plot(t, fitted_S,label="Predicted")
plt.plot(t, fitted_I, label = "Predicted"),
plt.plot(t, fitted_R, label = "Predicted")
plt.legend()
plt.show()


#---------------- Fitted on NYC data---------------------#
data_nyc_br = pd.read_csv("nyc.csv")

data_nyc_nr = data_nyc_br["CASE_COUNT"].to_numpy()#Fitting on Infected data

N = 8000 #population

I0 = 1 #Initial number of infected
R0 = 0 #Initial number of recovered
S0 = N - I0 - R0 #initial number of recovered
y0 = S0, I0, R0 #initial state vector

n=79 #number of days
t = np.linspace(0, n, n) #timeseries (\days)

#allow quick modification of the number of days to train on
train_size = 40
t_train = np.linspace(0, train_size, train_size) #time series for the training

data_nyc = np.resize(data_nyc_nr,train_size)

#Initial guess of our parameters
beta = 0.3
gamma = 1./10
guess = (beta, gamma)

#Creating the SIRModel
model = SIRModel()
fitted_model = SIRModel()

#Applying the fit
res = model.fit(t_train, data_nyc, guess, N)

print(res.params)

beta_fit=res.params['beta'].value
gamma_fit=res.params['gamma'].value

print("NYC beta fitted "+str(beta_fit))
print("NYC gamma fitted "+str(gamma_fit))

fitted_S, fitted_I, fitted_R = fitted_model.SIRSolve(y0, t, N, beta_fit, gamma_fit)

plt.axvline(x=train_size,color='gray',linestyle='--', label="End of train dataset")
plt.plot(t, data_nyc_nr, '+', label = "NYC Data")
plt.plot(t, fitted_I, label = "Predicted"),
plt.legend()
plt.show()
