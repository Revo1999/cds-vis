# Assignment 4 - Detecting faces in historical newspapers

#### Victor Rasmussen
##### Aarhus University, Language Analytics

This assignment works with a corpus of historic Swiss newspapers: the Journal de Genève (JDG, 1826-1994); the Gazette de Lausanne (GDL, 1804-1991); and the Impartial (IMP, 1881-2017). The program uses a MTCNN (Multi-task Cascaded Convolutional Networks) to detect faces in the scans of these newspaper.

The program works in three phases:
> 1. Uses MTCNN model on all scanned images and creates results.csv a csv with two columns one with a relative filepath, and the amount of faces
>
> 2. It splits the csv into individual datasets for each unique newspaper name. Then it will perform different calculations and write new csv's. (These calculations will be elaborated in the results section)
>
> 3. Reads the csv produced in second phase, and visualizing these datasets using altair (using vega-fusion for polars dataframe support)

<br><br>

# Folder structure

```
Assignment 4/
├── analysis/
│   ├── analyzer.py
│   ├── run.sh
│   └── dimensionschart.csv
├── in/
│   ├── GDL
│   ├── IMP
│   ├── JDG
│   └── README-images.txt
├── out/
│   ├── faces_per_page.csv
│   ├── LineChart.png
│   ├── LineChart1.png
│   ├── pages_with_faces.csv
│   └── results.csv
├── src/
│   └── mtcnn_face_detection.py     
├── createVEnv.sh
├── image.png
├── README.md
├── requirements.txt
└── run.sh
```
<br><br>

# Usage
It will prompt you to check

> ![](image.png?raw=true)

## Data Access

[click here!](https://zenodo.org/records/3706863)



### Results

![Description](out/LineChart1.png?raw=true)

![Description](out/LineChart.png?raw=true)

### To Batch or not to Batch?

The code is fairly ressource intensive. While the code is written so it doesn't utilize batch processing, as to batch process its required for the images to have the same dimensions(if you try it will tell you so in the console). To explore the idea a bit more, there is 4624 images, hence an overlap in image dimensions could be present. I've looked at the images, and organized them by image size (in polars). In the table (GroupedResults.csv), it shows has 354 entries meaning you would have to have 354 different batches. This is without any modification of the images, this might improve performance, given that batch-processing often is faster than individual processing when using models.

I've abandoned the idea, due to the dataset having a picture, with missing bites, an issue Pillow's ```img.verify() ``` can't detect. This would then make a whole batch unprocessable, and will first tell you when it gives an error, again leading to loss in efficiency, because the code needs to be rerun. While other dataset with uniform picture width and heights, might benefit from using batch processing, defect images cause it trouble. The code is therefore written to accommodate damaged files, and different image sizes.






Python 3.12.3