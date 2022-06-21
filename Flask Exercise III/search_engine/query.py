from search_engine.hand_crafted_features import hand_crafted_features
#from ae import auto_encoder
from search_engine.searcher import Searcher
import cv2
from pathlib import Path
import csv
import numpy as np
import os

INDEX = f"search_engine{os.sep}output{os.sep}out.csv"

class Query:

    def __init__(self, path_to_index = INDEX):
        """
        Init function of the Query class. Sets 'path_to_index' to the class variable 'path_to_index'. Class variables 'query_image_name' and 'results' are set to None.
        Parameters
        ----------
        path_to_index : string
            Path to the index file.
        """
        self.path_to_index = path_to_index
        self.query_image_name = None
        self.results = None


    def set_image_name(self, query_image_name):
        """
        Function to set the image name if it does not match the current one. Afterwards the image is loaded and features are retrieved.
        Parameters
        ----------
        query_image_name : string
            Image name of the query. For example: 'static/images/query/test.png'
        Tasks
        ---------
            - Check if 'query_image_name' is different to 'self.query_image_name'
            - If yes:
                - Set 'self.results' to None
                - Overwrite 'query_image_name'
                - Read in the image and save it under 'self.query_image'
                - Calculate features
        """
        if(query_image_name != self.query_image_name):
            self.results = None
            self.query_image_name = query_image_name
            self.query_image = cv2.imread(query_image_name, cv2.IMREAD_GRAYSCALE)
            self.calculate_features()


    def calculate_features(self):
        """
        Function to calculate features for the query image.
        Tasks
        ---------
            - Check if "self.query_image" is None -> exit()
            - Extract features wit "FeatureExtractor" and set to "self.features"
        """
        # create extractor
        feature_extractor = hand_crafted_features()

        # describe the image
        self.features = feature_extractor.extract(self.query_image)

 
    def run(self, limit = 10):
        """
        Function to start a query if results have not been computed before.
        Parameters
        ----------
        limit : int
            Amount of results that will be retrieved. Default: 10.
        Returns
        -------
        - results : list
            List with the 'limit' first elements of the 'results' list. 

        Tasks
        ---------
            - Check if 'self.results' is None
            - If yes:
                - Create a searcher and search with features
                - Set the results to 'self.results'
            - Return the 'limit' first elements of the 'results' list.
        """
        if(self.results == None):
            sr = Searcher(self.path_to_index)
            results = sr.search(self.features)
            self.results = results
            return results[:limit]

        return self.results[:limit]

    def relevance_feedback(self, selected_images, not_selected_images, limit = 10) -> list:
        """
        Function to start a relevance feedback query.
        Parameters
        ----------
        selected_images : list
            List of selected images.
        not_selected_images : list
            List of not selected images.
        limit : int
            Amount of results that will be retrieved. Default: 10.
        Returns
        -------
        - results : list
            List with the 'limit' first elements of the 'results' list. 
        """

        if(self.results == None):
            sr = Searcher(self.path_to_index)
            relevant          = self.get_feature_vector(selected_images)
            non_relevant      = self.get_feature_vector(not_selected_images)
            modified_features = rocchio(self.features, relevant, non_relevant)
            results           = sr.search(modified_features) 
            self.results      = results
            return results[:limit]

    def get_feature_vector(self, image_names) -> list:
        """
        Function to get features from 'index' file for given image names.
        Parameters
        ----------
        image_names : list
            List of images names.
        Returns
        -------
        - features : list
            List with of features.
        """
        features = []

        with open(self.path_to_index) as file:
            data = csv.reader(file)
            list_of_features = {row[0] : row[1:] for row in data}

            for image in image_names:
                features.append(list_of_features.get(image))

            return features
    
def rocchio(original_query, relevant, non_relevant, a = 1, b = 0.8, c = 0.1) -> list:
    """
    Function to adapt features with rocchio approach.

    Parameters
    ----------
    original_query : list
        Features of the original query.
    relevant : list
        Features of the relevant images.
    non_relevant : list
        Features of the non relevant images.
    a : int
        Rocchio parameter.
    b : int
        Rocchio parameter.
    c : int
        Rocchio parameter.
    Returns
    -------
    - features : list
        List with of features.
    """

    modified_query =  a * original_query
    modified_query += b * 1 / len(relevant)     * np.sum(relevant, axis = 0)
    modified_query -= c * 1 / len(non_relevant) * np.sum(non_relevant, axis = 0)

    return modified_query


if __name__ == "__main__":
    query = Query(path_to_index= "search_engine/output/out.csv")
    query.set_image_name(query_image_name="website/static/ImageCLEFmed2007_test/3145.png")
    query_result = query.run()
    print(query_result[0][0].split(f"{os.sep}"))
    print("Retrieved images: ", query_result)
    