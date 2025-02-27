import os
import requests
import cv2
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import sounddevice as sd

# Constants
IPadd = "192.168.234.166" #"192.168.234.245"
ESP32_URL = "http://" + str(IPadd) + "/download"  # Replace with your ESP32 IP address
SAVE_PATH = "downloaded_images"
SAVE_PATH_touch = "touch_recording"
VIDEO_OUTPUT_PATH = "output_video.avi"
FPS = 10  # Frames per second for the video

def download_touch_recording():
    os.makedirs(SAVE_PATH_touch, exist_ok=True)
    file_name = "touch_log.csv"
    response = requests.get(ESP32_URL + "?file=" + str(file_name))
    if response.status_code == 200:
        with open(f"{SAVE_PATH_touch}/{file_name}", "wb") as file:
            file.write(response.content)
            
def download_raw_recording():
    os.makedirs(SAVE_PATH_touch, exist_ok=True)
    file_name = "audio.raw"
    response = requests.get(ESP32_URL + "?file=" + str(file_name))
    if response.status_code == 200:
        with open(f"{SAVE_PATH_touch}/{file_name}", "wb") as file:
            file.write(response.content)
    
def download_images():
    """Download all .jpg images from ESP32"""
    os.makedirs(SAVE_PATH, exist_ok=True)
    i = 1  # Image counter
    while True:
        file_name = "video_" + str(i) + ".jpg"
        print(f"Downloading {file_name}...")
        
        # Request the image from the ESP32 server

        response = requests.get(ESP32_URL + "?file=" + str(file_name))

        
        # If the image is found, save it
        if response.status_code == 200:
            with open(f"{SAVE_PATH}/{file_name}", "wb") as file:
                file.write(response.content)
            i += 1
        else:
            print("No more images found.")
            break

def create_video_from_images():
    """Create a video from downloaded images."""
    images = []
    
    # Sort the files by name (assuming the order is important)
    image_files = sorted(Path(SAVE_PATH).glob("*.jpg"))
    
    # Read images into a list
    for image_file in image_files:
        img = cv2.imread(str(image_file))
        if img is not None:
            images.append(img)
        else:
            print(f"Failed to read {image_file}")
    
    # If no images were found, return
    if len(images) == 0:
        print("No valid images found to create a video.")
        return
    
    # Get the size of the first image
    height, width, layers = images[0].shape
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(VIDEO_OUTPUT_PATH, fourcc, FPS, (width, height))
    
    # Write images to video
    for img in images:
        video_writer.write(img)
    
    # Release the VideoWriter and clean up
    video_writer.release()
    print(f"Video created successfully at {VIDEO_OUTPUT_PATH}")


# Function to load CSV content into a NumPy array
def csv_to_numpy(file_path):
    try:
        # Read the CSV file into a Pandas DataFrame
        data = pd.read_csv(file_path)

        # Check if the required columns exist Timestamp (ms),Touch Value
        if 'Timestamp (ms)' not in data.columns or ' Touch Value' not in data.columns:
            print("Error: The CSV file must contain 'time stamp' and 'value' columns.")
            return None

        # Convert the DataFrame to a NumPy array
        numpy_array = data[['Timestamp (ms)', ' Touch Value']].to_numpy()

        return numpy_array

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except pd.errors.ParserError:
        print("Error: Failed to parse the CSV file. Check its format.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
  
    
def download_data_all():
    print("Starting touch log download...")
    download_touch_recording()
    
    print("Starting image download...")
    #download_images()
    
    print("Creating video from downloaded images...")
    #create_video_from_images()
    file_name = "touch_log.csv"
    file_path = SAVE_PATH_touch + "/" + file_name
    touch_np = csv_to_numpy(file_path)
    plt.plot(touch_np[:,0], touch_np[:,1])
    
if __name__ == "__main__":
    print("Starting touch log download...")
    download_touch_recording()
    
    print("Starting image download...")
    #download_images()
    
    print("Creating video from downloaded images...")
    #create_video_from_images()
    file_name = "touch_log.csv"
    file_path = SAVE_PATH_touch + "/" + file_name
    touch_np = csv_to_numpy(file_path)
    plt.plot(touch_np[:,0], touch_np[:,1])
    
# =============================================================================
#     download_raw_recording()
#         # File parameters (adjust these based on your raw audio format)
#     file_path = SAVE_PATH_touch + "/" + "audio.raw"  # Path to your raw file
#     sample_rate = 1000      # Sampling rate in Hz
#     dtype = np.int16         # Data type of each sample (e.g., int16 for 16-bit PCM)
#     
#     # Load the raw audio data into a numpy array
#     try:
#         raw_data = np.fromfile(file_path, dtype=dtype)
#         
#         sample_rate = raw_data.shape[0] / 10
#     
#         # Create a time axis for plotting
#         time = np.linspace(0, len(raw_data) / sample_rate, num=len(raw_data))
#     
#         # Plot the audio waveform
#         plt.figure(figsize=(10, 6))
#         plt.plot(time, raw_data, label="Audio Signal")
#         plt.title("Audio Waveform")
#         plt.xlabel("Time (seconds)")
#         plt.ylabel("Amplitude")
#         plt.legend()
#         plt.grid()
#         plt.show()
#         
#         signal = (raw_data - np.mean(raw_data))*10
#         
#         signalfft = np.fft.fftshift(np.fft.fft(signal))
#         
#         gap = 10000
#         signalfft[signalfft.shape[0]//2 - gap:signalfft.shape[0]//2 + gap] = 0
#         signal_filtered = np.real(np.fft.ifft(np.fft.fftshift(signalfft)))
#         
#         sd.play(signal_filtered, sample_rate)
#         sd.wait()  # Wait until the sound has finished playing
#         
#     except FileNotFoundError:
#         print(f"File not found: {file_path}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
# 
# =============================================================================
