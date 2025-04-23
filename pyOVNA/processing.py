import numpy as np
from pyOVNA.io import OVNAREADER
from pyOVNA.filters import supergf
import matplotlib.pyplot as plt

def process_file(file_paths):
    results = []
    for path in file_paths:
        t, f, e, spec = OVNAREADER(path, DEBUG=False)
        t = t[0]
        e = e[0]
        f = f[0]
        spec = spec[0]
        fcenter = np.mean(f)
        fwidth = 2  # THz
        forder = 10
        spec_fix = spec * supergf(f, fcenter, fwidth, forder)
        e_fix = np.fft.fftshift(np.fft.ifft(spec_fix))
        results.append((f, spec, spec_fix, e_fix))
    return results


def process_and_plot(file_path, distance_points, data):
    """
    Process each file's data to extract peaks, fit a polynomial,
    calculate average loss, and plot the transmission.

    Parameters:
        file_path (list of str): List of file paths.
        distance_points (list of int): Distance points for peak detection.
        data (list): Processed data from each file.
    
    Returns:
        list: Average power loss values (dB) for each file.
    """
    avg_loss = [0] * len(file_path)
    
    for i in range(len(file_path)):
        frequencies = data[i][0]
        transmission = data[i][1]

        # Get the peaks
        peaks, _ = find_peaks(20 * np.log10(np.abs(transmission)), distance=distance_points[i])
        
        # Fit the data to a polynomial
        x_fit = frequencies[peaks]
        y_fit = 20 * np.log10(np.abs(transmission[peaks]))
        
        coeffs = np.polyfit(x_fit, y_fit, 1)
        poly = np.poly1d(coeffs)
        x_poly = np.linspace(min(x_fit), max(x_fit), 1000)
        y_poly = poly(x_poly)

        # Calculate average loss and output plot
        avg_loss[i] = np.mean(y_poly)
        print(f"Average Power Loss for {file_path[i]}: {avg_loss[i]} dB")
        
        plt.figure(figsize=(5.12, 2.56), dpi=100)
        plt.plot(frequencies, 20 * np.log10(np.abs(transmission)), label='Transmission', linewidth=0.5, alpha=0.7)
        plt.plot(frequencies[peaks], 20 * np.log10(np.abs(transmission[peaks])), 'ro', label='Peaks')
        plt.plot(x_poly, y_poly, label='Fitted Polynomial', color='orange')
        plt.xlabel('Frequency (THz)')
        plt.ylabel('Transmission (dB)')
        plt.title(f'Transmission for {file_path[i]}')
        plt.legend()
        plt.show()
    
    return avg_loss
from scipy.signal import find_peaks