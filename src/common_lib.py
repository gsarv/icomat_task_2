"""
common_lib.py
=============

A small utility library providing common operations for signal processing,
data loading, and plotting.

This library includes:
- Loading CSV files into lists
- Padding signal data for windowed operations
- Plotting (x, y) data with matplotlib
- Basic statistical functions: mean, variance, standard deviation

Dependencies:
-------------
- os
- numpy
- matplotlib

"""

import os
import numpy
import matplotlib.pyplot as plt

##########################################

def load_csv(filename):
    """
    Load data from a CSV file into a list of lists.

    Each line in the file becomes a list of string values.

    Parameters
    ----------
    filename : str
        Path to the CSV file.

    Returns
    -------
    signals : list of list of str
        The loaded data, where each inner list represents a row.

    Raises
    ------
    AssertionError
        If the file does not exist.
    """
    
    signals = []

    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf-8') as f:
        
            for line in f:
 
                line = line.strip()
            
                if line:
                    values = line.split(',')
                    signals.append(values)
                else:
                    continue
    else:
        assert False, "File {} does not exist".format(filename)
            
    return signals

##########################################

def padded_data(data, window_size):
    """
    Pad signal data on both sides by repeating edge values.

    Useful for sliding window computations that need padding.

    Parameters
    ----------
    data : list
        Original data to pad.
    window_size : int
        The size of the window (padding will be window_size//2 on each side).

    Returns
    -------
    padded : list
        The padded data.
    """
    
    padded = [data[0]] * (window_size // 2) + data + [data[-1]] * (window_size // 2)
            
    return padded

##########################################

def plot_xy(x_list, y_list, x_label, y_label, title):
    """
    Plot x vs. y data with labels and title.

    Parameters
    ----------
    x_list : list
        Data for the x-axis.
    y_list : list
        Data for the y-axis.
    x_label : str
        Label for the x-axis.
    y_label : str
        Label for the y-axis.
    title : str
        Title of the plot.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The matplotlib figure object.
    """

    fig = plt.figure(111)
    ax  = fig.add_subplot(111)
    ax.plot(x_list, y_list)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    return fig

##########################################

def mean_value(data, number_of_data):
    """
    Compute the mean (average) of data.

    Parameters
    ----------
    data : list of numbers
        The data to compute the mean for.
    number_of_data : int
        Number of data points (typically len(data)).

    Returns
    -------
    mean : float
        The mean value.
    """

    mean = sum(data) / number_of_data
        
    return mean

##########################################
    
def variance(data, number_of_data):
    """
    Compute the variance of data.

    Parameters
    ----------
    data : list of numbers
        The data to compute the variance for.
    number_of_data : int
        Number of data points (typically len(data)).

    Returns
    -------
    variance : float
        The variance.
    """
        
    s = 0
    mean = mean_value(data, number_of_data)
        
    for value in data:
        s += + (value - mean)**2
        
    variance = s / number_of_data
    
    return variance

##########################################
    
def std_dev(variance):
    """
    Compute the standard deviation given the variance.

    Parameters
    ----------
    variance : float
        The variance of the data.

    Returns
    -------
    std_dev : float
        The standard deviation.
    """

    std_dev = numpy.sqrt(variance)
        
    return std_dev

##########################################



