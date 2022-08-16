import matplotlib.pyplot as plt, numpy as np, pandas as pd
from minimze import SIRModel
from scipy.optimize import curve_fit
from lmfit import Model
from sklearn.metrics import mean_absolute_error, mean_squared_error
import time

def lecture(filename):
	df = pd.read_csv(filename)
	return df

def pretraitement(df, state=None):
	COLUMNS = ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key']
	if state is not None:
		# Selection des comtés d'un état donné ('New York', 'Alabama', 'Minnesota'])
		df = df[ df.Province_State == state ].copy(deep=True)
	df.drop(columns=COLUMNS, inplace=True)

	df = df.sum(axis=0)
	df = pd.DataFrame(df)
	df.reset_index(inplace=True)
	df.rename(columns={'index': 'Date', 0: 'Cumul'}, inplace=True)

	# On rettranche à chaque colonne celle qui l'a précède
	df['Delta'] = 0
	for nr in range(1, len(df)):
		df.at[nr, 'Delta'] = df.at[nr, 'Cumul'] - df.at[nr-1, 'Cumul']

	df.reset_index(inplace=True)
	df.rename(columns={'index': 'Days'}, inplace=True)

	# ZOOM SUR LES 200 PREMIERS JOURS CAR 4 VAGUES POUR NY
	df = df[ df.Days < 200 ].copy(deep=True)
	df.reset_index(inplace=True, drop=True)

	return df

def traitement(df, train_size):
	measures = df.Delta.to_numpy()
	
	I0 = 1 
	R0 = 0 
	S0 = N - I0 - R0 
	y0 = S0, I0, R0 #Initial state vector

	n = len(df) 
	t = np.linspace(0, n, n) 

	t_train = np.linspace(0, train_size, train_size) #Time series for the training
	train_set = np.resize(measures, train_size)

	#Initial guess of our parameters
	beta, gamma = 0.3, 1./10
	guess = (beta, gamma)

	#Creating the SIRModel
	model = SIRModel()
	fitted_model = SIRModel()

	#Applying the fit
	res = model.fit(t_train, train_set, guess, y0, N)
	print(res.params)

	beta_fit=res.params['beta'].value
	gamma_fit=res.params['gamma'].value

	print(f'NYC beta fitted {beta_fit}')
	print(f'NYC gamma fitted {gamma_fit}')

	fitted_S, fitted_I, fitted_R = fitted_model.SIRSolve(y0, t, N, beta_fit, gamma_fit)
	
	return df, fitted_I	

def posttraitement(df, fitted_I, train_size, texec):
	mae, mse = mean_absolute_error(df['Delta'], fitted_I), mean_squared_error(df['Delta'], fitted_I)
	
	fig, ax = plt.subplots(figsize=(8.26, 8.26))
	ax.set_title('SIR Model')
	plt.axvline(x=train_size,color='gray',linestyle='--', label="End of train dataset")
	ax.scatter(df.Days, df.Delta, marker='+', color='black', label='Measures')
	ax.plot(df.Days, fitted_I, 'g-', label=f'Simulation (method=leastsq, execution time={texec})')
	ax.vlines(df.Days, df.Delta, fitted_I, color='g', linestyle=':', label=f'MAE = {mae:.1f}, MSE = {mse:.1f}')
	fig.legend(loc='upper center')
	plt.show()
	plt.close(fig)

# MAIN
#N = 3e8 #Population USA
N = 4e6 #Population NY
train_size = 70

filename = "covid-19/time_series_covid19_confirmed_US.csv"
df = lecture(filename)
df = pretraitement(df, 'New York')
#df.drop(columns=['Date', 'Cumul'], inplace=True)
#df.to_csv('data/ny_confirmed.csv', sep=';', index=False)
start = time.time()
df, fitted_I = traitement(df, train_size)
end = time.time()
texec = end-start
posttraitement(df, fitted_I, train_size, texec)
