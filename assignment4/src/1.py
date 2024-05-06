import vrashelper as vh
import sys
import glob
import os
import polars as pl
from PIL import Image
from tqdm import tqdm as tqdm_bar #Renaming tqdm avoids an error (is used in other packages)
from facenet_pytorch import MTCNN
import torch
import re



def list_files(directory):
    folders = os.listdir(directory)

    all_files = []
    for root, dirs, files in os.walk(directory_path, topdown=True):
        for filenames in files:
            all_files.append(os.path.join(root, filenames))

    return all_files


def check_files(file_list, wanted_filetype):
    print(f"\nChecking {len(file_list)} files for filetype... \n")

    wrong_filetype = []

    for file in file_list:
            if wanted_filetype not in file:
                wrong_filetype.append(file)
    
    if len(wrong_filetype) == 0:
        print(vh.colorbank.hackergreen + "All files are the right filetype"  + vh.colorbank.default)
    elif len(wrong_filetype) > 0:
        print(vh.colorbank.warning + f"{vh.ctext.bold}These files dont comply with {wanted_filetype} filetype:{vh.ctext.default}")
        print(vh.colorbank.error_red + "\n".join(wrong_filetype) + vh.colorbank.default)
        print("\nDo you wish to disregard these?\n")
        
    input = take_input()

    if input == True:
        print (vh.ctext.remove_line *2) #Removes 2 last lines from console
        files_removed = 0
        print("\nRemoving files from processing list...")
        for wrong_files in wrong_filetype:
             file_list.remove(wrong_files)
             files_removed += 1
        print(vh.colorbank.hackergreen + f"{vh.ctext.nline}{files_removed} files removed" + vh.colorbank.default)
    elif input == False:
        print (vh.ctext.remove_line) #Removes last input line from console
        print(vh.colorbank.error_red + "exiting..." + vh.colorbank.default)
        #Exits program
        sys.exit(1)

    return file_list

def take_input():
    inp = input("[Y]/[N]\n")
    if inp.lower() == "y" or inp.lower() == "yes":
        return True
    elif inp.lower() == "n" or inp.lower() == "no":
        return False
    else:
        print (vh.ctext.remove_line) #Removes last input line from console
        print(vh.colorbank.error_red + "\nwrong input!" + vh.colorbank.default)
        take_input()



def image_loader(image_paths_to_proces):

    images = [Image.open(img_path) for img_path in tqdm_bar(image_paths_to_proces, desc="Loading images", colour='green')]

    
    print(vh.ctext.nline) #new line

    return images


def image_processing(images):
    # Step 1: Initialize an empty DataFrame

    results = {"year":[],
               "faces": []}


    # Step 2: Process each image
    for i in tqdm_bar(range(len(images)),desc="Using facedetection on images", colour="green"):
        # Detect faces in the image
        boxes, _ = mtcnn.detect(images[i])

        # Extract the year from the file path
        year = re.split(r'/|-', files_to_proces[i])[4]
        

        # If result is null it will use zero instead, (it cannot use len of 'None'). And then len can see how many faces are detected
        try:
            boxes = len(boxes)
        except:
            boxes = 0


        results["year"].append(year)
        results["faces"].append(boxes)

    return results



vh.work_here()

directory = ["..", "in"]

directory_path = os.path.join(*directory)

files_to_proces = check_files(file_list=list_files(directory_path), wanted_filetype=".jpg")

images = image_loader(files_to_proces)

mtcnn = MTCNN(keep_all=True)


# For testing 
images = images[:100]


results = image_processing(images)

dataframe = pl.from_dict(results)

dataframe.write_csv("../out/results.csv")

print(dataframe)




