'''
Assignment 2
    Victor Rasmussen
        Visual Analytics, Aarhus University
            17-05-2024
'''

import numpy as np
import cv2
from tqdm import tqdm
import os

from tensorflow.keras.datasets import cifar10
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def img_normalize(image):
    normalized_image = cv2.normalize(image, None, 0, 1.0, cv2.NORM_MINMAX)
    return normalized_image

def img_grey(image):
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grey_img

def img_processor(image_variable):
    images_output = []
    
    #Note i normalize before greyscaling thinking it's more computational power, but more information get normalized since the normalization have 3 channels to normalize.
    #Though im not completely sure this is regarded as good practice?
    
    for image in tqdm(image_variable, colour='green',desc='Normalising and converting to greyscale'):
        images_output.append(img_grey(img_normalize(image)))

    return np.array(images_output).reshape(-1, 1024)



def main():
    shuffle_seed = 100

    (X_train, y_train), (X_test, y_test) = cifar10.load_data()

    cifar10_label_names = [ 'airplane', 'automobile', 'bird', 'cat', 'deer','dog', 'frog', 'horse', 'ship', 'truck']

    X_train_processed = img_processor(X_train)
    X_test_processed = img_processor(X_test)
    y_train_processed = y_train.flatten()
    y_test_processed = y_test.flatten()

    clf = LogisticRegression(random_state=shuffle_seed).fit(X_train_processed, y_train_processed)

    print("Fitting... this might take a while")

    y_pred = clf.predict(X_test_processed)

    with open("../out/logistic.txt", "w") as file:
            file.write(classification_report(y_test_processed, y_pred, target_names=cifar10_label_names))

    print("Classification report saved!")



if __name__ == "__main__":
    main()
