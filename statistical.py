"""
statistical.py
==============

This module provides the `statistical` class for computing basic statistical
and signal analysis metrics over a numeric signal vector.

It relies on helper functions from `common_lib` and NumPy for efficient computation.

Classes
-------
- statistical

Usage example
-------------
>>> from statistical import statistical
>>> stat = statistical(my_vector)
>>> mean = stat.mean_value()
>>> stats_summary = stat.analysis()
"""

import numpy as np
import common_lib

class statistical:
    """
    A class to perform statistical analysis on a numeric signal vector.

    Parameters
    ----------
    vector : object
        An object representing the signal. Must have:
        - `current` : list or array-like of numeric values (the actual data)
        - `n` : int, number of samples in the signal

    Attributes
    ----------
    vector : object
        The input vector object passed at initialization.
    vector_data : list or array-like
        A reference to the signal data (vector.current).

    Methods
    -------
    mean_value()
        Compute the mean of the signal.
    median()
        Compute the median of the signal.
    variance()
        Compute the variance of the signal.
    std_dev()
        Compute the standard deviation of the signal.
    min()
        Return the minimum value in the signal.
    max()
        Return the maximum value in the signal.
    range()
        Compute the range (max - min) of the signal.
    rms()
        Compute the Root Mean Square (RMS) of the signal.
    moving_average()
        Compute the moving average with window size = n/10.
    energy()
        Compute the total energy (sum of squares) of the signal.
    analysis()
        Return a dictionary with all the above statistics.
    """
    
    def __init__(self, vector):
        """
        Initialize the statistical object with a signal vector.

        Parameters
        ----------
        vector : object
            Must have attributes:
            - current: list/array of numeric values
            - n: length of the signal
        """

        self.vector     = vector
        self.vector_data = self.vector.current
    
    ##########################################

    def mean_value(self):
        """Compute the mean of the signal using common_lib."""

        mean = common_lib.mean_value(self.vector_data, self.vector.n)
        
        return mean
    
    ##########################################
    
    def median(self):
        """Compute the median of the signal."""
        
        sorted_vector = sorted(self.vector_data)
        
        mid_point = self.vector.n // 2
        
        if self.vector.n % 2 == 1:
            median = sorted_vector[mid_point]
        else:
            median = (sorted_vector[mid_point - 1] + sorted_vector[mid_point]) / 2

        return median
        
    ##########################################
    
    def variance(self):
        """Compute the variance of the signal using common_lib."""
        
        variance = common_lib.variance(self.vector_data, self.vector.n)
    
        return variance

    ##########################################
    
    def std_dev(self):
        """Compute the standard deviation using variance and common_lib."""

        std_dev = common_lib.std_dev(self.variance())
        
        return std_dev

    ##########################################
    
    def min(self):
        """Return the minimum value of the signal."""

        min_value = min(self.vector_data)
        
        return min_value

    ##########################################
    
    def max(self):
        """Return the maximum value of the signal."""
        
        max_value = max(self.vector_data)
        
        return max_value

    ##########################################
    
    def range(self):
        """Compute the range (max - min) of the signal."""

        rng = self.max() - self.min()
        
        return rng

    ##########################################
    
    def rms(self):
        """Compute the Root Mean Square (RMS) of the signal."""

        s = 0
        
        for value in self.vector_data:
            s += value ** 2

        rms = np.sqrt(s / self.vector.n)
        
        return rms

    ##########################################

    def moving_average(self):
        """
        Compute the moving average over the signal.

        Uses a window size of n/10 samples.
        """

        window_size = int(self.vector.n / 10)
    
        averages = []
        for i in range(self.vector.n - window_size + 1):
            window = self.vector_data[i:i+window_size]
            avg = sum(window) / window_size
            averages.append(avg)
    
        return averages

    ##########################################

    def energy(self):
        """Compute the total energy (sum of squares) of the signal."""

        energy = 0
        
        for value in self.vector_data:
            energy += value ** 2
                
        return energy

    ##########################################
    
    def analysis(self):
        """
        Compute and return all statistical metrics in a dictionary.

        Returns
        -------
        dict
            Dictionary containing:
            - mean_value
            - median
            - variance
            - std_dev
            - min
            - max
            - range
            - rms
            - moving_average
            - energy
        """

        analysis = {
            
            'mean_value'      : self.mean_value(),
            'median'          : self.median(),
            'variance'        : self.variance(),
            'std_dev'         : self.std_dev(),
            'min'             : self.min(),
            'max'             : self.max(),
            'range'           : self.range(),
            'rms'             : self.rms(),
            'moving_average'  : self.moving_average(),
            'energy'          : self.energy()
            
        }
        
        return analysis

    ##########################################
