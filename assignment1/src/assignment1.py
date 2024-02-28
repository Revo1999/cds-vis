#/work/VictorRasmussen#3454/cds.vis/cds-vis/assignment1/data/image_0321.jpg

# Går billeder igennem på en effektiv måde

# Aben billede
    # Extract histogram 
        # Compare
            # Save Score
             #Check om den er indenfor for de 5 højeste


#Dependencies

import cv2
import numpy as np
import pandas as pd
import os
from tqdm import tqdm

def is_image_chosen (image_file): #Return true if file is not chosen
    return image_file != chosen_image



def create_hist(picture_file):
    image_hist = cv2.calcHist([picture_file], [0,1,2], None, [256,256,256], [0,256, 0,256, 0,256]) #Syntax: cv2.calcHist(image(s), channels, mask, histSize, ranges[])
    # Normalizing values
    # Every pixel value we subtract the min pixel value in the image, then divide that by the max minus the min (source: https://github.com/CDS-AU-DK/cds-visual/blob/main/nbs/session3_inclass_rdkm.ipynb)
    cv2.normalize(image_hist, image_hist, 0, 1.0, cv2.NORM_MINMAX) #Syntax: normalize(source file, destination file, alpha, beta, normalization_type)
    return image_hist



def compare_histograms(chosen_image_hist, image_to_compare, metric):
    return round(cv2.compareHist(chosen_image_hist, create_hist(image_to_compare), metric), 1)



def update_top_values(dictionary_name, filename, new_value):
    
    # add new dictionary pair with file name and distance value
    dictionary_name.update({'filename':filename, 'value':new_value })

    #If the list is longer than 5 sort the list and only keep the 5 highest values(to avoid keeping track of all values)

    if len(dictionary_name) > 5:

        #This might be a little chaotic... it sorts based on the second value of the dictionary pair, this would normally be done with a getter function, lambda creates simpler syntax
        #For a detailed description check: https://realpython.com/sort-python-dictionary/#using-the-key-parameter-and-lambda-functions 

        dictionary_name = dict(sorted(dictionary_name.items(), key=lambda item: item[1], reverse=True)[:5])









chosen_image = 'image_0321.jpg'

directory = os.path.join('..',
                             'data',)

data = os.listdir(directory)

metric = cv2.HISTCMP_CHISQR

top_value_dict = {}

#Creates histogram of chosen image
chosen_image_hist = create_hist(cv2.imread(os.path.join(directory, chosen_image)))


save_tables_location = os.path.join('..',
                                'out')

# Goes trough image file directory

for picture_file in tqdm(data, colour='green'):
    if is_image_chosen(picture_file): #Continues if the file is not the chosen image

        # Load image   
        picture_to_proces = cv2.imread(os.path.join(directory, picture_file))

        print(type(picture_to_proces), 'picture to proces')
        print(compare_histograms(image_to_compare = picture_to_proces, metric=metric, chosen_image_hist=chosen_image_hist), 'compare histograms')


        #def update_top_values(dictionary_name, filename, new_value):

        update_top_values(top_value_dict, picture_to_proces, compare_histograms(image_to_compare = picture_to_proces, metric=metric, chosen_image_hist=chosen_image_hist))
     
#create and export dataframe

write_row = pd.DataFrame({'Filename': [top_value_dict[0]], 'Value':[top_value_dict[1]]})
            
df = pd.concat([df, write_row], ignore_index=True)

df.to_csv(f"{save_tables_location}/{folder}_table.csv", index=False)