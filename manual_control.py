"""
TODO: 
    1) Parametrized Random Movements
    2) Record camera in the same time? and then run YOLO / detection to check child presence
    3) Record sound
    4) Record movements at synch
    5) Sound generation + markers
    6) Light RGB
    7) Bubble
    
    http://192.168.175.63/download?file=0.jpg
    http://192.168.175.63/
    http://192.168.175.63/erase
    http://192.168.175.63/setVolume?level=30
    http://192.168.175.63/playSong?song=1&loop=0
    http://192.168.175.63/stopMusic
    
"""

import keyboard
import requests

# Replace with the IP address of your ESP32 robot
ROBOT_IP = "192.168.175.63"
ESP32_IP = "http://192.168.175.63/get-integer"

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
def main():
    print("Use arrow keys to control the robot. Press 'Esc' to exit.")

    while True:
        try:
            response = requests.get(ESP32_IP)
            print(response.text)
            if keyboard.is_pressed('up'):
                # Move forward
                send_command(120, 'forward', 120, 'forward')
            elif keyboard.is_pressed('down'):
                # Move backward
                send_command(120, 'backward', 120, 'backward')
            elif keyboard.is_pressed('left'):
                # Turn left (left motor backward, right motor forward)
                send_command(120, 'backward', 120, 'forward')
            elif keyboard.is_pressed('right'):
                # Turn right (left motor forward, right motor backward)
                send_command(120, 'forward', 120, 'backward')
            elif keyboard.is_pressed('esc'):
                print("Exiting program.")
                break
            else:
                # Stop the robot if no keys are pressed
                send_command(0, 'forward', 0, 'forward')
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()
