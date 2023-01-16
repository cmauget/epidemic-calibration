# Epidemic Calibration

 A simple epidemic calibration tool for SIR and SIRX model, created by Clément Mauget and Roxane Leduc during an internship at NYU.
 
## Organisation

We have built our GitHub mainly around two directories. A "dev" directory and a "calibration" directory. 

```
📂 epidemic-calibration/ 
├── 📂 calibration/
|       ├── 📂 config/
|       ├── 📂 data/
|       ├── 📂 output/
|       ├── 📜 calibration.py
|       |...
├── 📂 data/
├── 📂 dev/
│...
```
All the useful script are located in the calibration file. For more information refer to the [Additional information](##additional-information) section.

## Setup
You will need to install the following packages running the command :  

```
pip install pandas  
pip install numpy  
pip install lmfit  
pip install scipy  
```
## Calling the calibration function
First you will need to create a calibModel(), if you want to use the edge-adjacency matrix, or a calibModelOde(), if you want to use a custom ODE:

```python
from calibration import calibModel  
from calibration import calibModelEdo  
  
model = calibModel()
model2 = calibModelOde()
```

You will then have to call the calib function from those model. It will return
three values:  

* A minimizer result class (see [here](https://lmfit.github.io/lmfit-py/fitting.html#lmfit.minimizer.MinimizerResult) for more information)  
* A matrix containing the values of all comportment during the periode of
the data set producing the best fit.  
* An array made of the parameters producing the best fit.  

You can call the function in this way:  

```python
out, fitted_curve, fitted_parameters = model.calib("config_file_name.json")
```

If you want to use a custom Ode you will have to call it this way : 
python
```
out, fitted_curve, fitted_parameters = model2.calib("config_file_name.json", deriv)  
```
With **deriv** being the name of you ODE function defined as such : 

```python
def deriv(y, t, N, params):
   dy = np.zeros(3)
   S, I, R = y
   dy[0] = -params[0] * S * I / N
   dy[1] = params[0] * S * I / N - params[1] * I
   dy[2]= params[1] * I
   return dy
```

The calib function also have differents parameters : 

```python
calib(name_json, deriv (if using the Ode model), set_gamma=False, params_out=False, graph_out=True, method=’leastsq’, max_nfev=1000)
```

You can modify those parameters, given with their default values above:
* **set_gamma** take a Boolean. Sometimes you have access to newly infected data everyday. When set to True, this allows the user to manually set the recovery rate parameter to 1, basically telling the program to not expect continuity in the infected value over time, in order to still produce a fit. If false it will estimate this parameter.
* **params_out** take a Boolean. If true, it will output the parameters in a .txt file located in the calibration/out folder.
* **graph_out** take a Boolean. If true, it will display a graph of the fit, allowing you to monitor its coherence.
* **method** take a string. It allows you to choose which method to use when calibrating the model. You can choose them from the methods.txt file
* **max_nfev** take an integer. It allows you to set a maximum number of iterations for the calibration

## Additional information

### Dev directory
The "dev" directory contains our first codes (as well as programs allowing the reading of the JHU data) and allowed us to perform the analysis of the different methods using data frames taking into account the minimum value of the MAE for each method and train size. 

### Calibration directory
The "calibration" directory is the final version of this project and contains all the generalized codes. As seen above, the "model_gen.py" program allows the automatic generation of simulated data sets according to the user’s needs.  
The "calib_test.py" programs together with  config json show to examples of the running program.  
The "calibration.py" program, composed of two models, the "calibModel" which runs based on a edge matrix given by the user, and the "calibModelEdo" which can take as input a custom ODE defined by the user.   
And finally the "data_load.py", whose role is to decode the values contained in the config files.  

Tested with : Dell Latitude 5420 w/ 11th Gen Intel® Core™ i7-1185G7 @ 3.00GHz × 8, 7,5 GiB de RAM, Ubuntu 20.04.3 LTS 64 bits


