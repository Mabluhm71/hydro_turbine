from gpiozero import Button
import threading 
import time

# Global variable to be incremented
press_count = 0
prev_count = 0
start_time = time.time()
next_time = 0
rpm = 0
TPS_to_RPM_conversion = 60/2048

gpio_pin = 17
button = Button(gpio_pin, pull_up=False)  # If pull_up=True, use pull-up resistor

def counter():
    global press_count
    press_count += 1
    #print("Rising edge detected! Press count:", press_count)


def get_rpm():
    while True: 
        global press_count
        global prev_count
        global start_time
        global rpm
        current_time = time.time()
        # print("The Start Time is " + str(start_time))
        # print("The current time is " + str(current_time))
        time_diff = (current_time - start_time)# in seconds
        # print(time_diff)
        start_time = current_time
        count_diff = press_count - prev_count
        prev_count = press_count #in ticks need to convert to rotations 
        # print(count_diff)
        if time_diff == 0:
            rpm = 0
        else:
            rpm = (count_diff/time_diff) * TPS_to_RPM_conversion
        # print("rpm " + str(rpm))
        # time.sleep(5)
        return(rpm)


def Encoder():
    while True:
        button.when_pressed = counter


# # Create threads
# thread1 = threading.Thread(target=get_rpm)
# thread2 = threading.Thread(target=Encoder)

# # Start threads
# thread1.start()
# thread2.start()
