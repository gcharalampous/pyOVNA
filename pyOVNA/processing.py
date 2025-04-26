import numpy as np
from pyOVNA.io import OVNAREADER
from pyOVNA.filters import supergf
import matplotlib.pyplot as plt

def read_ovna_file(file_paths):
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


def fit_spectrum_peaks(distance_points: np.ndarray, raw_spectrum: np.ndarray, labels: list[str] = []):
    """
    Detects peaks in the transmission spectrum, fits a polynomial to the detected peaks, 
    calculates the average power loss, and generates plots for visualization.
        distance_points (np.ndarray): Array of integers specifying the minimum distance 
                                       between peaks for each spectrum.
        raw_spectrum (np.ndarray): Array of shape (n, 2), where each element contains 
                                   frequency and transmission data for a spectrum.
                                   raw_spectrum[i][0] corresponds to the frequency array, 
                                   and raw_spectrum[i][1] corresponds to the transmission array.
        labels (list[str], optional): List of labels corresponding to each spectrum. 
                                      Defaults to an empty list.
        list[float]: A list of average power loss values (in dB) for each spectrum.
    Notes:
        - The function assumes that the transmission data is provided in linear scale 
          and converts it to dB scale for processing.
        - A first-degree polynomial is fitted to the detected peaks for each spectrum.
        - The average power loss is computed as the mean of the fitted polynomial values.
        - Plots are generated for each spectrum, showing the transmission, detected peaks, 
          and the fitted polynomial.
    Example:
        >>> distance_points = np.array([50, 60])
        >>> raw_spectrum = [
        ...     (np.linspace(0, 10, 1000), np.random.random(1000)),
        ...     (np.linspace(0, 10, 1000), np.random.random(1000))
        ... ]
        >>> labels = ["Spectrum 1", "Spectrum 2"]
        >>> avg_loss = fit_spectrum_peaks(distance_points, raw_spectrum, labels)
        >>> print(avg_loss)
    """
    
    avg_loss = [0] * len(labels)
    
    for i in range(len(labels)):
        frequencies = raw_spectrum[i][0]
        transmission = raw_spectrum[i][1]

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
        print(f"Average Power Loss for {labels[i]}: {avg_loss[i]} dB")
        
        plt.figure(figsize=(5.12, 2.56), dpi=100)
        plt.plot(frequencies, 20 * np.log10(np.abs(transmission)), label='Transmission', linewidth=0.5, alpha=0.7)
        plt.plot(frequencies[peaks], 20 * np.log10(np.abs(transmission[peaks])), 'ro', label='Peaks')
        plt.plot(x_poly, y_poly, label='Fitted Polynomial', color='orange')
        plt.xlabel('Frequency (THz)')
        plt.ylabel('Transmission (dB)')
        plt.title(f'Transmission for {labels[i]}')
        plt.legend()
        plt.show()
    
    return avg_loss
from scipy.signal import find_peaks