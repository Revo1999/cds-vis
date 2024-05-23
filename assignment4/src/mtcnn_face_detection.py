'''
Assignment 4
    Victor Rasmussen
        Visual Analytics, Aarhus University
            17-05-2024
'''

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
import altair as alt
import vegafusion as vf

'''from random import choice''' # Used for testing



def list_files(directory):
    '''
    List files in "in" folder with full paths
    '''

    folders = os.listdir(directory)

    all_files = []
    for root, dirs, files in os.walk(directory, topdown=True):
        for filenames in files:
            all_files.append(os.path.join(root, filenames))

    return all_files


def check_files(file_list, wanted_filetype):

    '''
    Checks files to see if they are the wanted type

    Provides overview in console
    As well as asking users if they want to remove the files from the processing list
    A no will quit the program

    '''

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
    # Takes input
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
    #Tested this with corrupted images and it works for corruption will not detect missing bytes (truncation)
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

    '''
    Loads images from list
    '''

    images = [image_verify_and_load(img_path) for img_path in tqdm_bar(image_paths_to_proces, desc="Loading images", colour='green')]

     # Keeps the values if not None, effectively removing all errors caught by img.verify() by Pillow used in image_verify_and_load()
    images = [image for image in images if image is not None]

    print(vh.ctext.nline) #new line

    return images


def image_processing(images, model, file_list):
    results = {"year":[],
               "faces": []}

    # Processing each image from the processing list, it can only batch process pictures with the same pixel size
    for i in tqdm_bar(range(len(images)),desc="Using facedetection on images", colour="green"):
        try:
            # Detect faces in the image
            boxes, _ = model.detect(images[i])

            # If result is null it will use zero instead, (it cannot use len of 'None'). And then len can see how many faces are detected
            try:
                boxes = len(boxes)
            except:
                boxes = 0

            # Append results to a dict
            results["year"].append(file_list[i])
            results["faces"].append(boxes)
        except OSError as e:
            # excepting truncation error (    these are not caught in img.verify()    )
            print(f"Error processing image {file_list[i]}: {e}")
            continue  # Continues

    return results

def dict_to_csv(data, savepath):
    #Converts dict to polars dataframe

    dataframe = pl.from_dict(data)
    dataframe.write_csv(savepath)

def seperate_newspaper(data):
    
    """
    Separates the dataset by newspaper.

    This function adds a new column 'newspaper' extracted from the 'year' column,
    and returns a list of datasets, each filtered the unique newspaper name.
    """

    dataset_list = []

    # Extracts newspapernames from the year column (which contains relative paths)
    data = data.with_columns((pl.col("year").map_elements(extract_papername).cast(pl.Utf8)).alias("newspaper"))

    # Gets unique newspaper names
    unique_papers = data.select(pl.col("newspaper").unique()).to_series()

    # Filters the data for each unique newspaper and store in the list
    for unique_paper in unique_papers:
        unique_paper_dataset = data.filter(pl.col("newspaper") == unique_paper)
        dataset_list.append(unique_paper_dataset)

    return dataset_list

def extract_papername(filename):
    #Extracts papername from absolute path
    splitted_text = re.split(r'/|-', filename)
    paper = splitted_text[2]

    return paper

def extract_decade(filename):
    #Extracts year from absolute path
    splitted_text = re.split(r'/|-', filename)
    year = splitted_text[4]

    # Calculates the remainder when year is divided by 10, this means I always can turn the value to the lower then, effectively extracting the decade
    decade = int(year) - (int(year) % 10)
    return decade

def pages_with_faces_table(data):
    # Apply extract_decade() to all values in the year column
    data = data.with_columns(data['year'].map_elements(extract_decade).alias('decade'))

    # Calculates the number of pages with faces by creating a new column with 0 or 1
    data = data.with_columns((data['faces'] > 0).cast(pl.Int8).alias("has_faces"))

    # Groups by decade and newspaper, then sums the binary values to count the pages with faces
    occur_decade_faces = data.group_by(["decade", "newspaper"]).agg([
        pl.len().alias("total_pages"),
        pl.sum("has_faces").alias("pages_with_faces")
    ])

    # Calculate percent by dividing pages with faces with total pages times 100
    results = occur_decade_faces.with_columns(
        (pl.col("pages_with_faces").cast(pl.Float64) / pl.col("total_pages").cast(pl.Float64)*100)
        .alias("percent_of_pages_with_face"))

    return results



def faces_per_page_table(data):
    # Apply extract_decade() to all values in the year column
    data = data.with_columns(data['year'].map_elements(extract_decade).alias('decade'))

    
    occur_decade_faces = data.group_by(["decade", "newspaper"]).agg([pl.col("faces").sum(), pl.len().alias("pages")])

    # divides faces with pages to get faces pr. page. Float needs to be assigned when casted.
    results = occur_decade_faces.with_columns((pl.col("faces").cast(pl.Float64) / pl.col("pages").cast(pl.Float64)).alias("faces_per_page"))

    results_sorted = results.sort("decade")
    
    return results_sorted



def data_conversion(data, method):
    
    """

    Adds all dataset operations together

    First it seperates the dataset into each paper, then it calculates faces_per_page (also adding faces and pages columns)

    Then the datasets are concated back together again

    """

    dataset_list = []

    for dataset in seperate_newspaper(data=data): # Seperates datasets into newspaper
        converted_dataset = method(dataset) # applies method function to all datasets
        dataset_list.append(converted_dataset)
    
    joined_data = pl.concat(dataset_list) #joins data back together for a connected model

    return joined_data, dataset_list

def visualize_line_chart(data, y_value, y_title):
    
    '''
    Altair plotting of data

    Modified version of this template:
    https://altair-viz.github.io/gallery/line_with_last_value_labeled.html 
    
    '''


    y_value = str(y_value + ":Q")

    # Creates chat instance
    chart = alt.Chart(data).transform_filter(
        alt.datum.newspaper != ""  # Filter out empty newspaper names
    ).encode(
        alt.Color("newspaper").legend(None)
    )

    # Draws the line
    line = chart.mark_line().encode(
        x=alt.X("decade:Q", title="Decade"),  # Title for the x-axis
        y=alt.Y(y_value, title=y_title)  # Title for the y-axis
    )

    # Finds last value
    label = chart.encode(
        x=alt.X('max(decade):Q', title="Decade"),  # Title for the x-axis
        y=alt.Y(y_value, title=y_title).aggregate(argmax='decade'),  # Title for the y-axis
        text='newspaper'
    )

    # Creates text labels
    text = label.mark_text(align='left', dx=4)

    # Creates circles
    circle = label.mark_circle()

    # Combines all from the chart and draws it with width and height settings applied
    return line + circle + text.properties(width=500, height=400)

def main():
    vh.work_here()

    directory = ["..", "in"]

    directory_out = ["..", "out", "results.csv"]

    directory_path = os.path.join(*directory)

    # Checks filetypes
    files_to_proces = check_files(file_list=list_files(directory_path), wanted_filetype=".jpg")

    '''files_to_proces = [choice(files_to_proces) for _ in range(20)]''' # Used for testing
    
    # Loads images
    images = image_loader(files_to_proces)

    # Loads model
    mtcnn = MTCNN(keep_all=True)

    results = image_processing(images=images, model=mtcnn, file_list=files_to_proces)

    data = pl.from_dict(results)

    faces_per_page_data, faces_list = (data_conversion(data=data, method=faces_per_page_table))

    pages_with_face_data, pages_list = (data_conversion(data=data, method=pages_with_faces_table))


    # Writes Polars Dataframes to CSV's
    faces_per_page_data.write_csv("../out/faces_per_page.csv")

    pages_with_face_data.write_csv("../out/pages_with_faces.csv")

    vf.enable()

    visualize_line_chart(data=faces_per_page_data, y_value="faces_per_page", y_title="faces per page").save("../out/faces_per_page_all.png")

    visualize_line_chart(data=pages_with_face_data, y_value="percent_of_pages_with_face", y_title="Percent of pages with face").save("../out/percent_of_pages_with_face_all.png")

    for i in range(0, len(faces_list)):
        newspaper_name = (faces_list[i]['newspaper'].unique()).to_list()[0]

        # Makes folders for each newspaper name
        os.mkdir(os.path.join("..","out", newspaper_name))

        visualize_line_chart(data=faces_list[i], y_value="faces_per_page", y_title="faces per page").save(f"../out/{newspaper_name}/faces_per_page.png")
        visualize_line_chart(data=pages_list[i], y_value="percent_of_pages_with_face", y_title="Percent of pages with face").save(f"../out/{newspaper_name}/percent_of_pages_with_face.png")
        
        # Writes Polars Dataframes to CSV's
        faces_list[i].write_csv(f"../out/{newspaper_name}/faces_per_page.csv")
        pages_list[i].write_csv(f"../out/{newspaper_name}/percent_of_pages_with_face.csv")
        
if __name__ == "__main__":
    main()