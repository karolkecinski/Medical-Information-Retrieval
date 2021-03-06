#from ast import pattern
import csv
import os
from pathlib import Path
import string

def csv_to_dict(file_path):
    """
    Function to read in a csv file and create a dict based on the first two columns.

    Parameters
    ----------
    - file_path : string
        The filepath to the CSV file.
    
    Returns
    -------
    - csv_dict : dict
        The dict created from the CSV file.

    Tipps
    -------
    - Read in the CSV file from the path
    - For each row, add an entry to a dict (first column is key, second column is value)
    - Return the dict
    """
    
    csv_dict = {}

    with open(file_path) as file:
        data = csv.reader(file, delimiter = ';')
        for row in data:
            if any(x.strip() for x in row):
                #print(row)
                csv_dict.update({row[0]: row[1]})

    return csv_dict
    
    
class IRMA:
    """
    Class to retrieve the IRMA code and information for a given file.
    """
    labels_long = ["Technical code for imaging modality", "Directional code for imaging orientation", "Anatomical code for body region examined", "Biological code for system examined"]
    labels_short = ["Imaging modality", "Imaging orientation", "Body region", "System"]

    def __init__(self, dir_path= "irma_data" + os.sep):
        """
        Constructor of an IRMA element.

        Parameters
        ----------
        - dir_path : string
            The path where the irma data is. There should be a "A.csv", "B.csv", "C.csv", "D.csv" and "image_codes.csv" file in the directory.

        Tipps
        -------
        - Create a dict for part A, B, C, and D of the IRMA code (user csv_to_dict(file_path))
        - Save the dicts (list) as class variable
        - Save "image_codes.csv" as dict in a class variable
        """
        
        self.irma_data = dir_path

        A = csv_to_dict(dir_path + "A.csv")
        B = csv_to_dict(dir_path + "B.csv")
        C = csv_to_dict(dir_path + "C.csv")
        D = csv_to_dict(dir_path + "D.csv")

        dict_list       = [A, B, C, D]
        self.IRMA_codes = dict_list
        self.image_dict = csv_to_dict(dir_path + "image_codes.csv")


    def get_irma(self, image_names):
        """
        Function to retrieve irma codes for given image names.

        Parameters
        ----------
        - image_names : list
            List of image names.

        Returns
        -------
        - irma codes : list
            Retrieved irma code for each image in 'image_list'

        Tipps
        -------
        - Remove file extension and path from all names in image_names. Names should be in format like first column of 'image_codes.csv'
        - Use self.image_dict to convert names to codes. ('None' if no associated code can be found)
        - Return the list of codes
        """
        irma_codes = []

        for imageName in image_names:
            basename    = os.path.basename(imageName)
            noExtension = Path(basename).stem
            irma_code   = self.image_dict.get(noExtension)
            irma_codes.append(irma_code)

        return irma_codes

    def decode_as_dict(self, code: string):
        """
        Function to decode an irma code to a dict.

        Parameters
        ----------
        - code : str
            String to decode.

        Returns
        -------
        - decoded : dict

        Tipps
        -------
        - Make use of 'labels_short'
        - Possible solution: {'Imaging modality': ['x-ray', 'plain radiography', 'analog', 'overview image'], ...}
        - Solution can look different
        """

        decoded = {}
        
        separated = code.split("-")
        for i in range(4): # for each feature X in A-B-C-D
            labels_list = []
            for j in range(len(separated[i])):
                str = separated[i][:j+1]
                feature = self.IRMA_codes[i].get(str)
                labels_list.append(feature)
                if separated[i][j] == '0':
                    break
            decoded.update({self.labels_short[i]: labels_list})

        return decoded

    def decode_as_str(self, code):
        """
        Function to decode an irma code to a str.

        Parameters
        ----------
        - code : str
            String to decode.

        Returns
        -------
        - decoded : str
            List of decoded strings.

        Tipps
        -------
        - Make use of 'decode_as_dict'
        - Possible solution: ['Imaging modality: x-ray, plain radiography, analog, overview image', 'Imaging orientation: coronal, anteroposterior (AP, coronal), supine', 'Body region: abdomen, unspecified', 'System: uropoietic system, unspecified']
        - Solution can look different -> FLASK will use this representation to visualize the information on the webpage.
        """
        decoded = []
        
        separated = code.split("-")
        for i in range(4):
            labels_list = []
            for j in range(len(separated[i])):
                str = separated[i][:j+1]
                feature = self.IRMA_codes[i].get(str)
                labels_list.append(feature)
                if separated[i][j] == '0':
                    break
            labels = ''
            labels = ', '.join(labels_list)
            decoded.append(f'{self.labels_short[i]}: {labels}')

        return decoded
        

if __name__ == '__main__':
    image_names = ["1880.png"]

    irma = IRMA()

    codes = irma.get_irma(image_names)
    print("Codes: ", codes)

    if codes is not None:
        code = codes[0]
        print("Dict: \n{}\n\n".format(irma.decode_as_dict(code)))
        print("String: \n{}\n\n".format(irma.decode_as_str(code)))

    '''
    Result could look like this:


    Codes:  ['1121-127-700-500']
    Dict:
    {'Imaging modality': ['x-ray', 'plain radiography', 'analog', 'overview image'], 'Imaging orientation': ['coronal', 'anteroposterior (AP, coronal)', 'supine'], 'Body region': ['abdomen', 'unspecified'], 'System': ['uropoietic system', 'unspecified']}


    String:
    ['Imaging modality: x-ray, plain radiography, analog, overview image', 'Imaging orientation: coronal, anteroposterior (AP, coronal), supine', 'Body region: abdomen, unspecified', 'System: uropoietic system, unspecified']
    '''