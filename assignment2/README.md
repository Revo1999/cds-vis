# Assignment 2: Classification benchmarks with Logistic Regression and Neural Networks

###### Victor Rasmussen, Visual Analytics, Aarhus University 
<br>

This assignment is part of a course at Aarhus University called Visual Analytics. Access the Assignment instructions on this [Github page](https://github.com/CDS-AU-DK/cds-visual/tree/main/assignments/assignment2) 

In this assignment we were asked to write two programs which utilize sci-kit learns logistic regression classifier and neural network classifier and evaluate their performance

> **This is from the Assignment instructions linked above:** <br>
>For this exercise, you should write some code which does the following:
>   - Load the Cifar10 dataset
>   - Preprocess the data (e.g. greyscale, normalize, reshape)
>   - Train a classifier on the data
>   - A logistic regression classifier and a neural network classifier
>   - Save a classification report
>   - Save a plot of the loss curve during training (Only for MLP Classifier)
>   <br> <br>

This project includes two projects ```lr.py``` and ```mlp.py```

```lr.py```  is a python program which loads the CIFAR-10 dataset, preprocess the images på normalizing and converting to greyscale, after training sci-kit learns logistic regression it will give a classification report


```mlpr.py``` is a python program which loads the CIFAR-10 dataset, preprocess the images på normalizing and converting to greyscale, after training sci-kit learns mlp-model it will give a classification report and also plot the loss curve.

Both programs produce a csv and plots to show the results.

## Contents Table

1. [Introduction](#assignment-2-classification-benchmarks-with-logistic-regression-and-neural-networks)
2. [Project Structure](#project-structure)
3. [Data Source](#data-source)
4. [Usage](#usage)
5. [Compatibility & Other Uses](#compatibility--other-uses)
6. [Outputs](#outputs)
7. [Limitations & Possible Improvements](#limitations--possible-improvements)

<br><br>



## Project Structure

```
Assignment 2/
├── out/
│   ├── logistic.txt
│   ├── neural_loss_curve.png
│   └── neural.txt
├── src/
│   ├── lr.py
│   └── mlp.py     
├── createVEnv.sh
├── README.md
├── requirements.txt
└── run.sh

```

## Data source

The CIFAR-10 dataset has 60000 32 x 32 pixels color images in 10 classes.
There is 6000 images per class. The dataset is split in 50000 training images and 10000 test images. Data can be acessed [here!](https://www.cs.toronto.edu/~kriz/cifar.html)

In both programs the dataset is downloaded directly using:

```py
from tensorflow.keras.datasets import cifar10

(X_train, y_train), (X_test, y_test) = cifar10.load_data()
```
Keras API documentation can be found [here!](https://keras.io/api/datasets/cifar10/)



<br>

## Usage

**<u> The program is written for Python v.3.12.3, other versions might not function or produce unexpected behaviour. </u>**

1. Clone the repository

    ``` sh
    git clone  https://github.com/Revo1999/cds-vis.git
    ```
<br><br>


2. Change directory into the assignment2 directory <br>
    ``` sh
    cd assignment2
    ```
    <br><br>

3. Setup virtual environment containing the packages needed to run both programs. <br>
    ``` sh
    bash createVEnv.sh
    ```
    You can also install them globally in your environment use ```pip install -r requirements.txt``` while in assignment2 folder
<br><br>

4. Runs **lr.py** & **mlp.py** by activating the virtual environment, executing programs and closing the environment again.<br>
    ``` sh
    bash run.sh
    ``` 
<br>
<br>
<br>

5. **Only if you want to run the programs individually**, execute this line by line in console:
``` sh
# Accessing virtual environment
source assignment2_venv/bin/activate

# Runs the code
python src/TheNameOfThePythonFile.py

# Exits environment
deactivate
```
## Compatibility & Other Uses

Both programs are written with a specific task at hand, in terms of handling specifically the CIFAR-10 dataset. It might be useful as a guide-line for similar projects, in terms of setting up sci-kit learns MLP and Logistic Regression models, or how to use the CIFAR-10 dataset. With other datasets the program will need quite a bit to be rewritten. <br> <br>

## Outputs

### MLP Results - access [here](https://github.com/Revo1999/cds-vis/blob/main/assignment2/out/neural.txt)

|             |   precision |   recall | f1-score  | support|
|-------------|-------------|----------|-----------|-------|
|   airplane  |   0.39      |   0.40   |    0.40   |   1000|
| automobile  |    0.44     |   0.32   |   0.37    |   1000|
|      bird   |   0.31      |   0.37   |    0.33   |   1000|
|   cat       |    0.25     |   0.21   |   0.23    |   1000|
|  deer       |   0.27      |  0.25   |   0.26    |   1000|
|    dog      |   0.36      |   0.33   |    0.35   |   1000|
|   frog      |   0.32      |   0.35   |    0.33   |   1000|
|  horse      |   0.41      |   0.43   |    0.42   |   1000|
|    ship     |   0.46      |   0.45   |   0.46    |   1000|
|   truck     |   0.36      |    0.44  |    0.40   |   1000|
|-|
|  accuracy    |          |          |   0.35   |  10000|
| macro avg   |    0.36   |   0.35   |   0.35   |  10000|
|weighted avg    |   0.36    |  0.35  |    0.35   |  10000|

The model shows quite a balanced performance in the sense that it performs rather poorly at all categories. Images of ships, airplanes & horses perform a bit better than the rest (looking at F1-scores). Ships and airplanes might perform better because of they typically are easier to distinguish. ships because they are a larger shape located in water, and planes against the sky.

With an overall F1-score it can be said that this model is not performing very well, in terms of being useful. Further tweaking and testing for the parameters which the model use, might improve performance, but to make a model which sits at a more acceptable F1-score, 0.70 or higher, more complex models are needed.

![MLP training loss curve](out/neural_loss_curve.png?raw=true)

Plotting the loss curve for the MLP model shows a steady decline in loss. The program is running with ```early_stopping=True``` to prevent overfitting. This has resulted in the model stopping at approximately the 16 iteration. Since the curve is not completely stopped there might a little performance gain, still left in the model, but early stopping is in place also not to keep training for a too minimal gain.

### Logistic Results - access [here](https://github.com/Revo1999/cds-vis/blob/main/assignment2/out/logistic.txt)
|             |   precision |   recall | f1-score  | support|
|-------------|-------------|----------|-----------|-------|
|   airplane  |   0.31      |   0.34   |    0.32   |   1000|
| automobile  |    0.27     |   0.30   |   0.29    |   1000|
|      bird   |   0.25      |   0.19   |    0.22   |   1000|
|   cat       |    0.18     |   0.13   |   0.15    |   1000|
|  deer       |   0.20      |  0.18    |   0.19    |   1000|
|    dog      |   0.28      |   0.27   |    0.27   |   1000|
|   frog      |   0.23      |   0.21   |    0.22   |   1000|
|  horse      |   0.27      |   0.28   |    0.28   |   1000|
|    ship     |   0.30      |   0.35   |   0.33    |   1000|
|   truck     |   0.31      |    0.42  |    0.36   |   1000|
|-|
|  accuracy    |          |          |   0.27   |  10000|
| macro avg   |    0.26   |   0.27   |   0.26   |  10000|
|weighted avg    |   0.26    |  0.27  |    0.26   |  10000|

Sci-kit learns Logistic regression model does not perform well having an F1-score(a metric taking precision and recall into acount) of 0.26, this also applies to the precision. Logistical Regression is trying to handle images in a linear manner. Images on the other hand appear not linear, therefore it might be hard for the model to understand the relationship between pixels in the image. Like the MLP-model ship, airplane seem to perform well, i attribute the same reason, as explained earlier to why this is happening.

## Limitations & possible improvements

The clear limitations of the programs are the models used. Both MLP and Logistic Regression have difficulties handling the complex nature of images. Convolutional neural networks such as VGG16 are better suited for image processing. Also both MLP and Logistic Regression models are models which are not finely tuned for the task of analyzing images, here again VGG16 would be a better option.

Better preprocessing practices might improve performance quite a bit (for example slightly rotating images), and create a more robust models.