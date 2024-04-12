#This is the control unit that runs the Raspberry PI DAQ

from Encoder import Encoder, get_rpm
from Sensor import run_Sensor
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
start_time = time.time()
filename = "Output.csv"
header = ['Torque (Nm)', 'Temp1 (V)', 'Voltage', 'Current', 'Temp2 (V)', 'Water Sensor', "RPM"]
df = pd.DataFrame(columns = ['Torque (Nm)', 'Temp1 (V)', 'Voltage', 'Current', 'Temp2 (V)', "RPM", "Time (Seconds)", "Input Power", "Output Power", "Efficiency"], )


# Create a figure and axis for the graph
fig, ax = plt.subplots(3, sharey=False)
fig.subplots_adjust(wspace=0.3, hspace=0.3)
ax2 = ax[1].twinx()

# Create a function to update the graph with new data every second
def add_data():
    global df
    global ax2
    torque, temp1, temp2, voltage, current, temp2 = run_Sensor()
    rpm = get_rpm()
    # add rpm to concat call below here
    # add time as current_time - start time
    current_time = (time.time() - start_time)
    input_power = torque * rpm * 3.14159/30
    output_power = current * voltage
    efficency = output_power/input_power * 100
    df = pd.concat([df, pd.DataFrame({'Torque (Nm)': [torque], 'Temp1 (V)': [temp1], 'Voltage': [voltage], 'Current':[current], 'Temp2 (V)':[temp2], "RPM": [rpm], "Time (Seconds)": [current_time], "Input Power": [input_power], "Output Power": [output_power], "Efficiency":[efficency]})], ignore_index=True)
    print(df)
    write_dataframe_to_csv(df, 'data.csv')


def write_dataframe_to_csv(dataframe, filepath):
    dataframe.to_csv(filepath, index=False, header=True)

try:
    
    thread1 = threading.Thread(target=Encoder) #Initializes Encoder 
    thread1.start()

    while True:
        add_data()    
        time.sleep(1)
   
    
except KeyboardInterrupt:
    exit()