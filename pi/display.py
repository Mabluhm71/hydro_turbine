import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import threading
import time

def generate_data():
    """Function to generate random data."""
    return random.randint(0, 100)

def update_data():
    """Function to update the data and refresh the graphs."""
    while True:
        # Generate new data
        data1 = generate_data()
        data2 = generate_data()
        data3 = generate_data()
        
        # Update large numbers
        label1.config(text=str(data1))
        label2.config(text=str(data2))
        label3.config(text=str(data3))

        # Update graphs
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax1.bar(['Data'], [data1], color='blue')
        ax2.bar(['Data'], [data2], color='red')
        ax3.bar(['Data'], [data3], color='green')
        canvas1.draw()
        canvas2.draw()
        canvas3.draw()

        # Sleep for 5 seconds
        time.sleep(5)

# Create the main window
root = tk.Tk()
root.title("Graphs and Numbers")

# Create figure and axes for each graph
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

# Create canvases for each graph
canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1_widget = canvas1.get_tk_widget()
canvas1_widget.grid(row=0, column=0)

canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2_widget = canvas2.get_tk_widget()
canvas2_widget.grid(row=0, column=1)

canvas3 = FigureCanvasTkAgg(fig3, master=root)
canvas3_widget = canvas3.get_tk_widget()
canvas3_widget.grid(row=0, column=2)

# Create labels for large numbers
label1 = tk.Label(root, text="", font=("Arial", 30))
label1.grid(row=1, column=0)

label2 = tk.Label(root, text="", font=("Arial", 30))
label2.grid(row=1, column=1)

label3 = tk.Label(root, text="", font=("Arial", 30))
label3.grid(row=1, column=2)

# Start a thread to continuously update data
update_thread = threading.Thread(target=update_data)
update_thread.daemon = True
update_thread.start()

# Start the tkinter main loop
root.mainloop()
