'''
Assignment 2
    Victor Rasmussen
        Visual Analytics, Aarhus University
            17-05-2024
'''

import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import cifar10
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from tqdm import tqdm


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

def loss_curve_plotter(classifier, plot_save_path):
    plt.figure(figsize=(10, 5))
    plt.plot(classifier.loss_curve_, label='Training Loss')
    plt.title('Loss Curve')
    plt.xlabel('Iterations')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(plot_save_path)

def main():
    shuffle_seed = 100

    (X_train, y_train), (X_test, y_test) = cifar10.load_data()

    cifar10_label_names = [ 'airplane', 'automobile', 'bird', 'cat', 'deer','dog', 'frog', 'horse', 'ship', 'truck']

    X_train_processed = img_processor(X_train)
    X_test_processed = img_processor(X_test)
    y_train_processed = y_train.flatten()
    y_test_processed = y_test.flatten()


    print("Fitting... this might take a while")
    clf =  MLPClassifier(hidden_layer_sizes = (128,), max_iter=1000, random_state = 1964, early_stopping=True, verbose=True).fit(X_train_processed, y_train_processed)

    y_pred = clf.predict(X_test_processed)

    with open("../out/neural.txt", "w") as file:
            file.write(classification_report(y_test_processed, y_pred, target_names=cifar10_label_names))

    plot_save_path = "../out/neural_loss_curve.png"

    loss_curve_plotter(clf, plot_save_path)

    print("Classification report saved!")


if __name__ == "__main__":
    main()
