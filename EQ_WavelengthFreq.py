import numpy as np
from scipy.fft import fft
from tkinter import filedialog
import tkinter as tk


def open_file_dialog(index = ""):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title=f"Select a {index} .xlsx file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    return file_path

txtfile = open_file_dialog(".txt")

data = np.genfromtxt(txtfile, skip_header=2) 

# Extract time and acceleration columns
acceleration_data = data  # Time steps (column 1)
num_data_points = len(acceleration_data)
time_interval = 0.005


time_steps = np.arange(0, num_data_points * time_interval, time_interval)


# Perform the Fast Fourier Transform (FFT) on the acceleration data
fft_result = fft(acceleration_data)

# Compute the power spectral density (PSD) to find the dominant frequency component
psd = np.abs(fft_result) ** 2

# Find the index of the maximum value in the PSD (corresponding to the dominant frequency)
dominant_frequency_index = np.argmax(psd)

# Get the dominant frequency in Hz
sampling_rate = 1.0 / (time_steps[1] - time_steps[0])  # Calculate sampling rate
dominant_frequency = dominant_frequency_index * sampling_rate / len(time_steps)

# Calculate the wavelength using the dominant frequency and seismic wave velocity
# You will need to specify the appropriate seismic wave velocity for your data.
seismic_wave_velocity = 300.0  # Example seismic wave velocity in m/s (depends on geological conditions)

wavelength = seismic_wave_velocity / dominant_frequency

# Print the results
print("Dominant Frequency (Hz):", dominant_frequency)
print("Wavelength (meters):", wavelength)
