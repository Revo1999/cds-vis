'''
Assignment 1
    Victor Rasmussen
        Visual Analytics, Aarhus University
            17-05-2024
'''

#The chosen image is ../data/image_0321.jpg

#Dependencies
import cv2
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
import argparse

def is_image_chosen (image_file, chosen_image): #Return true if file is not chosen
    return image_file != chosen_image


def create_hist(picture_file):
        image_hist = cv2.calcHist([picture_file], [0,1,2], None, [256,256,256], [0,256, 0,256, 0,256]) #Syntax: cv2.calcHist(image(s), channels, mask, histSize, ranges[])
        # Normalizing values
        # Every pixel value we subtract the min pixel value in the image, then divide that by the max minus the min (source: https://github.com/CDS-AU-DK/cds-visual/blob/main/nbs/session3_inclass_rdkm.ipynb)
        cv2.normalize(image_hist, image_hist, 0, 1.0, cv2.NORM_MINMAX) #Syntax: normalize(source file, destination file, alpha, beta, normalization_type)
        return image_hist

def compare_histograms(chosen_image_hist, image_to_compare, metric):
    return round(cv2.compareHist(chosen_image_hist, create_hist(image_to_compare), metric), 1)


def add_top_values(list_name, filename, new_value):
    
    list_name.append( (filename, new_value) )

def comparer(chosen_image, chosen_file_type, directory, data, metric):

    top_value_list = []

    #Creates histogram of chosen image
    chosen_image_hist_normalized = create_hist(cv2.imread(os.path.join(directory, chosen_image)))

    progressbar = tqdm(data, desc='Pictures', colour='green')

    # Goes trough image file directory

    for picture_file in data:
        
        progressbar.update(1)

        if is_image_chosen(picture_file, chosen_image) and picture_file.endswith(chosen_file_type) : #Continues if the file is not the chosen image

            # Load image   
            picture_to_proces = cv2.imread(os.path.join(directory, picture_file))

            #def update_top_values(dictionary_name, filename, new_value):

            add_top_values(top_value_list, picture_file, compare_histograms(image_to_compare = picture_to_proces, metric=metric, chosen_image_hist=chosen_image_hist_normalized))

        elif picture_file != chosen_image:
            progressbar.write(f"{picture_file} is not a jpeg, therefore it's been skipped")

    progressbar.close()

    #create and export dataframe
    top_value_list = sorted(top_value_list, key=lambda x: x[1])
    top_value_list = top_value_list[:5]

    return top_value_list


def argument_collection():
    parser = argparse.ArgumentParser()
   
    parser.add_argument(
            "-I",
            "--Image_name",
            default="image_0321.jpg",
            help="Name of the image to compare to the rest of the dataset")
        
    return parser.parse_args()

def main():
    directory = os.path.join('..',
                                'data',)

    data = os.listdir(directory)

    metric = cv2.HISTCMP_CHISQR

    top_value_list = []

    save_tables_location = os.path.join('..',
                                        'out')

    chosen_image_name = argument_collection().Image_name

    results = comparer(chosen_image=chosen_image_name, chosen_file_type=".jpg", directory=directory, data=data, metric=metric)

    #column name dims
    df2 = pd.DataFrame(results, columns = ['Filename', 'Distance'])


    df2.to_csv(f"{save_tables_location}/{chosen_image_name}_results.csv", index=False)

    print('Done! Table created.')

if __name__ == "__main__":
    main()

