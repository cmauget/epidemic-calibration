import numpy as np

test = True #Easier testing removing human input


def init(test): #initialise the data

    if test:
        size = 3
        name_tab = ["Suspected", "Infected", "Recovered"]
        cor_tab = np.array([[0,1,0], [0,0,1], [0,0,0]])

    else:

        size=int(input("Enter the number of compartment wanted : "))
        cor_tab = np.zeros(shape=(size,size))
        name_tab = []
        for i in range(size):
            name_tab.append(input("Enter the name of the "+str(i+1)+" compartment : "))

    return name_tab, cor_tab, size

def create_deriv(name_tab, cor_tab, size, y0, params):

    y = np.zeros(size)
    dy = np.zeros(size)

    for i in range(size):
        dy[i] = -params[0]
   
    return 
    

name_tab, cor_tab, size = init(test)
create_deriv(name_tab, cor_tab, size)
