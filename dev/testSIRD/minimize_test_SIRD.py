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

def data_frame(data, start, end, step, basename):
    df = pd.DataFrame(data)
    df.to_csv(f'data/sird_{basename}.csv', sep = ',')
    for j in range(start,end,step):
        dfOpt = df[ df.Starting_Days == j ]
        print('Most effective method:')
        print(df.iloc[dfOpt.Mae.idxmin(),:])
    return df

def final_plot(df, basename):
    fig, ax = plt.subplots(figsize=(8.26,8.26))
    ax.set_title(f'Comparison of methods (SIRD model, {basename})', fontsize=20)
    for method in df.Methods.unique():
        _df = df[ df.Methods == method]
        ax.plot(_df.Starting_Days.apply(lambda v: str(v)), _df.Mae, label=method)
    ax.set_xlabel('Starting day', fontsize=16)
    ax.set_ylabel('MAE', fontsize=16)
    #~ ax.set_yscale('linear')
    #~ ax.set_ylim([1.3e7, 1.5e7])
    ax.legend(ncol=2, loc='upper center', fontsize=16)
    plt.savefig(f'fig/fig_SIRD_{basename}.pdf')
    plt.show()
    plt.close(fig)

#---------------- Fitted on NYC data ---------------------#
#Creating the SIRModel
model = SIRDModel()

methods=["leastsq",'least_squares','differential_evolution','brute','basinhopping','ampgo','nelder','lbfgsb','powell','cg','cobyla','bfgs','trust-constr','tnc','slsqp','shgo','dual_annealing']
#~ methods=["leastsq"]

data = {'Starting_Days': [], 'Methods': [], 'Beta': [], 'Gamma': [], 'Mae': []}

start, end, step, basename = 27, 37, 1, 'n5'
#~ start, end, step, basename = 32, 38, 1, 'n10'
#~ start, end, step, basename = 67, 80, 1, 'ny'

configFile = f'config_{basename}.txt'
for method in methods:
    for j in range(start,end,step):

        change_train_size(configFile, j)
        
        out, data_nr, fitted_parameters, fit, mae, t = model.fit(configFile, method)
        print(fitted_parameters)
        
        #~ disp(j, t, fitted_parameters, fit, data_nr, mae, method)
        data = data_set(data, j, method, fitted_parameters, mae)

df = data_frame(data, start, end, step, basename)
final_plot(df, basename)
