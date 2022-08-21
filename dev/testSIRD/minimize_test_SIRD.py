import pkgutil
from matplotlib.font_manager import json_dump
from minimize import SIRDModel
import matplotlib.pyplot as plt, pandas as pd
import numpy as np

def disp(train_size, t, fitted_parameters, fit, data_nr, mae, methods):	
    fig, ax = plt.subplots(figsize=(8.26, 8.26))
    #ax.set_ylim(0,data_nr.max()*1.1)
    ax.set_title('Infected')
    plt.axvline(x=train_size,color='gray',linestyle='--', label="End of train dataset")
    ax.scatter(t, data_nr, marker='+', color='black', label=f'Measures (method = {methods})')
    ax.plot(t, fit[:][1], 'g-', label=f'Simulation')
    ax.vlines(t, data_nr, fit[:][1], color='g', linestyle=':', label=f'MAE = {mae:.1f}')
    fig.legend(loc='upper center')
    plt.show()
    plt.close(fig)
    
def change_train_size(config_name, train_size):  
    with open("data/"+config_name, "r") as f:
        data = f.readlines()
    f.close()
    data[7] = data[7].rstrip("\n")
    f = open("data/"+config_name, "r")
    replacement = ""
    for line in f:
        line = line.strip()
        changes = line.replace(data[7], str(j))
        replacement = replacement + changes + "\n"
    f.close()
    fout = open("data/"+config_name, "w")
    fout.write(replacement)
    fout.close()

def data_set(data, train_size, methods, fitted_parameters, mae):
    data['Starting_Days'].append(train_size)
    data['Methods'].append(methods)
    data['Beta'].append(fitted_parameters[0])
    data['Gamma'].append(fitted_parameters[1])
    data['Mae'].append(mae)

    return data

def data_frame(data, start, end, step):
    df = pd.DataFrame(data)
    df.to_csv('data/data_out_infected.csv', sep = ',')
    for j in range(start,end,step):
        dfOpt = df[ df.Starting_Days == j ]
        print('Most effective method:')
        print(df.iloc[dfOpt.Mae.idxmin(),:])

#---------------- Fitted on NYC data ---------------------#
#Creating the SIRModel
model = SIRDModel()

methods=["leastsq",'least_squares','differential_evolution','brute','basinhopping','ampgo','nelder','lbfgsb','powell','cg','cobyla','bfgs','trust-constr','emcee','slsqp','shgo','dual_annealing']
data = {'Starting_Days': [], 'Methods': [], 'Beta': [], 'Gamma': [], 'Mae': []}

start, end, step = 70, 85, 5
mae_tab = np.zeros([17,3])
for i in range(17):
    for j in range(start,end,step):

        change_train_size("config_ny.txt", j)
        
        out, data_nr, fitted_parameters, fit, mae, t = model.fit("config_ny.txt" , methods[i])
        print(fitted_parameters)
        
        ind = int((j-start)/step)
        mae_tab[i][ind] = np.sqrt(mae)

        disp(j, t, fitted_parameters, fit, data_nr, mae, methods[i])
        data = data_set(data, j, methods[i], fitted_parameters, mae)

data_frame(data, start, end, step)
plt.plot([65,70,75], mae_tab[0][:],label='leastsq')
plt.plot([65,70,75], mae_tab[1][:],label='least_squares')
plt.plot([65,70,75], mae_tab[2][:],label='differential_evolution')
plt.plot([65,70,75], mae_tab[3][:],label='brute')
plt.plot([65,70,75], mae_tab[4][:],label='basinhopping')
plt.plot([65,70,75], mae_tab[5][:],label='ampgo')
plt.plot([65,70,75], mae_tab[6][:],label='nelder')
plt.plot([65,70,75], mae_tab[7][:],label='lbfgsb')
plt.plot([65,70,75], mae_tab[8][:],label='powell')
plt.plot([65,70,75], mae_tab[9][:],label='cg')
plt.plot([65,70,75], mae_tab[10][:],label='cobyla')
plt.plot([65,70,75], mae_tab[11][:],label='bfgs')
plt.plot([65,70,75], mae_tab[12][:],label='trust-constr')
plt.plot([65,70,75], mae_tab[13][:],label='emcee')
plt.plot([65,70,75], mae_tab[14][:],label='slsqp')
plt.plot([65,70,75], mae_tab[15][:],label='shgo')
plt.plot([65,70,75], mae_tab[16][:],label='dual_annealing')
plt.legend()
disp(45, t, fitted_parameters, fit, data_nr, mae, methods[1])
