"""
signal_process.py
=================

This module defines the `signal_process` class, which performs basic
signal processing operations on a time-domain vector, such as Fourier transform,
power spectral density calculation, phase extraction, and integration.

Dependencies
------------
- numpy
- scipy.fft
- scipy.signal
- scipy.integrate
"""

import numpy as np
from scipy.fft import rfft
from scipy.fft import rfftfreq
from scipy.signal import periodogram
from scipy.integrate import cumulative_trapezoid

class signal_process:
    """
    Perform signal processing transformations and calculations on a vector.

    Parameters
    ----------
    vector : vector
        A `vector` object containing the signal data to process.
    time_step : float
        Time interval between samples in the signal.

    Attributes
    ----------
    vector : vector
        The original vector object.
    time_step : float
        Sampling interval.
    vector_data : list or array-like
        Signal data extracted from the vector.
    """

    def __init__(self, vector, time_step):
        self.vector        = vector
        self.time_step     = time_step
        self.vector_data   = self.vector.current

    ##########################################
        
    def frequencies(self):
        """
        Compute the frequency bins corresponding to the real FFT.

        Returns
        -------
        freq : ndarray
            Array of frequency values.
        """

        freq = rfftfreq(self.vector.n, d = 1.0/self.time_step)
    
        return freq

    ##########################################
        
    def fourier(self):
        """
        Compute the real-valued Fast Fourier Transform (FFT) of the signal.

        Returns
        -------
        fourier : ndarray
            Complex-valued FFT coefficients.
        """

        fourier = rfft(self.vector_data)
    
        return fourier

    ##########################################
        
    def amplitude(self):
        """
        Compute the amplitude spectrum from the FFT.

        Returns
        -------
        ampl : ndarray
            Amplitude values scaled by signal length.
        """

        ampl = 2.0 * np.abs(self.fourier()) / self.vector.n
    
        return ampl

    ##########################################
    
    def phase(self):
        """
        Compute the phase spectrum (in radians) of the signal.

        Returns
        -------
        phs : ndarray
            Phase angles corresponding to FFT coefficients.
        """

        phs = np.angle(self.fourier())
    
        return phs

    ##########################################
    
    def psd(self):
        """
        Compute the power spectral density (PSD) using the periodogram.

        Returns
        -------
        freqs_psd : ndarray
            Array of frequency bins.
        psd : ndarray
            Power spectral density values.
        """

        freqs_psd, psd = periodogram(self.vector_data, fs=1.0/self.time_step)
    
        return freqs_psd, psd

    ##########################################

    def integral(self):
        """
        Compute the cumulative integral of the signal using the trapezoidal rule.

        Returns
        -------
        integ : list
            Integrated signal values as a list.
        """

        data  = np.asarray(self.vector_data)
        integ = cumulative_trapezoid(data, dx = self.time_step, initial=0)
        integ = integ.tolist()
    
        return integ

    ##########################################
