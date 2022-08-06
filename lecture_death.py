import matplotlib.pyplot as plt, numpy as np, pandas as pd
from minimize import SIRModel
from scipy.optimize import curve_fit
from lmfit import Model
from sklearn.metrics import mean_absolute_error, mean_squared_error
import time

def lecture(filename):
	df = pd.read_csv(filename)
	return df

def pretraitement(df, state=None):
	COLUMNS = ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key', 'Population']
	if state is not None:
		# Selection des comtés d'un état donné ('New York', 'Alabama', 'Minnesota'])
		df = df[ df.Province_State == state ].copy(deep=True)
	df.drop(columns=COLUMNS, inplace=True)

	df = df.sum(axis=0)
	df = pd.DataFrame(df)
	df.reset_index(inplace=True)
	df.rename(columns={'index': 'Date', 0: 'Cumul'}, inplace=True)

	df.reset_index(inplace=True)
	df.rename(columns={'index': 'Days'}, inplace=True)

	return df

# MAIN
#N = 3e8 #Population USA
#N = 4e6 #Population NY
train_size = 70

filename = "covid-19/time_series_covid19_deaths_US.csv"
df = lecture(filename)
N = df.Population.sum()
df = pretraitement(df, None)
df.drop(columns=['Date'], inplace=True)
df.to_csv('data/ny_death.csv', sep=',', index=False)

# PLOT
fig, ax = plt.subplots(figsize=(8.26, 8.26))
ax.set_title('Death us')
ax.scatter(df.Days, df.Cumul, marker='+', color='black', label='Measures')
plt.show()
plt.close(fig)
