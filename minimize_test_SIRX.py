from minimze import SIRXModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#-----------------Fitting on simulated data-----------------------#
data_br = pd.read_csv("data/data_SIRX_175.csv")


data_nr = data_br["Recovered"].to_numpy() #fitting on Infected data


N = 3e8 #population

I0 = 1 #Initial number of infected
R0 = 0 #Initial number of recovered
S0 = N - I0 - R0 #initial number of recovered
X0 = 0
y0 = S0, I0, R0, X0 #initial state vector

n=175 #number of days
t = np.linspace(0, n, n) #timeseries (\days)

#allow quick modification of the number of days to train on
train_size = 70
t_train = np.linspace(0, train_size, train_size) #time series for the training
data = np.resize(data_nr,train_size)



#Initial guess of our parameters
beta = 0.3
gamma = 1./10
kappa = 0.2
alpha = 0.2
guess = (beta, gamma, kappa, alpha)

#Creating the SIRModel
model = SIRXModel()
fitted_model = SIRXModel()

#Applying the fit
res = model.fit(t_train, data, guess, y0 , N)

print(res.params)

beta_fit=res.params['beta'].value
gamma_fit=res.params['gamma'].value
kappa_fit=res.params['kappa'].value
alpha_fit=res.params['alpha'].value

print(beta_fit)
print(gamma_fit)
print(kappa_fit)
print(alpha_fit)

fitted_S, fitted_I, fitted_R, fitted_X = fitted_model.SIRSolve(y0, t, N, beta_fit, gamma_fit, kappa_fit, alpha_fit)

del data_br["Day"]
plt.axvline(x=train_size,color='gray',linestyle='--', label="End of train dataset")
plt.plot(t, data_br, '+', label = "Simulated Data")
plt.plot(t, fitted_S,label="Predicted S")
plt.plot(t, fitted_I, label = "Predicted I"),
plt.plot(t, fitted_R, label = "Predicted R")
plt.plot(t, fitted_X, label = "Predicted X")
plt.legend()
plt.show()

