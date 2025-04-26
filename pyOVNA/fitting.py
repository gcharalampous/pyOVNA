import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.optimize import curve_fit
from scipy.signal import find_peaks



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
        frequencies = raw_spectrum[i]['frequency']
        transmission = raw_spectrum[i]['amplitude_raw']

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


def fit_propagation_length(x_data, y_data, x_label='Propagation Length (cm)'):
    slope, intercept, _, _, _ = linregress(x_data, y_data)

    def plot_propagation_length(x_data, y_data, slope, intercept):
        X_fit = np.linspace(0, 2)
        Y_fit = slope * X_fit + intercept
        px = 1 / plt.rcParams['figure.dpi']
        fig, ax = plt.subplots(figsize=(512 * px, 256 * px))
        ax.scatter(x_data, y_data, color='blue', label='Measured Data')
        ax.plot(X_fit, Y_fit, color='red', label=f'Fit (Slope: {slope:.2f} dB/cm)')
        ax.set_xlabel(x_label)
        ax.set_ylabel('y_label')
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        return ax
    ax = plot_propagation_length(x_data, y_data, slope, intercept)
    
    return slope, intercept, ax


def fano_resonance_equation(f, f0, q, gamma, a, b):
    """
    Fano resonance equation.
    f: Frequency
    f0: Resonance frequency
    q: Fano parameter
    gamma: Linewidth
    a: Amplitude
    b: Offset
    """
    epsilon = (f - f0) / (gamma)
    return a * ((q + epsilon)**2 / (1 + epsilon**2)) + b # Fano resonance function


def fit_fano_resonance(frequencies, powers):
    """
    Fit the Fano resonance to the data.
    frequencies: Array of frequency values
    powers: Array of power values
    """
    # Initial guess for parameters: f0, q, gamma, a, b
    initial_guess = [ frequencies[np.argmin(powers)], 1, 0.01, np.ptp(powers), np.min(powers)]
    popt, pcov = curve_fit(fano_resonance_equation, frequencies, powers, p0=initial_guess)
    return popt, pcov


def calculate_q_numerically(frequencies, powers):
    """
    Calculate the Q factor numerically from the data in dB.
    frequencies: Array of frequency values
    powers: Array of power values in linear scale
    """
    # Convert powers to dB
    powers_db = 20 * np.log10(powers)

    # Find the notch (minimum) and half-maximum points in dB
    notch_index = np.argmin(powers_db)
    notch_frequency = frequencies[notch_index]
    half_maximum_db = np.min(powers_db) + 6  # Half-maximum is 3 dB above the minimum in dB scale

    # Find the frequencies at half-maximum in dB
    left_indices = np.where(powers_db[:notch_index] >= half_maximum_db)[0]
    right_indices = np.where(powers_db[notch_index:] >= half_maximum_db)[0]
    
    if left_indices.size == 0 or right_indices.size == 0:
        raise ValueError("Unable to find half-maximum points in dB. Check the data or adjust the half-maximum calculation.")
    
    
    left_half_index = left_indices[-1]
    right_half_index = right_indices[0] + notch_index

    # Calculate Full-width half maximum (FWHM) in dB
    fwhm = frequencies[right_half_index] - frequencies[left_half_index]
    
    # print('power_left:', powers_db[left_half_index])
    # print('power_right:', powers_db[right_half_index])
    # [print('power_notch:', powers_db[notch_index])]

    # Calculate Q factor
    Q = notch_frequency / fwhm
    return Q