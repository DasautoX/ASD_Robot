

import keyboard
import requests
import time
import numpy as np
from download_video import download_data_all

# Replace with the IP address of your ESP32 robot
ROBOT_IP = "192.168.234.166" #"192.168.234.245"
#ESP32_IP_getPush = "http://192.168.234.245/get-integer"

ESP32_IP_getPush = "http://" + str(ROBOT_IP) + "/get-integer"

# Function to send motor commands
def send_command(motor1_speed, motor1_dir, motor2_speed, motor2_dir):
    url = f"http://{ROBOT_IP}/motor1?speed={motor1_speed}&dir={motor1_dir}&speed2={motor2_speed}&dir2={motor2_dir}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command sent: {url}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Failed to send command: {e}")

# Key event loop

def send_music_play(file_number, loop):
    url = f"http://{ROBOT_IP}/playSong?song={file_number}&loop={loop}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command sent: {url}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Failed to send command: {e}")
        
        
def send_music_stop():
    url = f"http://{ROBOT_IP}/stopMusic"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command sent: {url}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Failed to send command: {e}")
        
        
def set_music_volume(volume):
    volume = int(volume)
    url = f"http://{ROBOT_IP}/setVolume?level={volume}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command sent: {url}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Failed to send command: {e}")

def set_big_button_led_period(period):
    period = int(period)
    url = f"http://{ROBOT_IP}/setButtonLedPeriod?period={period}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command sent: {url}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Failed to send command: {e}")
        
def send_record_start():
    url = f"http://{ROBOT_IP}/start"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command sent: {url}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Failed to send command: {e}")       

def send_record_stop():
    url = f"http://{ROBOT_IP}/stop"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command sent: {url}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Failed to send command: {e}") 
        
        
def send_erase_data():
    url = f"http://{ROBOT_IP}/erase"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command sent: {url}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Failed to send command: {e}") 
        
def robot_state_update(robot_mvmt_state, current_time, time_to_next_change, prev_tick_time, min_T, max_T, proba_mvt):
    if current_time - prev_tick_time >= time_to_next_change:
        elements = np.array([1, 2, 3, 4])
        select = robot_mvmt_state
        while select == robot_mvmt_state:
            choice = np.random.choice(elements, 1, p=proba_mvt)
            select = choice[0]
            
        time_to_next_change = np.random.uniform(min_T, max_T)
        robot_mvmt_state = select
        prev_tick_time = current_time
        return robot_mvmt_state, time_to_next_change, prev_tick_time
    else:
        return robot_mvmt_state, time_to_next_change, prev_tick_time


def handle_big_button_pressed():
    global play_file_number, static_set_big_button, led_pressed_period
    if static_set_big_button == False:
        set_big_button_led_period(int(led_pressed_period))
        time.sleep(0.1)
        send_music_play(play_file_number, loop)
        static_set_big_button = True
    

    
Speed_fwd = 120
Speed_bckwd = 120
Speed_right = 120
Speed_left = 120

min_T = 1
max_T = 2
proba_mvt = np.array([1, 1, 1, 1]) / 4
time_to_next_change = 1
big_button_state = 0
button_pressed_state = 0
play_file_number = 1
loop = 0
button_pressed_period = 10
led_pressed_period = 400
led_normal_period = 1000

pressed_but_time = time.time()
 
pushed_once_stop = False
robot_mvmt_state = 0
prev_tick_time = time.time()

def main():
    global robot_mvmt_state, time_to_next_change, prev_tick_time, button_state, pressed_but_time, led_normal_period, led_pressed_period
    global big_button_state, play_file_number, button_pressed_state, static_set_big_button, pushed_once_stop
    global Speed_fwd, Speed_bckwd, Speed_right, Speed_left, min_T, max_T, proba_mvt, button_pressed_period
    while True:
        
        if button_state == "On":
            pushed_once_stop = False

            current_time = time.time()
            robot_mvmt_state, time_to_next_change, prev_tick_time = robot_state_update(robot_mvmt_state, current_time, time_to_next_change, prev_tick_time, min_T, max_T, proba_mvt)
            
            try:
                response = requests.get(ESP32_IP_getPush)
                time.sleep(0.05)
                big_button_state = int(response.text)
                if big_button_state == 1:
                    pressed_but_time = time.time()
                    button_pressed_state = 1
                
                if button_pressed_state == 1:
                    handle_big_button_pressed()
                    time.sleep(0.1)
                    
                if time.time() - pressed_but_time > button_pressed_period:
                    button_pressed_state = 0
                    static_set_big_button = False
                    set_big_button_led_period(led_normal_period)
                    time.sleep(0.1)
                
                if robot_mvmt_state == 1:
                    # Move forward
                    send_command(Speed_fwd, 'forward', Speed_fwd, 'forward')
                elif robot_mvmt_state == 2:
                    # Move backward
                    send_command(Speed_bckwd, 'backward', Speed_bckwd, 'backward')
                elif robot_mvmt_state == 3:
                    # Turn left (left motor backward, right motor forward)
                    send_command(Speed_right, 'backward', Speed_right, 'forward')
                elif robot_mvmt_state == 4:
                    # Turn right (left motor forward, right motor backward)
                    send_command(Speed_left, 'forward', Speed_left, 'backward')
                else:
                    # Stop the robot if no keys are pressed
                    send_command(0, 'forward', 0, 'forward')
                    
                time.sleep(0.05)
                
            except Exception as e:
                print(f"Error: {e}")
                break
            
        elif button_state == "Off":
            try:
                if pushed_once_stop == False:
                    send_command(0, 'forward', 0, 'forward')
                    send_music_stop()
                    set_big_button_led_period(led_normal_period)
                    time.sleep(0.1)

                    pushed_once_stop = True
                    
            except Exception as e:
                print(f"Error: {e}")
                break
            




import tkinter as tk
import threading
import time

# Global variable to store the button state
button_state = "Off"

# Store entry field values
entry_values = []

def toggle_button():
    global Speed_fwd, Speed_bckwd, Speed_right, Speed_left, min_T, max_T, proba_mvt, button_pressed_period, led_pressed_period, led_normal_period
    """Toggle the state of the button between On and Off."""
    global button_state, entry_values
    if button_state == "Off":
        button_state = "On"
        button.config(text="On", bg="green")
        
        # Read and print values from the text entry fields
        print("Reading values from text fields:")
        entry_values.clear()  # Clear previous values
        for i, entry in enumerate(entry_fields):
            value = entry.get()
            entry_values.append(float(value))
            print(f"Field {i+1}: {value}")
        
        Speed_fwd = entry_values[0]
        Speed_bckwd = entry_values[1]
        Speed_right = entry_values[2]
        Speed_left = entry_values[3]
        min_T = entry_values[4]
        max_T = entry_values[5]
        SUM = entry_values[6] + entry_values[7] + entry_values[8] + entry_values[9]
        proba_mvt[0] = entry_values[6] / SUM #= np.array([1, 1, 1, 1]) / 4
        proba_mvt[1] = entry_values[7] / SUM
        proba_mvt[2] = entry_values[8] / SUM
        proba_mvt[3] = entry_values[9] / SUM
        volume = entry_values[10]
        set_music_volume(volume)
        button_pressed_period = entry_values[11]
        led_normal_period = entry_values[12]
        led_pressed_period = entry_values[13]
        
        send_record_start()
        time.sleep(1)

        
    else:
        button_state = "Off"
        button.config(text="Off", bg="red")
        send_record_stop()
        time.sleep(1)

def download_data():
    """Simulate downloading data."""
    download_data_all()

def monitor_button_state():
    global button_state
    while True:
        main()

# Create the main GUI window
root = tk.Tk()
root.title("ASD Intervention Robot Platform")

# Create the toggle button and set its properties
button = tk.Button(root, text="Off", bg="red", font=("Arial", 16), command=toggle_button)
button.pack(pady=10)

# Create the "Download Data" button and set its properties
download_button = tk.Button(root, text="Download Data", bg="blue", fg="white", font=("Arial", 16), command=download_data)
download_button.pack(pady=10)

# Create a frame to hold the text entry fields
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

# Create 15 text entry fields arranged in a matrix (5 columns, 3 rows)

field_names = ["Forward Speed", "Backward Speed", "Right Turn Speed", "Left Turn Speed", "min T", "max T", "Pfwd", "Pbck", "Pright", "Pleft", "Sound Volume", "Button Response Period", "Led Normal Period", "Led Pressed Period", ""]
default_value = [120, 120, 120, 120, 1, 2, 1, 1, 1, 1, 20, 10, 2000, 400, 0]
entry_fields = []
for row in range(3):  # 3 rows
    for col in range(5):  # 5 columns
        label = tk.Label(entry_frame, text=field_names[row * 5 + col], font=("Arial", 10))
        label.grid(row=row * 2, column=col, padx=5, pady=5)
        
        entry = tk.Entry(entry_frame, font=("Arial", 10))
        entry.grid(row=row * 2 + 1, column=col, padx=5, pady=5)
        entry.insert(0, str(default_value[row * 5 + col]))  # Add default value
        
        entry_fields.append(entry)

# Start the state monitoring thread
monitor_thread = threading.Thread(target=monitor_button_state, daemon=True)
monitor_thread.start()

# Start the GUI event loop
root.mainloop()

