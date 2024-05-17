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

def image_verify_and_load(img_path):
    #Tested this with corrupted images and it works
    try:
        # Opens Image
        with Image.open(img_path) as img:
            img.verify()
            # If verification is succesful assign image
            image = Image.open(img_path)
            os.path.getsize(img_path)
            return image
    except Exception as e:
        # Image couldnt load do this tell me why
        print(f"Error opening image '{img_path}': {e}")
        return None

def image_loader(image_paths_to_proces):

    images = [image_verify_and_load(img_path) for img_path in tqdm_bar(image_paths_to_proces, desc="Loading images", colour='green')]

     # Keeps the values if not None, effectively removing all errors caught by img.verify() by Pillow used in image_verify_and_load()
    images = [image for image in images if image is not None]

    print(vh.ctext.nline) #new line

    return images


def image_processing(images):
    results = {"year":[],
               "faces": []}

    # Processing each image from the processing list, it can only batch process pictures with the same pixel size
    for i in tqdm_bar(range(len(images)),desc="Using facedetection on images", colour="green"):
        try:
            # Detect faces in the image
            boxes, _ = mtcnn.detect(images[i])

            # Extract the year from the file path
            '''year = re.split(r'/|-', files_to_proces[i])[4]'''

            # If result is null it will use zero instead, (it cannot use len of 'None'). And then len can see how many faces are detected
            try:
                boxes = len(boxes)
            except:
                boxes = 0

            # Append results to a dict
            results["year"].append(files_to_proces[i])
            results["faces"].append(boxes)
        except OSError as e:
            # excepting truncation error (    these are not caught in img.verify()    )
            print(f"Error processing image {files_to_proces[i]}: {e}")
            continue  # Continues

    return results

def dict_to_csv(data, savepath):
    dataframe = pl.from_dict(data)
    dataframe.write_csv(savepath)

def extract_decade(filename):
    splitted_text = re.split(r'/|-', filename)[4]
    # Calculates the remainder when decade is divided by 10, this means I always can turn the value to the lower then, effectivelyextracting the decade
    decade = int(splitted_text) - (int(splitted_text) % 10)
    return decade

def convert_table(dataset):
    data = dataset
    # Apply extract_decade() to all values in the year column
    data = data.with_columns(data['year'].map_elements(extract_decade).alias('decade'))

    # Faces is group by decade and sum amount of faces, then pages counts the amount of decades from the decade list
    occur_decade_faces = data.group_by("decade").agg([pl.col("faces").sum(), pl.len().alias("pages")])



    # divides faces with pages to get faces pr. page. Float needs to be assigned when casted.
    results = occur_decade_faces.with_columns((pl.col("faces").cast(pl.Float64) / pl.col("pages").cast(pl.Float64)).alias("faces_per_page"))

    results_sorted = results.sort("decade")
    
    return results_sorted


def main():
    directory = ["..", "in"]

    directory_out = ["..", "out", "results.csv"]

    directory_path = os.path.join(*directory)

    files_to_proces = check_files(file_list=list_files(directory_path), wanted_filetype=".jpg")

    images = image_loader(files_to_proces)

    mtcnn = MTCNN(keep_all=True)

    results = image_processing(images)

    dict_to_csv(convert_table(results), os.path.join(*directory_out))


if __name__ == "__main__":
    main()