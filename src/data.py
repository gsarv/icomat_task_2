"""
data.py
=======

This module defines the `data` class, which manages multiple signal vectors
from raw data (e.g., CSV input). It builds `vector` objects and computes
basic metadata such as the number of vectors and time step.

Dependencies
------------
- vector
"""

from vector import vector

class data:
    """
    Class to manage and organize raw multi-dimensional data into vector objects.

    Parameters
    ----------
    data : list of list of str
        Raw data as read from a CSV file. Each sublist represents a row; 
        the first row may contain headers.

    Attributes
    ----------
    raw_data : list of list of str
        Original raw data.
    n_vectors : int
        Number of vectors (columns) in the data.
    vectors : list of vector
        List of `vector` objects created from the raw data columns.
    time_step : float
        Estimated time step, calculated as the difference between the first two 
        numerical entries in the first vector.
    """
    def __init__(self, data):
        
        self.raw_data   = data                       # Data as read by csv file
        self.n_vectors  = self.number_vectors()      # Number of vectors
        self.vectors    = self.create_data_vectors() # List with objects vectors
        self.time_step  = self.vectors[0].original_data[1] - self.vectors[0].original_data[0]
    ##########################################

    def create_data_vectors(self):
        """
        Convert raw column data into a list of `vector` objects.

        Returns
        -------
        vectors : list of vector
            Each vector corresponds to a column of data from the raw data.
        """

        vectors = []
        
        for i in range(self.n_vectors):
            vectors.append([])
            
        for i,line in enumerate(self.raw_data):
            for j in range(self.n_vectors):
                if (i==0):
                    vectors[j].append(self.raw_data[i][j])
                else:
                    vectors[j].append(float(self.raw_data[i][j]))
                    
        for i, vec in enumerate(vectors):
            vectors[i] = vector(vec)

        return vectors

    ##########################################

    def number_vectors(self):
        """
        Determine the number of vectors (columns) in the raw data.

        Returns
        -------
        n : int
            Number of vectors.
        """

        n = len(self.raw_data[0])
        
        return n

    ##########################################





