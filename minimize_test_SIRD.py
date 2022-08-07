from matplotlib.font_manager import json_dump
from minimize import SIRDModel
import matplotlib.pyplot as plt, pandas as pd

def disp(train_size, t, fitted_parameters, fit, data_nr, mae, methods):	
    fig, ax = plt.subplots(figsize=(8.26, 8.26))
    ax.set_ylim(0,data_nr.max()*1.1)
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
    data[5] = data[5].rstrip("\n")
    f = open("data/"+config_name, "r")
    replacement = ""
    for line in f:
        line = line.strip()
        changes = line.replace(data[5], str(j))
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

methods=["leastsq",'least_squares','differential_evolution','brute','basinhopping','ampgo','nelder','lbfgsb','powell','cg','cobyla','bfgs','tnc','trust-constr','slsqp','shgo','dual_annealing']
methods=["leastsq",'least_squares']
data = {'Starting_Days': [], 'Methods': [], 'Beta': [], 'Gamma': [], 'Mae': []}

"""
start, end, step = 55, 80, 5
for i in range(2):
	for j in range(start,end,step):
		change_train_size("config.txt", j)
		t, out, data_nr, fitted_parameters, fit, mae = model.fit("config.txt" , methods[i])
		disp(j, t, fitted_parameters, fit, data_nr, mae, methods[i])
		data = data_set(data, j, methods[i], fitted_parameters, mae)
data_frame(data, start, end, step)
"""

out, data_nr, fitted_parameters, fit, mae, t = model.fit("config2_2.txt")

print(fitted_parameters)


disp(100, t, fitted_parameters, fit, data_nr, mae, methods[0])