import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

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


