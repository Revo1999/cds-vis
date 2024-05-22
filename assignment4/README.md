# Assignment 4: Detecting faces in historical newspapers

###### Victor Rasmussen, Visual Analytics, Aarhus University 
<br>

This assignment is part of a course at Aarhus University called Visual Analytics. Access the Assignment instructions on this [Github page](https://github.com/CDS-AU-DK/cds-visual/tree/main/assignments/assignment4) 

In this assignment we were asked to use Open-CV to design a simple search algorithm.

> **This is from the Assignment instructions linked above:** <br>
>
> You should write code which does the following:
> - For each of the three newspapers
>   - Go through each page and find how many faces are present
>   - Group these results together by decade and then save the following:
>       - A CSV showing the total number of faces per decade and the percentage of pages for that decade which have faces on them
>       - A plot which shows the latter information - i.e. percentage of pages with faces per decade over all of the decades available for that newspaper <br>
>
>  - Repeat for the other newspapers
> <br>
> <br>

```mtcnn_face_detection.py``` is a python program which loads images from the in folder, dividing them into each newspaper and decade by their file name, uses mtcnn face detection, creates csv's documenting percent of pages with faces and also how many faces per decade per newspaper. The program creates csv for each newspaper, but also a unified one containing all newspapers.

**The program works in three phases:**
> 1. Uses MTCNN model on all scanned images and creates results.csv a csv with two columns one with a relative filepath, and the amount of faces
>
> 2. It splits the csv into individual datasets for each unique newspaper name. Then it will perform different calculations and write new csv's. (These calculations will be elaborated in the results section)
>
> 3. Reads the csv produced in second phase, and visualizing these datasets using altair (with vega-fusion for polars dataframe support)

## Content table

1. [Introduction](#assignment-1-simple-image-search-algorithm)
2. [Project Structure](#project-structure)
3. [Data Source](#data-source)
4. [Usage](#usage)
5. [Flags](#flags)
6. [Compatibility & Other Uses](#compatibility--other-uses)
7. [Outputs](#outputs)
    1. [Compare Hist OpenCV](#compare-hist-opencv)
    2. [Nearest Neighbor Sci-kit Learn](#nearest-neighbor-sci-kit-learn)
8. [Limitations & Possible Improvements](#limitations--possible-improvements)

<br><br>



## Project Structure

```
assignment4/
├── analysis/
│   ├── analyzer.py
│   ├── dimensionchart.csv
│   └── run.sh
├── in/
│   ├── GDL
│   ├── IMP
│   ├── JDG
│   └── README-images.txt
├── out/
│   ├── GDL/
│   │   ├── faces_per_page.csv
│   │   ├── faces_per_page.png
│   │   ├── percent_of_pages_with_face.csv
│   │   └── percent_of_pages_with_face.png
│   ├── IMP/
│   │   ├── faces_per_page.csv
│   │   ├── faces_per_page.png
│   │   ├── percent_of_pages_with_face.csv
│   │   └── percent_of_pages_with_face.png
│   ├── JDG/
│   │   ├── faces_per_page.csv
│   │   ├── faces_per_page.png
│   │   ├── percent_of_pages_with_face.csv
│   │   └── percent_of_pages_with_face.png
│   ├── faces_per_page_all.csv
│   └── percent_of_pages_with_face_all.png
├── src/
│   └── mtcnn_face_detection.py
├── createVEnv.sh
├── image.png
├── README.md
├── requirements.txt
└── run.sh

```

## Data source

This assignment works with a corpus of historic Swiss newspapers: the Journal de Genève (JDG, 1826-1994); the Gazette de Lausanne (GDL, 1804-1991); and the Impartial (IMP, 1881-2017). Access data [here!](https://zenodo.org/records/3706863)

<br>

## Usage

**<u> The program is written for Python v.3.12.3, other versions might not function or produce unexpected behaviour. </u>**

1. Clone the repository

    ``` sh
    git clone  https://github.com/Revo1999/cds-vis.git
    ```
<br><br>
2. Insert the data as so it matches the folder-structure provided in Project structure.
<br><br>

3. Change directory into the assignment4 directory <br>
    ``` sh
    cd assignment4
    ```
    <br><br>

4. Setup virtual environment containing the packages needed to run both programs. <br>
    ``` sh
    bash createVEnv.sh
    ```
<br><br>

5. Runs ```mtcnn_face_detection.py``` by activating the virtual environment, and after the program has ran it will close the environment again.<br>
    ``` sh
    bash run.sh
    ```

6. It will prompt you to check if the files it removes are correct.

    ![](image.png?raw=true)
    ```
    write "y" or "n" in the console
    ```

<br>
<br>

## Compatibility & other uses

The program is written so it also can be used on other datasets, as long as they are **.jpg**.

You would have to modify these two functions to match the structure of your other data both functions use relative paths.

The regex expression will split the filename at ```/``` and ```-``` <br>
In this program the paths look like this ```"../in/GDL/GDL-1798....."``` regex split turn it into: <br><br> ["..", "in",**"GDL"**,"GDL",**"1798"**] <br><br> I've made the two selection 2 and 4 bold for clarity.

``` py
def extract_papername(filename):
    #Extracts papername from absolute path
    splitted_text = re.split(r'/|-', filename)
    paper = splitted_text[2]

    return paper
```

``` py
def extract_decade(filename):
    #Extracts year from absolute path
    splitted_text = re.split(r'/|-', filename)
    year = splitted_text[4]
```
## Outputs

![Description](out/percent_of_pages_with_face_all.png?raw=true)

![Description](out/faces_per_page_all.png?raw=true)

## Limitations & possible improvements

### To Batch or not to Batch?

The code is fairly ressource intensive. While the code is written so it doesn't utilize batch processing, as to batch process its required for the images to have the same dimensions(if you try it will tell you so in the console). To explore the idea a bit more, there is 4624 images, hence an overlap in image dimensions could be present. I've looked at the images, and organized them by image size (in polars). In the table (dimensionchart.csv.csv), it shows has 354 entries meaning you would have to have 354 different batches. This is without any modification of the images, this might improve performance, given that batch-processing often is faster than individual processing when using models.

I've abandoned the idea, due to the dataset having a picture, with missing bites, an issue Pillow's ```img.verify() ``` can't detect. This would then make a whole batch unprocessable, and will first tell you when it gives an error, again leading to loss in efficiency, because the code needs to be rerun. While other dataset with uniform picture width and heights, might benefit from using batch processing, defect images cause it trouble. The code is therefore written to accommodate damaged files, and different image sizes.