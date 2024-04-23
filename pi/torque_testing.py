#This is the control unit that runs the Raspberry PI DAQ

#from Encoder import Encoder, get_rpm
from Encoder import Encoder, get_rpm
from torqueSensor import run_Sensor
from test_data import rand_data
import pandas as pd
import threading
import time
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import random
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



#////////////////////////////////////////////////////////////////////////////////////////
#Notes
# Still need to implement getting RPM and Time into the data frame so that I can graph values against time and display RPM
# Still need to implement creating and appending to a new csv once the script is run so that data can easily be retrived
# Still need ti implement making the display look nice and adding data labels
#////////////////////////////////////////////////////////////////////////////////////////

# Constants
gearbox_ratio = 5
start_time = time.time()
filename = "Output.csv"
#df = pd.DataFrame(columns = ['Torque (Nm)', 'Voltage', 'Current', "Gen RPM", "Time (Seconds)", "Input Power", "Output Power", "Efficiency", "Resistance"], )
df = pd.DataFrame()
# Create a function to update the graph with new data every second
def add_data():
    global df
    global ax2
    torque= run_Sensor()
    input_rpm = get_rpm()
    gen_rpm = input_rpm *gearbox_ratio
    # add rpm to concat call below here
    # add time as current_time - start time
    current_time = (time.time() - start_time)
    df = pd.concat([df, pd.DataFrame({'Torque (Nm)': [torque], 'Current Time': [current_time]})], ignore_index=True)
    print(df)
    write_dataframe_to_csv(df, 'data.csv')


def write_dataframe_to_csv(dataframe, filepath):
    dataframe.to_csv(filepath, index=False, header=True)

try:
    
    #thread1 = threading.Thread(target=Encoder) #Initializes Encoder 
    #thread1.start()

    while True:
        add_data()    
   
    
except KeyboardInterrupt:
    exit()