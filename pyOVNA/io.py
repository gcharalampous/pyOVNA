import numpy as np
import matplotlib.pyplot as plt

def OVNAREADER(filename, DEBUG=False):
    size_uint32 = '>u4'
    size_uint16 = '>u2'
    size_double = '>f8'

    with open(filename, 'rb') as FILE:
        SIZE = np.fromfile(FILE, size_uint32, count=1)[0]
        OVNAtype = np.fromfile(FILE, 'c', count=SIZE)
        _ = np.fromfile(FILE, size_uint16, count=49)
        Channels = np.fromfile(FILE, size_uint32, count=1)[0]

        N = np.zeros(Channels, dtype=int)
        cf = np.zeros(Channels, dtype='float64')
        df = np.zeros(Channels, dtype='float64')
        StartT = np.zeros(Channels, dtype='float64')

        spec, e, f, t = {}, {}, {}, {}

        for index in range(Channels):
            N[index] = np.fromfile(FILE, size_uint32, count=1)[0]
            pdata = np.fromfile(FILE, size_double, count=N[index] * 2)
            spec[index] = pdata[::2] + 1j * pdata[1::2]
            cf[index] = np.fromfile(FILE, size_double, count=1)[0]
            df[index] = np.fromfile(FILE, size_double, count=1)[0]
            StartT[index] = np.fromfile(FILE, size_double, count=1)[0] * 1000.0
            f[index] = np.arange(0, N[index]) * df[index] + cf[index]
            t[index] = np.arange(0, N[index]) / N[index] / df[index] + StartT[index]
            e[index] = np.fft.fftshift(np.fft.ifft(np.fft.fftshift(spec[index])))

            if DEBUG:
                plt.figure(index + 1)
                plt.plot(t[index], 20 * np.log10(np.abs(e[index])))
                plt.title(f"Time-domain Response (Channel {index})")
                plt.xlabel("Time (ps)")
                plt.ylabel("Amplitude (dB)")

                plt.figure((index + 1) * 10)
                plt.plot(f[index], 20 * np.log10(np.abs(spec[index])))
                plt.title(f"Frequency Spectrum (Channel {index})")
                plt.xlabel("Frequency (THz)")
                plt.ylabel("Amplitude (dB)")

    return t, f, e, spec
