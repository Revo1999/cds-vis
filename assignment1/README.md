# Assignment 1 - Simple image search algorithm

###### Victor Rasmussen, Visual Analytics, Aarhus University 
<br>

This assignment is part of a course at Aarhus University called Visual Analytics. Access the Assignment instructions on this [Github page](https://github.com/CDS-AU-DK/cds-visual/tree/main/assignments/assignment1) 

In this assignment we were asked to use Open-CV to design a simple search algorithm.

> **This is from the Assignment instructions linked above:** <br>
>For this exercise, you should write some code which does the following:
>
> Define a particular image that you want to work with:
>   - For that image
>       - Extract the colour histogram using OpenCV
>        - Extract colour histograms for all of the other images in the data
>        - Compare the histogram of our chosen image to all of the other histograms
>        For this, use the cv2.compareHist() function with the cv2.HISTCMP_CHISQR metric
>       - Find the five images which are most similar to the target image.
>       - Save a CSV file to the folder called "out", showing the five most similar images and the distance metric. 
>
> <u>Additionally we were asked to make another version of the assignment above using the nearest neighbor model from sci-kit learn </u>

This project includes two projects ```open_cv_compare.py``` and ```nearest_neighbor.py```

```open_cv_compare.py``` is a python program which loads images from the in folder, creates histograms, which it then compares to find the 5 closest to the target image. Using OpenCV's ```compareHist()``` function.


```nearest_neighbor.py``` is a python program which loads images using the pre-trained VGG16 model, then it calculates distances from the VGG16's vectors using sci-kit learns nearest neighbor model.

Both programs produce a csv and plots to show the results.



## Project Structure

```
assignment1/
├── in/
│   ├── image_0001.jpg
│   ├── image_0002.jpg
│   └── image_0003.jpg
├── out/
│   ├── compare_hist_image_0321.jpg_results.csv
│   ├── compare_hist.png
│   ├── nearest_neighbor_image_0321.jpg_results.csv
│   └── nearest_neighbor.png
├── src/
│   ├── nearest_neighbor.py
│   └── open_cv_compare_hist.py     
├── createVEnv.sh
├── README.md
├── requirements.txt
├── run_custom.sh
└── run.sh

```

## Data source

The dataset used is the 17 Category Flower Dataset by Maria-Elena Nilsback and Andrew Zisserman. It can be accessed [here!](https://www.robots.ox.ac.uk/~vgg/data/flowers/17/) (Beware of terms of usage!) The dataset contains 17 categories of flowers with 80 images of each.

<br>

## Usage

**<u> The program is written for Python v.3.12.3, other versions might not function or produce unexpected behaviour. </u>**

1. Clone the repository

    ``` git clone  https://github.com/Revo1999/cds-vis.git```
<br><br>
2. Insert the data as so it matches the folder-structure provided in Project structure.
<br><br>

3. Change directory into the assignment1 directory <br>
    ``` cd assignment1```
    <br><br>

4. Setup virtual environment containing the packages needed to run both programs. <br>
```bash createVEnv.sh```
<br><br>

5. Run open_cv_compare_hist.py &  nearest_neighbor.py by activating the virtual environment, and after the program has ran it will close the environment again.<br>
```bash run.sh``` <br><br>
**For custom execution use** ```bash run_custom.sh``` it will prompt you to select which program to run here you can apply flags to the execution this does also automatically open and close the virtual environment: <br> ```bash run_custom```  then write for example: ```nearest_neighbor.py -I image_0001.jpg```.

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

When comparing images of flowers using computers, the goal is the find similarities in the pictures which can be of use. In this case with the flowers dataset the goal of a good algorithm can be said to be finding similar flowers, or the same catagory of flowers.

### Compare Hist OpenCV

![Description](out/compare_hist.png?raw=true)

```compareHist()``` computes the images and calculates how similar the colors are across the whole picture. To the eye the picture i've chosen purple is dominant as the colour of the flower, and you would think it would result in similar images also with purple flowers. compareHist does not take spatial information into count, and I imagine that the different colours is the result of comparehist having RGB channels. So Purple is constructed mostly of red and blue therefore red and blue flowers would overlap in the "r" & "b" values. ```compareHist()``` does not take spatial information into acount this also leads to a significant loss of data.

If the goal is to catagorize flowers, or find similar flowers compareHist does not succeed.


##### Compare Hist OpenCV CSV [Access here!](https://github.com/Revo1999/cds-vis/blob/main/assignment1/out/compare_hist_image_0321.jpg_results.csv)
|Filename|Distance      |
|--------|--------------|
|image_0321.jpg|0.0     |
|image_0189.jpg|1510.8  |
|image_0043.jpg|1558.3  |
|image_0525.jpg|1564.5  |
|image_1249.jpg|1567.0  |
|image_1096.jpg|1579.1  |



### Nearest Neighbor Sci-kit learn
![Description](out/nearest_neighbor.png?raw=true)

Unlike ```compareHist()```, nearest neighbor uses the spatial information in the image files. Using VGG16 the model leverage deep learning techniques used in preprocessing of pictures, this type of feature extraction helps the models "understand" the images that they are presented. Nearest neighbor looks for cosine similarity between the pictures.

In the results of it's clear it picks up the colour of the flowers better. This could be due to the spatial information of the pictures. As the colors typically is clustered.

If the goal is to categorize flowers it's performing really well in this example. As mentioned earlier the dataset is comprised of 80 images per category, this means the image chosen (image 321) is from a category ranging from 320 to 400. This also means the 5 images with the lowest distance all fit this category.

##### Nearest Neighbor Sci-kit learn CSV [Access here!](https://github.com/Revo1999/cds-vis/blob/main/assignment1/out/nearest_neighbor_image_0321.jpg_results.csv)

|Filename|Distance    |
|--------|------------|
|image_0321.jpg|0.0   |
|image_0351.jpg|0.079 |
|image_0371.jpg|0.108 |
|image_0333.jpg|0.141 |
|image_0328.jpg|0.157 |
|image_0343.jpg|0.157 |

## Limitations & possible improvements

OpenCV's comparehist has some clear limitations. In terms of catagorizing flowers. VGG16 + Nearest Neighbor performes significantly better. VGG16 does however take significantly more computing power, than compareHist. That said VGG16 is known to be small in size for the type of model that it is. <br> Possible improvements could be tweaking different settings. Nearest Neighbor can look for similarities with different options, this project uses cosine, but testing might reveal other options that yield better results. 

Both programs could improve in compability, and also have error-handling, as of right now both programs would crash with damaged images. Also the programs could include more options towards filetype's of pictures. Both programs only accept JPG, other datasets could have other formats, which the programs cant handle.

As of rightnow the plots are pretty much hardcoded, so if you wanted to have the ten closest it would mess up the plots, this is why there isn't created a option for this. This could be improved upon.
