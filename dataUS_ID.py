import matplotlib.pyplot as plt, numpy as np, pandas as pd

def lecture(filename):
	df = pd.read_csv(filename)
	return df

def pretraitement(dfD, dfI, state=None):
	COLUMNSD = ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key', 'Population']
	COLUMNSI = ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key']
	
	'''
	if state is not None:
		# Selection des comtés d'un état donné ('New York', 'Alabama', 'Minnesota'])
		df = df[ df.Province_State == state ].copy(deep=True)
	'''
	
	dfD.drop(columns=COLUMNSD, inplace=True)
	dfI.drop(columns=COLUMNSI, inplace=True)
	
	dfD = dfD.sum(axis=0)
	dfI = dfI.sum(axis=0)
	
	df = pd.DataFrame({'Death': dfD, 'Cumul':dfI})
	df.reset_index(inplace=True)
	df.rename(columns={'index': 'Date', 0: 'Death', 1: 'Cumul'}, inplace=True)

	# On rettranche à chaque colonne celle qui l'a précède
	df['Infectious'] = 0
	for nr in range(1, len(df)):
		df.at[nr, 'Infectious'] = df.at[nr, 'Cumul'] - df.at[nr-1, 'Cumul']

	df.reset_index(inplace=True)
	df.rename(columns={'index': 'Days'}, inplace=True)
	
	# ZOOM SUR LES 200 PREMIERS JOURS CAR 4 VAGUES POUR NY
	#df = df[ df.Days < 200 ].copy(deep=True)
	#df.reset_index(inplace=True, drop=True)

	return df

# MAIN
#N = 3e8 #Population USA
#N = 4e6 #Population NY
train_size = 70
filenameD = "covid-19/time_series_covid19_deaths_US.csv"
filenameI = "covid-19/time_series_covid19_confirmed_US.csv"
dfD = lecture(filenameD)
dfI = lecture(filenameI)
N = dfD.Population.sum()
df = pretraitement(dfD, dfI, None)
df.drop(columns=['Date', 'Cumul'], inplace=True)
df.to_csv('data/ny_death_infectious.csv', sep=',', index=False)

# PLOT
fig, ax = plt.subplots(figsize=(8.26, 8.26))
ax.set_title('Death and infectious us')
ax.scatter(df.Days, df.Infectious, marker='+', color='black', label='Infectious')
ax.scatter(df.Days, df.Death, marker='+', color='red', label='Death')
plt.show()
plt.close(fig)
