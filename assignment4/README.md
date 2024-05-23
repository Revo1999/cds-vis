# Assignment 4: Detecting faces in historical newspapers

###### Victor Rasmussen, Visual Analytics, Aarhus University 
<br>

This assignment is part of a course at Aarhus University called Visual Analytics. Access the Assignment instructions on this [Github page](https://github.com/CDS-AU-DK/cds-visual/tree/main/assignments/assignment4) 

In this assignment we are asked to use Open-CV to design a simple search algorithm.

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

```mtcnn_face_detection.py``` is a python program which loads images from the in folder, dividing them into each newspaper and decade by their file name, uses mtcnn face detection, creates csv's documenting the percent of pages with faces and also how many faces per decade per newspaper. The program creates csv for each newspaper, but also a unified one containing all newspapers.

**The program works in three phases:**
> 1. Uses MTCNN model on all scanned images and creates results.csv a csv with two columns one with a relative filepath, and the amount of faces
>
> 2. It splits the csv into individual datasets for each unique newspaper name. Then it will perform different calculations and write new csv's. (These calculations will be elaborated in the results section)
>
> 3. Reads the csv produced in second phase, and visualizes these datasets using altair (with vega-fusion for polars dataframe support)

## Table of contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Data Source](#data-source)
4. [Usage](#usage)
5. [Compatibility & Other Uses](#compatibility--other-uses)
6. [Outputs](#outputs)
    1. [Graph Analysis](#graph-analysis)
7. [Limitations & Possible Improvements](#limitations--possible-improvements)

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

This assignment works with a corpus of historic Swiss newspapers: the Journal de Genève (JDG, 1826-1994); the Gazette de Lausanne (GDL, 1804-1991); and the Impartial (IMP, 1881-2017). Access the data [here!](https://zenodo.org/records/3706863)

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

4. Set up virtual environment containing the packages needed to run both programs. <br>
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
    Type "y" or "n" in the console
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

- GDL (Gazette de Lausanne) in <span style="color:blue">blue</span>
- JDG (Journal de Genève) in <span style="color:red">red</span>
- IMP (L'Impartial) in <span style="color:orange">orange</span>

<br>

Going in to the results i suspected that MTCNN might perform better on newer images, due to the evolution of technology, mainly printing techniques(easier for the algorithm to detect the faces) and cameras(easier to take pictures and place them in newspaper). The MTCNN is trained on [CASIA-WEBFACE](https://paperswithcode.com/paper/learning-face-representation-from-scratch). Which is 494,414 face images of 10,575 real identities collected from the web. I suspect these images are newer (in relation to our earliest data points are pre 1800's, which is long prior to the existance of "the web" ). <br><br>

![Description](out/faces_per_page_all.png?raw=true)

Looking into the first graph its clear that the amount of faces explodes for IMP(L'Impartial) around the 1990's, was a daily newspaper similar to Daily express covering politics. GDL and JDG also have a small increase but not in relation to IMP.

Generally, all the newspapers rise steadily from the first data points onward to the last. This could be as earlier mentioned both be because of camera technology evovling, but also printing quality getting better, thereby making it easier for MTCNN to detect faces.


![Description](out/percent_of_pages_with_face_all.png?raw=true)

As well as the faces per page graph, percent of pages with faces also increase from 1840 and onwards. IMP also rise a little more aggressive with percent of pages with face since the first data points. This could indicate editorial policies pushing towards more content with images containing faces. In this period from 1880 GDL and JDG also increase, thus having lower numbers.

GDL data points from 1840 is at the graph hitting zero, this is due to not having any datapoints for this period at all. 

Generally it's hard to attribute the evolution in graphs to specific technology or journalistic practices, it might be a combination, though it's evident that MTCNN face detection finds more faces per page, on more percent of the scanned images have faces generally trending towards a rise for all newspapers from 1880 onward. Especially IMP explodes which i attribute mainly to journalistic practices for this newspaper. As the other two newspaper have the same conditions technologically.

## Limitations & possible improvements

### To Batch or not to Batch?

The code is fairly ressource intensive. While the code is written so it doesn't utilize batch processing, while MTCNN batch processing requires the images to have the same dimensions (if you try it will tell you so in the console). To explore the idea a bit more, there is 4624 images, hence an overlap in image dimensions could be present. I've looked at the images, and organized them by image size [Analyzer.py](https://github.com/Revo1999/cds-vis/blob/main/assignment4/analysis/analyzer.py). In the table [dimensionchart.csv](https://github.com/Revo1999/cds-vis/blob/main/assignment4/analysis/dimensionchart.csv), it shows has 354 entries meaning you would have to have 354 different batches. This is without any modification of the images, this might improve performance, given that batch-processing often is faster than individual processing when using models.

I've abandoned the idea, due to the dataset having a couple of pictures, with missing bites, an issue Pillow's ```img.verify() ``` can't detect. This would then make a whole batch unprocessable, and will first tell you when it gives an error, again leading to loss in efficiency, because the code needs to be rerun. In the current state if an individual image cant be processed by MTCNN it will continue without it (it's in a try/except statement).
While other dataset with uniform picture width and heights, might benefit from using batch processing, defect images cause it trouble. The code is therefore written to accommodate damaged files, and different image sizes.

### Face-detection

MTCNN face detection does not detect all faces, sifting through some of the results in earlier stages of programming this program, i noticed a couple of pages with faces that did'nt got recognized. I do not have any exact amount of how many faces it missed, but it missed a few of the around 50 images i looked at.

### Preprocessing

Preprocessing might improve upon performance, setting up more lightweight algorithms to access pictures before MTCNN process them, or cutting down image resolutions can produce very similar results, for less computing power.

