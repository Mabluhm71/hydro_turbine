#This is the control unit that runs the Raspberry PI DAQ

#from Encoder import Encoder, get_rpm
from Encoder import Encoder, get_rpm
from Sensor import run_Sensor
from test_data import rand_data
from gpiozero import LED
import pandas as pd
import threading
import time
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



#////////////////////////////////////////////////////////////////////////////////////////
#Notes
# Still need to implement getting RPM and Time into the data frame so that I can graph values against time and display RPM
# Still need to implement creating and appending to a new csv once the script is run so that data can easily be retrived
# Still need ti implement making the display look nice and adding data labels
#////////////////////////////////////////////////////////////////////////////////////////

# Constants
waterLED = LED(27)
gearbox_ratio = 5
start_time = time.time()
filename = "Output.csv"
#df = pd.DataFrame(columns = ['Torque (Nm)', 'Voltage', 'Current', "Gen RPM", "Time (Seconds)", "Input Power", "Output Power", "Efficiency", "Resistance"], )
df = pd.DataFrame()
# Create a function to update the graph with new data every second
def add_data():
    global df
    torque, temp1, temp2, voltage, current, water = run_Sensor()
    if water > 0.1:
        water()
    input_rpm = get_rpm()
    gen_rpm = input_rpm *gearbox_ratio
    # add rpm to concat call below here
    # add time as current_time - start time
    current_time = (time.time() - start_time)
    output_power = current * voltage
    if current <= 0: 
        resistance = 0
    else:
        resistance = voltage/current
    df = pd.concat([df, pd.DataFrame({'Voltage': [voltage], 'Current':[current], "Gen RPM": [gen_rpm], "Time (Seconds)": [current_time], "Output Power": [output_power], "Resistance":[resistance], "Generator Temp": [temp1], "Gearbox Temp": [temp2]})], ignore_index=True)
    print(df)
    write_dataframe_to_csv(df, 'data.csv')

        # Update large numbers
    label1.config(text="RPM: " + str(gen_rpm))
    label2.config(text="Power Output:  " + str(output_power) + " Watts")

    # Update graphs
    ax1.clear()
    ax2.clear()
    ax3.clear()

    ax1.plot(df['Time (Seconds)'], df['Voltage'], linewidth = 2.0, color = "orange")
    ax1.set_ylabel('Voltage (Volts)')
    ax1.legend(['Voltage'])
    ax0 = ax1.twinx()
    ax0.plot(df['Time (Seconds)'], df['Current'], linewidth = 2.0, color = "blue")
    ax0.set_ylabel('Current (Amps)')
    ax0.set_xlabel('Time (Seconds)')
    ax0.legend(['Current'])

    ax2.plot(df['Time (Seconds)'], df['Gen RPM'], linewidth = 2.0, color = "black")
    ax2.set_ylabel('RPM')
    ax2.set_xlabel('Time (Seconds)')
    ax2.legend(['Gen RPM'])

    ax3.plot(df['Time (Seconds)'], df['Output Power'], linewidth = 2.0, color = "red")
    ax2.set_ylabel('Output Power (Watts)')
    ax2.set_xlabel('Time (Seconds)')
    ax3.legend(['Output Power'])

    canvas1.draw()
    canvas2.draw()
    canvas3.draw()


def write_dataframe_to_csv(dataframe, filepath):
    dataframe.to_csv(filepath, index=False, header=True)

def water():
    waterLED.on()
    
try:
    
    thread1 = threading.Thread(target=Encoder) #Initializes Encoder 
    thread1.start()

        # Create the main window
    root = tk.Tk()
    root.title("Hydro Turbine Data")

    # Create figure and axes for each graph
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()

    # Create canvases for each graph
    canvas1 = FigureCanvasTkAgg(fig1, master=root)
    canvas1_widget = canvas1.get_tk_widget()
    canvas1_widget.grid(row=0, column=0, sticky="nsew")

    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas2_widget = canvas2.get_tk_widget()
    canvas2_widget.grid(row=1, column=0, sticky="nsew")

    canvas3 = FigureCanvasTkAgg(fig3, master=root)
    canvas3_widget = canvas3.get_tk_widget()
    canvas3_widget.grid(row=2, column=0, sticky="nsew")

    # Create labels for large numbers
    label1 = tk.Label(root, text="", font=("Arial", 14))
    label1.grid(row=0, column=1, sticky='w')

    label2 = tk.Label(root, text="", font=("Arial", 14))
    label2.grid(row=1, column=1, sticky='w')

    label3 = tk.Label(root, text="", font=("Arial", 14))
    label3.grid(row=2, column=1, sticky='w')

    # Start a thread to continuously update data
    update_thread = threading.Thread(target=add_data)
    update_thread.daemon = True
    update_thread.start()

    # Configure grid weights to make the graphs expandable
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Start the tkinter main loop
    root.mainloop()


    # while True:
    #     add_data()    
    #     time.sleep(2)
   
    
except KeyboardInterrupt:
    exit()