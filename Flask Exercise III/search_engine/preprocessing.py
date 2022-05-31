from cv2 import cv2
from search_engine.hand_crafted_features import hand_crafted_features
#from ae import auto_encoder
import numpy as np
import glob,os
import sys
import csv

def get_images_paths(image_directory: str, file_extensions):
 
    extensions_list = []
    for i in file_extensions:
        extensions_list.extend(glob.glob(image_directory.replace('/', os.sep) + '/*' + i))   
    return extensions_list
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
    pass

def create_feature_list(image_paths):
    result=[]
    feature_extractor = hand_crafted_features()
    for element in image_paths:
        image = cv2.imread(element, cv2.IMREAD_GRAYSCALE)
        features = feature_extractor.extract(image)
        result.append(features)
        #print(features)
    return result

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
    pass


def write_to_file(feature_list, image_paths, output_path):
    # f = open(output_path + 'results.csv', "w")
    f = open(output_path + '.csv', "w",newline='')
    with f:
        writer = csv.writer(f)
        j=0
        #print(feature_list)
        #print(feature_list[0])
        for i in feature_list:
            writer.writerow([str(image_paths[j])] + [str(x) for x in i])
            j = j+1
            # if j>100:
            #     break
    f.close()
        

    
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
        - 
        - Iterate over all features (image wise)
        - Create a string with all features concerning one image seperated by ","
        - Write the image paths and features in one line in the file [format: image_path,feature_1,feature_2, ..., feature_n]
        - Close file eventually
        - Information about files http://www.tutorialspoint.com/python/file_write.htm 
    """
    pass


def preprocessing_main(image_directory, output_path, file_extensions = (".png", ".jpg")):
    """
    Function which calls 'get_images_paths', 'create_feature_list' and 'write_to_file'
    """

    image_paths = get_images_paths(image_directory, file_extensions)

    feature_list  = create_feature_list(image_paths)

    write_to_file(feature_list, image_paths, output_path)
    print(output_path)


if __name__ == '__main__':
    #x = get_images_paths('ImageCLEFmed2007_test/', ['.png'])
    #print(x)
    preprocessing_main(image_directory = "website/static/images/", output_path="search_engine/output/out")
    # preprocessing_main(image_directory = "static/images/database/", output_path="static/")