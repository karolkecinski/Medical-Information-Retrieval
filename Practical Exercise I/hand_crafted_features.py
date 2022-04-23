import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt
 
class hand_crafted_features:
    """
    Class to extract features from a given image.

    Example
    --------
    feature\_extractor = hand_crafted_features()
    features = feature_extractor.extract(example_image)
    print("Features: ", features)
    """

    def extract(self, image):
        """
        Function to extract features for an image.
        Parameters
        ----------
        - image : (x,y) array_like
            Input image.

        Returns
        -------
        - features : list
            The calculated features for the image.

        Examples
        --------
        >>> fe.extract(image)
        [126, 157, 181, 203, 213, 186, 168, 140, 138, 155, 177, 176]
        """
        # TODO: You can change your extraction method here:
        #features = self.thumbnail_features(image)
        features= self.histogram(image)
        #features=self.partitionbased_histograms(image)
        #features=self.extract_features_spatial(image)
        # TODO: You can even extend features with another method:
        #features.extend(self.thumbnail_features(image))

        return features
    
    def histogram(self, image):

        hist = cv2.calcHist([image],[0],None,[256],[0,256])
        #plt.hist(image.ravel(),256,[0,256])
        #plt.title('Histogram for gray scale picture')
        #plt.show()

        features=hist.tolist()
       # feature_list = list(np.concatenate(feature_list).flat)
        # flatten the list of lists
        features = [item for sublist in features for item in sublist]
        return features
        """
        Function to extract histogram features for an image.
        Parameters
        ----------
        - image : (x,y) array_like
            Input image.
        
        Returns
        -------
        - features : list
            The calculated features for the image.

        Tipps
        -----
            - Use 'cv2.calcHist'
            - Create a list out of the histogram (hist.tolist())
            - Return a list (flatten)
        """
        pass


    def thumbnail_features(self, image):
        """
        Function to create a thumbnail of an image and return the image values (features).
        Parameters
        """
        #image=cv2.imread("image")
        #image=cv2.imread("1880.png")
        width=30
        height=30
        dim=(width,height)
        resized_img=cv2.resize(image,dim,interpolation=cv2.INTER_AREA)
        # cast image to list of lists
        features =  resized_img.tolist()
        # flatten the list of lists
        features = [item for sublist in features for item in sublist]

        # _2d_list=list(resized_img)

        # #_2d_list=np.asarray(resized_img)
    
        # feature_list = list(np.concatenate(_2d_list).flat)

        return features

        """
        - image : (x,y) array_like
            Input image.
        
        Returns
        -------
        - features : list
            The calculated features for the image.

        Tipps
        -----
            - Resize image (dim(30,30))
            - Create a list from the image (np array)
            - Return a list (flatten)
        """
        pass


    def partitionbased_histograms(self, image, factor = 10):

        # width=200
        # height=200
        # dim=(width,height)
        resized = cv2.resize(image, (200,200))
        #img=cv2.resize(image,dim,interpolation=cv2.INTER_AREA)
        hist_list=[]
        #tiles = [img[x:x+factor,y:y+factor] for x in range(0,img.shape[0],factor) for y in range(0,img.shape[1],factor)]
        M = resized.shape[0]//(200//factor)
        N = resized.shape[1]//(200//factor)

        for r in range(0,resized.shape[0], M):
            for c in range(0,resized.shape[1], N):
                #window = img[r:r+M,c:c+N]
                c1 = r + M
                r1 = c + N
                tiles = resized[r:r+M,c:c+N]
                hist_list.extend(self.histogram(tiles))
        

        return hist_list

            
        """
        Function to create partition based histograms.
        Parameters
        ----------
        - image : (x,y) array_like
            Input image.
        - factor : int
            Partitioning factor.
        
        Returns
        -------
        - features : list
            The calculated features for the image.

        Tipps
        -----
            - Resize image (dim(200, 200))
            - Observe (factor * factor) image parts
            - Calculate a histogramm for each part and add to feature list
        """
        pass


    def extract_features_spatial(self, image, factor = 10):

        # width=20
        # height=20
        # dim=(width,height)
        #resized_img=cv2.resize(image,dim,interpolation=cv2.INTER_AREA)


        resized = cv2.resize(image, (200,200))
        #img=cv2.resize(image,dim,interpolation=cv2.INTER_AREA)
        features=[]
        tiles_list=[]
        #tiles = [img[x:x+factor,y:y+factor] for x in range(0,img.shape[0],factor) for y in range(0,img.shape[1],factor)]
        M = resized.shape[0]//(200//factor)
        N = resized.shape[1]//(200//factor)

        for r in range(0,resized.shape[0], M):
            for c in range(0,resized.shape[1], N):
                #window = img[r:r+M,c:c+N]
                c1 = r + M
                r1 = c + N
                tiles = resized[r:r+M,c:c+N]
                tiles_list.extend(tiles)

        for element in tiles_list:
            features.append(np.max(element))
            features.append(np.min(element))
            features.append(np.mean(element))

        # for element in tiles:
        #     features.append(np.max(element))
        #     features.append(np.min(element))
        #     features.append(np.mean(element))
        
        return features
        """
        Function to extract spatial features.
        Parameters
        ----------
        - image : (x,y) array_like
            Input image.
        - factor : int
            Partitioning factor.
        
        Returns
        -------
        - features : list
            The calculated features for the image.

        Tipps
        -----
            - Resize image (dim(200, 200))
            - Observe (factor * factor) image parts
            - Calculate max, min and mean for each part and add to feature list
        """

        #max(list)
        #min(list)
        #mean(list)
        pass


    def image_pixels(self, image):
        """
        Function to return the image pixels as features.
        Example of a bad implementation. The use of pixels as features is highly inefficient!

        Parameters
        ----------
        - image : (x,y) array_like
            Input image.
        
        Returns
        -------
        - features : list
            The calculated features for the image.
        """
        # cast image to list of lists
        features =  image.tolist()
        # flatten the list of lists
        features = [item for sublist in features for item in sublist]
        # return 
        return features

if __name__ == '__main__':
    # Read the test image
    # TODO: You can change the image path here:
    example_image = cv2.imread('3145.png', cv2.IMREAD_GRAYSCALE)

    # Assert image read was successful
    #assert example_image is not None

    # create extractor
    feature_extractor = hand_crafted_features()

    # describe the image
    features = feature_extractor.extract(example_image)

    # print the features
    print("Features: ", features)
    print("Length: ", len(features))
