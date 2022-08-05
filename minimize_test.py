from matplotlib.font_manager import json_dump
from minimize import SIRModel
import matplotlib.pyplot as plt



def init():

    N = 3e8 #population

    I0 = 1 #Initial number of infectedJacobian is required for Newton-CG method
    R0 = 0 #Initial number of recovered
    S0 = N - I0 - R0 #initial number of recovered
    y0 = S0, I0, R0 #initial state vector

    #Initial guess of our parameters
    beta = 0.3
    gamma = 1./10
    guess = (beta, gamma)

    data_info = (["data_SIR_175_n.csv","Infected","100"])
    #data_info=(["nyc.csv","CASE_COUNT","50"])

    return N, y0, guess, data_info
    

def disp(fitted_parameters, fit, data_nr):

    print(fitted_parameters)

    plt.plot(fit[:][1])
    plt.plot(data_nr,'+')

    plt.show()


#---------------- Fitted on NYC data---------------------#

#Creating the SIRModel
model = SIRModel()

methods=["leastsq",'least_squares','differential_evolution','brute','basinhopping','ampgo','nelder','lbfgsb','powell','cg','cobyla','bfgs','tnc','trust-constr','slsqp','shgo','dual_annealing']

out, data_nr, fitted_parameters, fit = model.fit("config.txt" , methods[0])

disp(fitted_parameters, fit, data_nr)


