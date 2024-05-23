# Assignment 3: Document classification using pretrained image embeddings

###### Victor Rasmussen, Visual Analytics, Aarhus University 
<br>

This assignment is part of a course at Aarhus University called Visual Analytics. Access the Assignment instructions on this [Github page](https://github.com/CDS-AU-DK/cds-visual/tree/main/assignments/assignment3) 

> **This is from the Assignment instructions linked above:** <br>
>For this exercise, you should write some code which does the following:
>
> You should write code which does the following:
> - Loads the Tobacco3482 data and generates labels for each image <br> <br>
> - Train a classifier to predict document type based on visual features <br> <br>
> - Present a classification report and learning curves for the trained classifier <br> <br>
> - Your repository should also include a short description of what the classification report and learning curve show. <br> <br>

```document_classifier.py``` is a python program which loads images from Tobacco-dataset into a VGG16 model for image classification. It preprocess and prepares the dataset, trains the model. The program creates classification reports and plots which can be used to analysis.

## Table of Contents

## Table of Contents

1. [Introduction](#assignment-3-document-classification-using-pretrained-image-embeddings)
2. [Project Structure](#project-structure)
3. [Data Source](#data-source)
4. [Usage](#usage)
5. [Compatibility & Other Uses](#compatibility--other-uses)
6. [Outputs](#outputs)
7. [Limitations & Possible Improvements](#limitations--possible-improvements)

<br><br>



## Project Structure

```
assignment3/
└── in/
    └── Tobacco3482/
        ├── ADVE
        ├── Email
        ├── Form
        ├── ...
        └── ...
model/
└── tobacoo_model.h5
out/
├── Loss_Acc_Curves.png
└── tobacco_report.txt
src/
├── document_classifier.py
├── createVEnv.sh
├── image.png
├── README.md
├── requirements.txt
└── run.sh

```

## Data source

The Tobacco-3482 dataset consists of images belonging to 10 different classes including Letter, Memo, Email etc. The dataset has a total of 3482 images. All images are from Tobacco industry hence the name.
 It can be accessed [here!](https://www.kaggle.com/datasets/patrickaudriaz/tobacco3482jpg?resource=download)

<br>

## Usage

**<u> The program is written for Python v.3.12.3, other versions might not function or produce unexpected behaviour. </u>**

1. Clone the repository

    ``` sh
    git clone  https://github.com/Revo1999/cds-vis.git
    ```
<br>

2. Insert the data as so it matches the folder-structure provided in Project structure.
<br><br>

3. Change directory into the assignment3 directory <br>
    ``` sh
    cd assignment3
    ```
    <br>

4. Setup virtual environment containing the packages needed to run both programs. <br>
    ``` sh
    bash createVEnv.sh
    ```
<br>

5. Run ```document_classifier.py``` by activating the virtual environment, changing directory into src and after the program has ran it will change directory back and it will close the environment again.<br>
    ```sh
    bash run.sh
    ``` 
<br>

6. It will prompt you to check if the files it removes are correct.

    ![](image.png?raw=true)
    ```
    Type "y" in the console
    ```
<br>

## Compatibility & other uses

This program is not written specifically for the tobacco-dataset. If you have another dataset in **".jpg"**-format with images categorized in folder it will work with one change. The directory would have to be changed. Which can be edited in line 170 in the  ```document_classifier.py```:

``` py
directory = ["..", "in", "Tobacco3482"]
```

## Outputs

![Hello](out/Loss_Acc_Curves.png?raw=true)

It seems like the model is overfitting as the accuracy on the training data, is quite a bit higher than, than the validation data. This indicate that the model have room for improvement in terms of the training. 

The loss curve is interpreted as the difference between the train_loss and validation_loss is initially the difference in performance between training and validation, this means any difference shown is a sign of overfitting, baring in mind that small differences is expected as the data the model is presented is different.

```
              precision    recall  f1-score   support

        News       0.86      0.84      0.85        43
        ADVE       0.86      0.81      0.83       126
        Memo       0.80      0.38      0.51        96
      Letter       0.42      0.83      0.55       106
       Email       0.58      0.44      0.50       117
      Resume       0.73      0.75      0.74        40
        Form       0.61      0.62      0.62        40
  Scientific       0.42      0.46      0.44        54
      Report       0.50      0.14      0.22        21
        Note       0.34      0.28      0.31        54

    accuracy                           0.59       697
   macro avg       0.61      0.55      0.56       697
weighted avg       0.63      0.59      0.58       697
```
 The classification report shows that the model's overall accuracy is 0.59, which is relatively low for a classification task, 0.7 or higher is typically considered more reasonable News and ADVE have reasonably good precision and recall. "Memo" have good precision but horrible recall, meaning when it guess memo it's correct 80% of the time, but it is only finding 38% procent of them.
 
The model struggles with classifying "Note" and "Letter". Notes can vary a lot in how they can look since notes generally have less stylistic rules than other categories. Letters may also vary quite a bit in style. Which can explain the low numbers.

## Limitations & possible improvements

### Overfitting problem

To improve the overfitting situation quite a few things can be done. I've tried to list some ideas, none of these have been tried:

- Artificially make the dataset larger using data-augmentation
- Using different parameters:
    - early stopping
    - L1 or L2 regulization (more information about: [implementation](https://www.tensorflow.org/api_docs/python/tf/keras/regularizers/L1L2) & [theory](https://medium.com/@fernando.dijkinga/explaining-l1-and-l2-regularization-in-machine-learning-2356ee91c8e3))
- Collect more data (this is difficult and not very viable)
