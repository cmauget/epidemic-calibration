from calibration import calibModel
from calibration import calibModelOde
import numpy as np
import matplotlib.pyplot as plt

'''
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
'''
#------------------------------using an edge matrix----------------------------#

model = calibModel()
out, fitted_curve, fitted_parameters = model.calib("config_SIR_1.json")


#-------------------------------using custom ODE--------------------------------#

def deriv(y, t, N, params): 

    dy = np.zeros(3)
    S, I, R = y
    dy[0] = -params[0] * S * I / N
    dy[1] = params[0] * S * I / N - params[1] * I
    dy[2]= params[1] * I
    return dy


model2 = calibModelOde()

out, fitted_curve, fitted_parameters = model2.calib("config_SIR_1_Edo.json", deriv)
