from venv import create
import cv2
from hand_crafted_features import hand_crafted_features
# from ae import auto_encoder
import numpy as np
import glob
import sys
import os

def get_images_paths(image_directory, file_extensions):
    """
    Function to receive every path to a file with ending "file_extension" in directory "image_directory".
    Parameters
    ----------
    image_directory : string
        Image directory. For example: 'static/images/database/'
    file_extensions : tuple
        Tuple of strings with the possible file extensions. For example: '(".png", ".jpg")'
    Returns
    -------
    - image_paths : list
        List of image paths (strings).
    Tasks
    -------
        - Iterate over every file_extension
            - Create a string pattern 
            - Use glob to retrieve all possible file paths (https://docs.python.org/3.7/library/glob.html )
            - Add the paths to a list  (extend)
        - Return result
    """
    
    # for file in image_directory:
    listOfDirectories = []

    for extension in file_extensions:
        directory = image_directory + '*' + extension
        listOfDirectories.extend(glob.glob(directory))
    #print(listOfDirectories)
    return listOfDirectories




def create_feature_list(image_paths):
    """
    Function to create features for every image in "image_paths".
    Parameters
    ----------
    image_paths : list
        Image paths. List of image paths (strings).
    Returns
    -------
    - result : list of lists.
        List of 'feature_list' for every image. Each image is summarized as list of several features.
    Tasks
    -------
        - Iterate over all image paths
        - Read in the image
        - Extract features with class "feature_extractor"
        - Add features to a list "result"
    """
    
    HCF = hand_crafted_features()
    featureLists = []
    print(image_paths)

    for path in image_paths:
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        featureLists.append(HCF.extract(image))

    return featureLists


def write_to_file(feature_list, image_paths, output_path):
    """
    Function to write features into a CSV file.
    Parameters
    ----------
    feature_list : list
        List with extracted features. Should come from 'create_feature_list':
    image_paths : list
        Image paths. List of image paths (strings). Should come from 'get_images_paths':
    output_path : string
        Path to the directory where the index file will be created.
    Tasks
    -------
        - Open file ("output_name")
        - Iterate over all features (image wise)
        - Create a string with all features concerning one image seperated by ","
        - Write the image paths and features in one line in the file [format: image_path,feature_1,feature_2, ..., feature_n]
        - Close file eventually

        - Information about files http://www.tutorialspoint.com/python/file_write.htm 
    """

    with open(output_path, 'w+') as file:

        for image_features, image_path in zip(feature_list, image_paths): 
            output = f'{image_path}'
            for feature in image_features:
                output += ',' + str(feature)
            output += '\n'
            file.write(output)
    


def preprocessing_main(image_directory, output_path, file_extensions = (".png", ".jpg")):
    """
    Function which calls 'get_images_paths', 'create_feature_list' and 'write_to_file'
    """

    image_paths = get_images_paths(image_directory, file_extensions)

    feature_list  = create_feature_list(image_paths)

    write_to_file(feature_list, image_paths, output_path)


if __name__ == '__main__':
    #x = get_images_paths('ImageCLEFmed2007_test/', ['.png'])
    #print(x)
    preprocessing_main(image_directory = "ImageCLEFmed2007_test/", output_path="output/out.txt")
    # preprocessing_main(image_directory = "static/images/database/", output_path="static/")