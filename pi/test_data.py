import random
import numpy as np

def rand_data():
    chan0 = []
    chan1 = []
    chan2 = []
    chan3 = []
    chan4 = []
    chan5 = []
    for x in range(3):
        chan0.append(random.randint(0, 100))
        chan1.append(random.randint(0, 100))
        chan2.append(random.randint(0, 100))
        chan3.append(random.randint(0, 100))
        chan4.append(random.randint(0, 100))
        chan5.append(random.randint(0, 100))


    np.array(chan0)
    average0 = np.average(chan0)
    np.array(chan1)
    average1 = np.average(chan1)
    np.array(chan2)
    average2 = np.average(chan2)
    np.array(chan3)
    average3 = np.average(chan3)
    np.array(chan4)
    average4 = np.average(chan4)
    np.array(chan5)
    average5 = np.average(chan5)


    return average0, average1, average2, average3, average4, average5
def return_data():
    data = rand_data()
    return data

print(return_data())
