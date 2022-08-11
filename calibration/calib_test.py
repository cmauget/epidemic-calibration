from calibration import calibModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def init():

    guess = np.array([0.3, 1./10])

    nb_comp = 3 #len name_tab?
    name_comp = ["Suspected", "Infected", "Recovered"]
    cor_tab = np.array([[0,1,0,], [0,0,1], [0,0,0]]) #SIR Model
    name_params = ["Beta", "Gamma"]
    fit_tab = [1,1,1]

    n=175
    t = np.linspace(0, n, n)

    N = 3e8 #population
    I0 = 1 #Initial number of infected
    R0 = 0 #Initial number of recovered
    S0 = N - I0 - R0 #initial number of recovered
    y0 = S0, I0, R0


    name_fic = "data_SIR_175.csv"
    data = pd.read_csv("calibration/data/"+name_fic)

    return guess, N, t, data, y0, cor_tab, nb_comp, name_comp, name_params, fit_tab

def init2():

    guess = np.array([1, 1./10])

    nb_comp = 3 #len name_tab?
    name_comp = ["Suspected", "CASE_COUNT", "Recovered"]
    cor_tab = np.array([[0,1,0,], [0,0,1], [0,0,0]]) #SIR Model
    name_params = ["Beta", "Gamma"]
    fit_tab = [0,1,0]

    n=79
    t = np.linspace(0, n, n)

    N = 3e6 #population
    I0 = 100 #Initial number of infected
    R0 = 1e6 #Initial number of recovered
    S0 = N - I0 - R0 #initial number of recovered
    y0 = S0, I0, R0


    name_fic = "nyc.csv"
    data = pd.read_csv("calibration/data/"+name_fic)

    return guess, N, t, data, y0, cor_tab, nb_comp, name_comp, name_params, fit_tab


def init3():

    guess = np.array([0.3, 1./10, 2./100])

    nb_comp = 4 #len name_tab?
    name_comp = ["Suspected", "Infected", "Recovered", "Death"]
    cor_tab = np.array([[0,1,0,0], [0,0,1,1], [0,0,0,0],[0,0,0,0]]) #SIRD Model
    name_params = ["Beta", "Gamma", "Delta"]
    fit_tab = [0,1,0,1]

    n=175
    t = np.linspace(0, n, n)

    N = 3e8 #population
    I0 = 1 #Initial number of infected
    R0 = 0 #Initial number of recovered
    S0 = N - I0 - R0 #initial number of recovered
    y0 = S0, I0, R0, 0


    name_fic = "data_SIRD__n0.csv"
    data = pd.read_csv("calibration/data/"+name_fic)

    return guess, N, t, data, y0, cor_tab, nb_comp, name_comp, name_params, fit_tab

#----------------------------------------------------------------#

guess, N, t, data, y0, cor_tab, nb_comp, name_comp, name_params, fit_tab = init3()

model = calibModel()

out, fitted_curve = model.calib(guess, N, t, data, y0, cor_tab, nb_comp, name_comp, name_params, fit_tab)

print(out.params)

plt.plot(fitted_curve[1,:])
plt.plot(data[name_comp[1]], '+')
plt.show()