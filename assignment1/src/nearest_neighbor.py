'''
Assignment 1
    Victor Rasmussen
        Visual Analytics, Aarhus University
            17-05-2024
'''

#Dependencies
from tensorflow.keras.preprocessing.image import (load_img, 
                                                  img_to_array)
from tensorflow.keras.applications.vgg16 import (VGG16, 
                                                 preprocess_input)
from sklearn.neighbors import NearestNeighbors
import numpy as np
from numpy.linalg import norm
import os
from tqdm import tqdm
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd

def argument_collection():
    parser = argparse.ArgumentParser()
   
    parser.add_argument(
            "-I",
            "--Image_name",
            default="image_0321.jpg",
            help="Name of the image to compare to the rest of the dataset")
        
    return parser.parse_args()


def model_load():
    print("Loading model")

    model = VGG16(weights='imagenet', 
                include_top=False,
                pooling='avg',
                input_shape=(224, 224, 3))

    print("Model loaded")
    return model


def load_neighbor(feature_list):
    neighbors = NearestNeighbors(n_neighbors=6, 
                                algorithm='brute',
                                metric='cosine').fit(feature_list)

    return neighbors


def extract_features(img_path, model):
   
    """
    Extract features from image data using a model
    """
    
    # Define input image shape - remember we need to reshape
    input_shape = (224, 224, 3)

    # load image from file path
    img = load_img(img_path, target_size=(input_shape[0], 
                                          input_shape[1]))

    # convert to array
    img_array = img_to_array(img)

    # expand to fit dimensions
    expanded_img_array = np.expand_dims(img_array, axis=0)

    # preprocess image - see last week's notebook
    preprocessed_img = preprocess_input(expanded_img_array)

    # use the predict function to create feature representation
    features = model.predict(preprocessed_img, verbose=False)

    # flatten
    flattened_features = features.flatten()
    
    # normalise features
    normalized_features = flattened_features / norm(features)
    return flattened_features

def get_target_idx(filenames, target_image):

    target_idx = None
    idx = 0
    for files in filenames:
        if files == target_image:
            target_idx = idx
        idx += 1

    return target_idx


def apply_neighbor(filenames, target_image):
        model = model_load()

        target_idx = get_target_idx(filenames, target_image)

        feature_list = []

        # iterate over all files with a progress bar
        for i in tqdm(range(len(filenames)), colour="green"):
            feature_list.append(extract_features(filenames[i], model))

        neighbors = load_neighbor(feature_list=feature_list)

        distances, indices = neighbors.kneighbors([feature_list[target_idx]])

        idxs = []
        distance_list = []

        for i in range(1,6):
            idxs.append(indices[0][i])
            distance_list.append(distances[0][i])

        return distance_list, idxs, target_idx

def get_filenames():
    # path to folder with images
    root_dir = os.path.join("..", "data")

    filenames = [root_dir + "/" + name for name in sorted(os.listdir(root_dir)) if name.endswith(".jpg")]

    return filenames


def main():
    target_image = os.path.join("..", "data", argument_collection().Image_name)

    filenames = get_filenames()

    distance_list, idxs, target_idx = apply_neighbor(filenames=filenames, target_image=target_image)

    # plot target image & 5 most similar
    f, axarr = plt.subplots(1,6, figsize=(15, 6))
    f.subplots_adjust(wspace=2)

    axarr[0].imshow(mpimg.imread(filenames[target_idx]))
    axarr[0].axis('off')
    axarr[0].set_title(f'Chosen image: {filenames[target_idx].split("/")[2]}', fontsize = 7)
    df_to_export = []
    df_to_export.append( (filenames[target_idx].split("/")[2], 0) )


    for i in range(1,6):
        axarr[i].imshow(mpimg.imread(filenames[idxs[i-1]]))
        axarr[i].axis('off')
        axarr[i].set_title(f'Image: {filenames[idxs[i-1]].split("/")[2]} \nDistance: {"%.2f" % distance_list[i-1]}', fontsize = 7)
        df_to_export.append( (filenames[idxs[i-1]].split("/")[2], distance_list[i-1]) )

    plt.savefig("../out/nearest_neighbor.png", bbox_inches='tight', dpi=400)

    df = pd.DataFrame(df_to_export, columns = ['Filename', 'Distance'])
    df.to_csv(f"../out/nearest_neighbor_{argument_collection().Image_name}_results.csv", index=False)

if __name__ == "__main__":
    main()