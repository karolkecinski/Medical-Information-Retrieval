# import the necessary packages
import csv
import math
import numpy as np
from numpy.core import sqrt, add
from pathlib import Path
from numpy.linalg import norm
import scipy.spatial #import distance
from scipy import spatial
#import pandas as pd
from decimal import Decimal
#from numpy import dot
from numpy.linalg import norm



def square_rooted(x):

    
    return round(sqrt(sum([float(a)*float(a) for a in x])),3)
    #return np.sqrt(np.sum(x)**2)
    """
    Function to calculate the root of the sum of all squared elements of a vector (iterable).
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    Returns
    -------
    square rooted : float
        Root of the sum of all squared elements of 'x'.
        
    """

def euclidean_distance(x, y):
    """
    Function to calculate the euclidean distance for two lists 'x' and 'y'.
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    y : (N,) array_like
        Input array.
    Returns
    -------
    euclidean distance : float
        The euclidean distance between vectors `x` and `y`.
    Help
    -------
    https://pythonprogramming.net/euclidean-distance-machine-learning-tutorial/
    
    """

    edistance = []
    if len(x) < len(y): 
        smaller = len(x) 
    else:
        smaller = len(y)
    for i in range(smaller):
            edistance.append(float(x[i])-float(y[i]))

   
    return square_rooted(edistance)



def manhattan_distance(self, x, y):

    return sum(abs(float(a)-float(b)) for a,b in zip(x,y))
    """
    Function to calculate the manhattan distance for two lists 'x' and 'y'.
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    y : (N,) array_like
        Input array.
    Returns
    -------
    manhattan distance : float
        The manhattan distance between vectors `x` and `y`.
    """

 
def nth_root(value, n_root):
 
    root_value = 1/float(n_root)
    return round (Decimal(value) ** Decimal(root_value),3)

def minkowski_distance(self, x, y, p):

    return nth_root(sum(pow(abs(float(a)-float(b)),p) for a,b in zip(x, y)),p)
    """
    Function to calculate the minkowski distance for two lists 'x' and 'y'.
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    y : (N,) array_like
        Input array.
    p : int
        P-value.
    Returns
    -------
    minkowski distance : float
        The minkowski distance between vectors `x` and `y`.
    """
    pass

def cosine_similarity(self, x, y):

    numerator = sum(float(a)*float(b) for a,b in zip(x,y))
    denominator = square_rooted(x)*square_rooted(y)
    return round(numerator/float(denominator),3)
    """
    Function to calculate the cosine similarity for two lists 'x' and 'y'.
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    y : (N,) array_like
        Input array.
    Returns
    -------
    cosine similarity : float
        The cosine similarity between vectors `x` and `y`.
    Help
    -------
        - Compute numerator
        - Compute denominator with the help of "square_rooted"
        - Calculate similarity
        - Change range to [0,1] rather than [-1,1]
    """

def dot(A,B): 
    return (sum(float(a)*float(b) for a,b in zip(A,B)))

def cosine_distance(self, x, y):
    return dot(x,y) / ( (dot(x,x) **.5) * (dot(y,y) ** .5) )

    """
    Function to calculate the cosine distance for two lists 'x' and 'y'.
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    y : (N,) array_like
        Input array.
    Returns
    -------
    cosine distance : float
        The cosine distance between vectors `x` and `y`.
    Help
    -------
        - Convert 'cosine similarity' to distance.
    """
    pass

class Searcher:

    def __init__(self, path_to_index):
        self.path_to_index=path_to_index

        """
        Init function of the Searcher class. Sets 'path_to_index' to the class variable 'path_to_index'.
        Parameters
        ----------
        x : string
            Path to the index file.
        """
        pass

        
        
    def search(self, query_features):
        if Path(self.path_to_index).exists() == False:
            print('Incorrect or not defined Path')
            return ("error")
        else:
            dic=dict()
            distance=0.0
            f = open(self.path_to_index) #"r")
            with f:
                 reader=csv.reader(f)
                 for row in reader:
                     key=row.pop(0)
                     distance =euclidean_distance(row,query_features)
                     dic[key]= distance
            f.close()
            sortedDict = sorted(dic.items(), key=lambda x: x[1])

            
            return sortedDict

        """
        Function retrieve similar images based on the queryFeatures
        Parameters
        ----------
        query_features : list
            List of features.
        Returns
        -------
        results : list
            List with the retrieved results (tuple). Tuple: First element is name and the second the distance of the image.
        Task
        -------
            - If there is no index file -> Print error and return False [Hint: Path(*String*).exists()]
            - Open the index file
            - Read in CSV file [Hint: csv.reader()]
            - Iterate over every row of the CSV file
                - Collect the features and cast to float
                - Calculate distance between query_features and current features list
                - Save the result in a dictionary: key = image_path, Item = distance
            - Close file
            - Sort the results according their distance
            - Return limited results
        """
        pass
