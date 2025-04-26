import numpy as np
from pyOVNA.io import OVNAREADER
from pyOVNA.filters import supergf
import matplotlib.pyplot as plt

def read_ovna_file(file_paths):
    """
    Reads and processes OVNA (Optical Vector Network Analyzer) data files.
    This function takes a list of file paths, reads the data from each file using the `OVNAREADER` function, 
    applies a super-Gaussian filter to the frequency domain data, and computes the time-domain field 
    using an inverse FFT. The processed data is returned as a list of dictionaries.
    Args:
        file_paths (list of str): A list of file paths to the OVNA data files.
    Returns:
        list of dict: A list of dictionaries, each containing the following keys:
            - 'frequency' (numpy.ndarray): The frequency data from the file.
            - 'amplitude_raw' (numpy.ndarray): The raw amplitude spectrum from the file.
            - 'amplitude_filtered' (numpy.ndarray): The filtered amplitude spectrum after applying the super-Gaussian filter.
            - 'time_domain_field' (numpy.ndarray): The time-domain field obtained by applying an inverse FFT to the filtered spectrum.
    Notes:
        - The `OVNAREADER` function is assumed to read the file and return the time, frequency, electric field, 
          and spectrum data as lists of numpy arrays.
        - The `supergf` function is used to apply a super-Gaussian filter to the spectrum.
        - The filter parameters are hardcoded: `fwidth` is set to 2 THz, and `forder` is set to 10.
        - Only the first element of the returned lists from `OVNAREADER` is used for processing.
    """
    
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
        # min_index = (np.argmin(np.abs(spec)))
        # max_index = (np.argmax(np.abs(spec)))        
        results.append({
            'frequency': f,
            'amplitude_raw': spec,
            'amplitude_filtered': spec_fix,
            'time_domain_field': e_fix,
        })      
    return results



def plot_ovna_data(ovna_data: dict, labels: list[str] = []):
    """
    Plots the OVNA data.
    Args:
        ovna_data (list of dict): A list of dictionaries containing OVNA data.
        labels (list of str): A list of labels for each dataset. Defaults to an empty list.
    """
    for i, data in enumerate(ovna_data):
        plt.figure(figsize=(12, 8))
        plt.subplot(3, 1, 1)
        plt.plot(data['frequency'], 20 * np.log10(np.abs(data['amplitude_raw'])), label='Raw Amplitude')
        plt.title(f'OVNA Data {i + 1} {labels[i] if i < len(labels) else ""} - Raw Amplitude Spectrum')
        plt.xlabel('Frequency (THz)')
        plt.ylabel('Transmission (dB)')
        plt.grid()
        plt.legend()

        plt.subplot(3, 1, 2)
        plt.plot(data['frequency'], 20 * np.log10(np.abs(data['amplitude_filtered'])), label='Filtered Amplitude', color='orange')
        plt.title(f'OVNA Data {i + 1} {labels[i] if i < len(labels) else ""} - Filtered Amplitude Spectrum')
        plt.xlabel('Frequency (THz)')
        plt.ylabel('Transmission (dB)')
        plt.grid()
        plt.legend()

        plt.subplot(3, 1, 3)
        plt.plot(np.real(data['time_domain_field']), label='Time Domain Field', color='green')
        plt.title(f'OVNA Data {i + 1} {labels[i] if i < len(labels) else ""} - Time Domain Field')
        plt.xlabel('Time (ps)')
        plt.ylabel('Field Amplitude')
        plt.grid()
        plt.legend()

        plt.tight_layout()
        plt.show()