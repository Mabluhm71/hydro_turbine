#This is the control unit that runs the Raspberry PI DAQ

#from Encoder import Encoder, get_rpm
#from Sensor import run_Sensor
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
df = pd.DataFrame(columns = ['Torque (Nm)', 'Temp1 (V)', 'Voltage', 'Current', 'Temp2 (V)', "RPM", "Time (Seconds)"], )


# Initialize the tkinter window
window = tk.Tk()
window.title("Live Updating Data")

# Create a figure and axis for the graph
fig, ax = plt.subplots(3, sharey=False)
fig.subplots_adjust(wspace=0.3, hspace=0.3)
ax2 = ax[1].twinx()

# Create a function to update the graph with new data every second
def update_graph():
    global df
    global ax2
    i=0
    while i < 5: 
        torque, temp1, temp2, voltage, current, temp2 = rand_data()
        #rpm = get_rpm()
        # add rpm to concat call below here
        # add time as current_time - start time
        rpm = random.randint(600, 800)
        current_time = (time.time() - start_time)
        df = pd.concat([df, pd.DataFrame({'Torque (Nm)': [torque], 'Temp1 (V)': [temp1], 'Voltage': [voltage], 'Current':[current], 'Temp2 (V)':[temp2], "RPM": [rpm], "Time (Seconds)": [current_time]})], ignore_index=True)
                    #   , 'Temp1 (V)':temp1, 'Voltage':voltage, 'Current':current, 'Temp2 (V)':temp2})
        i+=1
        
        print(df)
            # Create csv file / append to csv

    # Generate some new data
    # Needs to be the x-y values from the main.py function that has all data
    y_torque = df["Torque (Nm)"].tolist()
    x_time = df["Time (Seconds)"].tolist()
    y_current = df["Current"].tolist()
    y_voltage = df["Voltage"].tolist()
    y_RPM = df["RPM"].tolist()

    
    # Clear the old data from the axis
    ax[0].clear()
    ax2.clear()
    ax[1].clear()
    ax[2].clear()
    # Plot the new data
    ax[0].set_title("Torque Output Over Time")
    ax[0].set_xlabel("Time (Seconds)")
    ax[0].set_ylabel("Torque (Nm)")
    ax[1].set_title("Current and Voltage Output Over Time")
    ax[1].set_xlabel("Time (Seconds)")
    ax[1].set_ylabel("Current (Amps)")

    ax[2].set_title("RPM Over Time")
    ax[2].set_xlabel("Time (Seconds)")
    ax[2].set_ylabel("RPM")


    ax[0].plot(x_time, y_torque)
    ax[1].plot(x_time, y_current)
    ax[1].legend(['Current'])
    ax2.set_ylabel("Voltage (V)")
    ax2.plot(x_time, y_voltage, color='red')
    ax2.legend(['Voltage'])
    ax[2].plot(x_time, y_RPM)
    
    
    write_dataframe_to_csv(df, 'data.csv')
    # Redraw the canvas
    canvas.draw()
    window.after(5000, update_graph)


def write_dataframe_to_csv(dataframe, filepath):
    """
    Writes a pandas DataFrame to a CSV file without index and with header.

    Parameters:
        dataframe (pandas.DataFrame): The DataFrame to be written to the CSV file.
        filepath (str): The path to the CSV file.

    Returns:
        None
    """
    dataframe.to_csv(filepath, index=False, header=True)

    # Example usage:
    # Assuming you have a DataFrame named 'df' and you want to write it to 'data.csv' file
    #write_dataframe_to_csv(df, 'data.csv')


# Used to export data to CSV file so that data can be used later
def create_csv_file(filename, headers, *data):
    """
    Creates a CSV file with given filename, headers, and data.
    
    Args:
        filename (str): Name of the CSV file to be created.
        headers (list): List containing headers for the CSV file.
        *data: Variable length argument containing arrays of data.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        # Zip data arrays together to iterate over them simultaneously
        for row in zip(*data):
            writer.writerow(row)


#Used to resize window when it is resized
def on_resize(event):
    fig.set_size_inches(event.width / fig.dpi, event.height / fig.dpi)
    canvas.draw()

# run sensor and rpm data at the same time
# Sample rpm and sensor data at the same time so that they correpond to eachother

# Running the Encoder every 0.25 seconds and average all sensors over 0.25 seconds

# Sample them 10 times


# Create GUI Window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
update_graph()
# Connect the resize event to the on_resize function
window.bind('<Configure>', on_resize)

def test():
    print("THIS IS A TEST THIS IS A TEST THIS IS A TEST")
window.mainloop()

try:


    """
    thread1 = threading.Thread(target=Encoder) #Initializes Encoder 
    thread1.start()

    chan0, chan1, chan2, chan3, chan4, chan5 = run_Sensor() #Change sensor so that it only returns values one value for each channel
    RPM.appendget_rpm() # retrun rpm
    """
    # while True: 
    #     i=0
    #     while i < 5: 
    #         torque, temp1, temp2, voltage, current, temp2 = rand_data()
    #         df = pd.concat([df, pd.DataFrame({'Torque (Nm)': [torque], 'Temp1 (V)': [temp1], 'Voltage': [voltage], 'Current':[current], 'Temp2 (V)':[temp2]})], ignore_index=True)
    #                 #   , 'Temp1 (V)':temp1, 'Voltage':voltage, 'Current':current, 'Temp2 (V)':temp2})
    #         i+=1
        
    #     time.sleep(5)
            # Create csv file / append to csv
    
    test()
    time.sleep(5)

    
except KeyboardInterrupt:
    exit()