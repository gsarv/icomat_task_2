"""
vector.py
=========

This module defines the `vector` class, which holds the time history of a signal
and provides methods for signal analysis, including spike detection, oscillation
detection, stall detection, filtering, and basic statistics.

Dependencies:
-------------
- numpy
- scipy.signal.detrend
- common_lib
- statistical
"""

from statistical import statistical
import common_lib
import numpy as np
from scipy.signal import detrend

class vector:
    """
    A class that encapsulates signal data and provides various signal analysis tools.

    Parameters
    ----------
    vec : list
        Time history of the examined data. Can optionally include a header as the first element.

    Attributes
    ----------
    original_data : list
        The original signal data (without header).
    current : list
        The current (possibly modified) version of the signal.
    header : str or None
        Header string if present in the input data; otherwise None.
    n : int
        Number of data points in the current signal.
    """
    
    def __init__(self, vec):
        
        self.original_data  = self.check_header(vec)[0]
        self.current        = self.check_header(vec)[0]
        self.header         = self.check_header(vec)[1]
        self.n              = self.number_values()
    
    ##########################################

    def check_header(self,vec):
        """
        Detect if the first element is a header (string) and separate it.

        Parameters
        ----------
        vec : list
            Input data, possibly with a header as the first element.

        Returns
        -------
        tuple
            (data without header, header string or None)
        """

        if isinstance(vec[0], str):
            header = vec[0]
            vec    = vec[1:]
        else:
            header = None
            vec    = vec
        
        return vec, header
    
    ##########################################

    def number_values(self):
        """
        Get the number of data points in the current signal.

        Returns
        -------
        n : int
            Number of values.
        """

        n = len(self.current)
        
        return n
    
    ##########################################

    def statistical(self):
        """
        Create a statistical analysis object for the current signal.

        Returns
        -------
        statistical
            Instance of the statistical class.
        """

        stat = statistical(self)
        
        return stat
    
    ##########################################

    def detect_spikes(self):
        """
        Detect significant spikes in the current signal using local vs. global variance.

        Returns
        -------
        spikes : list of [int, float]
            Each spike is represented as [index, value].
        """
        
        window_ratio     = 0.05
        min_stall_length = 10
        window_size      = max(int(self.n * window_ratio), min_stall_length)

        spikes = []

        padded_data = common_lib.padded_data(self.current, window_size)
        variance    = common_lib.variance(self.current, self.n)
        global_std  = common_lib.std_dev(variance)
        
        for i in range(self.n):
            window           = padded_data[i:i+window_size]
            center_idx       = window_size // 2
            window_wo_center = window[:center_idx] + window[center_idx+1:]
            n_window_center  = len(window_wo_center)

            local_mean = common_lib.mean_value(window_wo_center, n_window_center)
            local_var  = common_lib.variance(window_wo_center, n_window_center)
            local_std  = common_lib.std_dev(local_var)

            if local_std > 0:
                diff = abs(self.current[i] - local_mean)
                if diff > 4.0 * local_std:
                    spikes.append([i, self.current[i]])
        
        return spikes

    ##########################################

    def detect_oscillations(self, window_ratio):
        """
        Detect regions in the signal with periodic oscillations.
        Needs further improvement and testing for ensuring rubustness

        Returns
        -------
        osci_regions : list of [int, int]
            Each region is represented by [start index, end index].
        """

        min_cycles         = 5
        min_osci_length    = 10
        osci_regions       = []
        window_size        = max(int(self.n * window_ratio), min_osci_length)

        padded_data = common_lib.padded_data(self.current, window_size)
        variance    = common_lib.variance(self.current, self.n)
        global_std  = common_lib.std_dev(variance)

        for i in range(self.n - window_size + 1):
            start  = i
            end    = i + window_size
            window     = padded_data[start:end]
            n_window   = len(window)
            amp        = []
            length     = []

            centered   = detrend(np.array(window))
            local_var  = common_lib.variance(centered, n_window)
            local_std  = common_lib.std_dev(local_var)

            if local_std < 0.01 * global_std:
                continue

            else:
                signs            = np.sign(centered)
                zero_crossings   = np.where(np.diff(signs) != 0)[0]

                if len(zero_crossings) > min_cycles:
                    for j in range(len(zero_crossings) - 1):
                        idx1, idx2 = zero_crossings[j], zero_crossings[j+1]
                        length.append(idx2 - idx1)
                        local_amp = max(centered[idx1:idx2], key=abs)
                        amp.append(abs(local_amp))

                    amp_var  = common_lib.variance(amp, len(amp))
                    amp_std  = common_lib.std_dev(amp_var)
                    amp_mean = common_lib.mean_value(amp, len(amp))
                    
                    count = 0
                    for k in range(len(length)):
                        # more than 5 data should exists between to zero crossings, otherwise propably is noise.
                        # detected oscilation amplitudes should have small deviation, otherwise propably is noise.
                        if (length[k] >= 5) and (amp_std < 0.3 * amp_mean) :
                            count += 1
                        
                    if count > 3:
                        osci_regions.append([start, end])
        
        return osci_regions

    ##########################################

    def filtered_data(self, count):
        """
        Apply median filter to the current signal.

        Parameters
        ----------
        count : int
            Filter parameter to control window size (10 + 5*count).

        Returns
        -------
        filtered : list
            The filtered signal.
        """

        window_size = 1 + 2*count

        filtered = []
    
        padded_data = common_lib.padded_data(self.current, window_size)
        
        for i in range(self.n):
            window = padded_data[i : i + window_size]
            median = sorted(window)[window_size // 2]
            filtered.append(median)

        return filtered

    ##########################################

    def restore_spikes(self, spikes, vec):
        """
        Restore spike values into a modified signal vector.

        Parameters
        ----------
        spikes : list of [int, float]
            List of spikes with [index, value].
        vec : list
            Vector to restore the spike values into.

        Returns
        -------
        vec : list
            Updated vector with spikes restored.
        """

        for spike in spikes:
            vec[spike[0]] = spike[1]

        return vec

    ##########################################

    def detect_stalls(self):
        """
        Detect regions where the signal has very low variance (stalls).

        Returns
        -------
        stalls : list of (int, int)
            Each stall is represented by (start index, end index).
        """

        window_ratio     = 0.03
        threshold_ratio  = 0.002
        min_stall_length = 10

        stalls           = []
        moving_std       = []
        in_stall         = False
        start            = 0
    
        window_size = max(int(self.n * window_ratio), min_stall_length)
    
        variance    = common_lib.variance(self.current, self.n)
        global_std  = common_lib.std_dev(variance)
        
        if global_std == 0:
            stalls = [(0, n-1)]
        
        else:
            threshold = global_std * threshold_ratio

            for i in range(self.n - window_size + 1):
                var = common_lib.variance(self.current[i:i+window_size], len(self.current[i:i+window_size]))
                std = common_lib.std_dev(var)
                moving_std.append(std)
                
            
            stall_flags = moving_std < threshold
    
            for i, flag in enumerate(stall_flags):
                if flag and not in_stall:
                    in_stall = True
                    start = i
                elif not flag and in_stall:
                    end = i + window_size - 1
                    if (end - start) >= min_stall_length:
                        stalls.append((start, min(end, self.n-1)))
                    in_stall = False
    
        if in_stall:
            end = self.n - 1
            if (end - start) >= min_stall_length:
                stalls.append((start, end))

        return stalls

    ##########################################



    

