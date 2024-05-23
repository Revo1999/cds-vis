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
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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

    '''
    Creates and parses command-line arguments to get the name of the image that will be compared to the rest of the dataset.
    '''

    parser = argparse.ArgumentParser()
   
    parser.add_argument(
            "-I",
            "--Image_name",
            default="image_0321.jpg",
            help="Name of the image to compare to the rest of the dataset")
        
    return parser.parse_args()

def main():
    directory = os.path.join('..',
                                'in',)

    data = os.listdir(directory)
    # Comparisson metric
    metric = cv2.HISTCMP_CHISQR

    top_value_list = []

    save_tables_location = os.path.join('..',
                                        'out')

    # Gets chosen image from from args
    chosen_image_name = argument_collection().Image_name
    
    # Applies comparer function
    results = comparer(chosen_image=chosen_image_name, chosen_file_type=".jpg", directory=directory, data=data, metric=metric)

    # Appends chosen image to results with a distance value of 0
    results.append( (argument_collection().Image_name, 0) )

    # Sorts the list by distance, bringing chosen image first
    df2 = pd.DataFrame(results, columns = ['Filename', 'Distance']).sort_values(by=['Distance'])

    # Saves CSV
    df2.to_csv(f"{save_tables_location}/compare_hist_{chosen_image_name}_results.csv", index=False)

    # Plotting images
    f, axarr = plt.subplots(1, 6, figsize=(15, 6))
    f.subplots_adjust(wspace=2)

    # Plots chosen image
    axarr[0].imshow(mpimg.imread(os.path.join(directory, chosen_image_name)))
    axarr[0].axis('off')
    axarr[0].set_title(f'Chosen image: {chosen_image_name}', fontsize=7)

    # Plots the other images
    for i in range(1,6):
        axarr[i].imshow(mpimg.imread(os.path.join(directory, df2.iloc[i]['Filename'])))
        axarr[i].axis('off')
        axarr[i].set_title(f'Image: {df2.iloc[i]["Filename"]} \nDistance: {df2.iloc[i]["Distance"]:.2f}', fontsize=7)

    # Saves plot
    plt.savefig(os.path.join(save_tables_location, "compare_hist.png"), bbox_inches='tight', dpi=400)

    print('Done! Table created.')

if __name__ == "__main__":
    main()

