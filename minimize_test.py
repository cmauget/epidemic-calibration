from minimze import SIRModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

#---------------- Fitted on NYC data---------------------#
data_nyc_br = pd.read_csv("data/nyc.csv")

data_nyc_nr = data_nyc_br["CASE_COUNT"].to_numpy()#Fitting on Infected data

N = 8000 #population

I0 = 1 #Initial number of infectedJacobian is required for Newton-CG method
R0 = 0 #Initial number of recovered
S0 = N - I0 - R0 #initial number of recovered
y0 = S0, I0, R0 #initial state vector

n=79 #number of days
t = np.linspace(0, n, n) #timeseries (\days)



#Initial guess of our parameters
beta = 0.3
gamma = 1./10
guess = (beta, gamma)

#Creating the SIRModel
model = SIRModel()
fitted_model = SIRModel()
mae_tab=np.zeros(shape=(10,18))

methods=["leastsq",'least_squares','differential_evolution','brute','basinhopping','ampgo','nelder','lbfgsb','powell','cg','cobyla','bfgs','tnc','trust-constr','slsqp','shgo','dual_annealing']


#Applying the fit
ficname="data_OUT_.txt"
fic = open("data/"+ficname,"w")
st = 40
end = 60
mae_tab=np.zeros(shape=(int(((end-st)/5)-1),18))
for j in range(st,end,5):
    #allow quick modification of the number of days to train on
    print("///////////////////////////// ")
    print("Starting with "+str(j)+" days")
    fic.write("///////////////////////////// \n")
    fic.write("Starting with "+str(j)+" days \n")
    train_size = j
    t_train = np.linspace(0, train_size, train_size) #time series for the training
    data_nyc = np.resize(data_nyc_nr,train_size)    
    for i in range(17):
        res = model.fit(t_train, data_nyc, guess, y0, N, methods[i])
        print(res.params)
        print("method used is : "+methods[i])
        fic.write("method used is : "+methods[i]+"\n")
        beta_fit=res.params['beta'].value
        gamma_fit=res.params['gamma'].value
        print("NYC beta fitted "+str(beta_fit))
        print("NYC gamma fitted "+str(gamma_fit))
        fic.write("NYC beta fitted "+str(beta_fit)+"\n")
        fic.write("NYC gamma fitted "+str(gamma_fit)+"\n")
        fitted_S, fitted_I, fitted_R = fitted_model.SIRSolve(y0, t, N, beta_fit, gamma_fit)
        mae = mean_absolute_error(data_nyc_nr, fitted_I)
        print("Mean absolute error is :"+str(mae))
        fic.write("Mean absolute error is :"+str(mae)+"\n")
        ind=(j-st)/5
        mae_tab[int(ind)][i]= np.log(mae)
        print("------------------------")
        fic.write("------------------------ \n")

print(mae_tab)

fic.close()


'''
plt.axvline(x=train_size,color='gray',linestyle='--', label="End of train dataset")
plt.plot(t, data_nyc_nr, '+', label = "NYC Data")
plt.plot(t, fitted_I, label = "Predicted"),
'''

plt.plot(mae_tab)
plt.legend()
plt.show()

