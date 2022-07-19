from minimze import SIRModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
res = model.fit(t_train, data, guess, y0 , N)

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
data_nyc_br = pd.read_csv("data/nyc.csv")

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
res = model.fit(t_train, data_nyc, guess, y0, N)

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

