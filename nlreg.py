import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("data/data_80.csv")

def func(beta, data, t):
    return int(3e8*np.exp((-beta * t * data.Infected[t])/3e8))

def funclog(beta, data, t):
    return int(np.log(3)+8+((-beta * t * data.Infected[t])/3e8))
guess = 0.5

size = len(data["day"])

y = np.empty(size)
y2 = np.empty(size)

for i in range(size):
    y[i]=func(guess, data, i)
    y2[i]=funclog(guess, data, i)
    print(y[i])


plt.plot(data["day"],np.log(data["suspected"]))
plt.plot(data["day"],y2,'r.')
plt.show()

