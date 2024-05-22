# Assignment 1 - Simple image search algorithm

###### Victor Rasmussen, Visual Analytics, Aarhus University 
<br>

This repo is part of a course at Aarhus University called Visual Analytics. Th

This project includes two projects ```open_cv_compare.py``` and ```nearest_neighbor.py```

Specific task at hand

 files that go through 1300 .jpg's (From the 17 flowers dataset), creates a histogram, and compares them with a chosen image, resulting in a distance value. The five highest values are printed in to a csv in the out folder.

## Project Structure

```

.
└── Assignment1/
    ├── data/
    │   ├── image_0001.jpg
    │   └── image_0002.jpg
    ├── out/
    │   └── table.csv
    ├── src/
    │   └── assignment1.py
    ├── readme.md
    ├── requirements.txt
    └── setup.sh

```

## Data source

The dataset used is the 17 Category Flower Dataset by Maria-Elena Nilsback and Andrew Zisserman. It can be accessed [here!](https://www.robots.ox.ac.uk/~vgg/data/flowers/17/) (Beware of terms of usage!) The dataset contains 17 categories of flowers with 80 images of each.

<br>

## Usage

1. Insert the data as so it matches the folder-structure provided in Project structure. The program is written for **Python v.3.12.3**, other versions might not function or produce unexpected behaviour.
<br><br>

2. run ```bash createVEnv.sh``` in console, will setup virtual environment containing the packages needed to run both programs.
<br><br>
3. run ```bash run.sh``` in console will run ```open_cv_compare_hist.py``` &  ```nearest_neighbor.py``` by activating the virtual environment, and after the program has ran it will close the environment again

<br>
<br>

## Flags for ```open_cv_compare_hist.py``` & ```nearest_neighbor.py```:

- `-I`, `--Image_name`: Name the image file you want to compare to the rest of the images (default: "image_0321.jpg").<br><br>

    >Example: ```python nearest_neighbor.py -I image_0001.jpg``` <br>
    >Example: ```python open_cv_compare_hist.py -I image_0002.jpg```

<br>
<br>

## Compatibility & other uses

Both programs are written to be able to accept other datasets. This mean you could use other datasets, be aware the code is written to accept images of **".jpg"**. The dataset must be placed directly into the data folder (as shown in project structure). If your dataset contains other filetypes, you dont have to manually remove them, the program simply disregard these.

## Outputs

## Limitations & possible improvements