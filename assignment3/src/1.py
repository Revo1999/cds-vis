import os
import vrashelper as vh # A small package containing a work_here and console text definitions i use often
import glob
import sys
from tqdm import tqdm as tqdm_bar #Renaming tqdm avoids an error (is used in other packages)
import tensorflow as tf
import gc

from tensorflow.keras.applications.vgg16 import (preprocess_input,
                                                 decode_predictions,
                                                 VGG16)

# layers
from tensorflow.keras.layers import (Flatten, 
                                     Dense, 
                                     Dropout, 
                                     BatchNormalization)
# generic model object
from tensorflow.keras.models import Model

# optimizers
from tensorflow.keras.optimizers.schedules import ExponentialDecay
from tensorflow.keras.optimizers import SGD, Adam

from tensorflow.keras.preprocessing.image import (load_img, #Needs pillow, therefore in requirements.txt
                                                  img_to_array,
                                                  ImageDataGenerator)
#scikit-learn
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# for plotting
import numpy as np
import matplotlib.pyplot as plt


def list_files(directory):
    folders = os.listdir(directory)

    all_files = []
    for root, dirs, files in os.walk(directory_path, topdown=True):
        for filenames in files:
            all_files.append(os.path.join(root, filenames))

    return all_files


def check_files(file_list, wanted_filetype):
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
    inp = input("[Y]/[N]\n")
    if inp.lower() == "y" or inp.lower() == "yes":
        return True
    elif inp.lower() == "n" or inp.lower() == "no":
        return False
    else:
        print (vh.ctext.remove_line) #Removes last input line from console
        print(vh.colorbank.error_red + "\nwrong input!" + vh.colorbank.default)
        take_input()
          

def create_labels_list(directory):
    folders = os.listdir(directory)
    return folders

def image_loader(image_paths_to_proces, folder_step):
    #loading image and resizing
    images_list = [load_img(img_path, target_size=(224, 224)) for img_path in tqdm_bar(image_paths_to_proces, desc="Loading images", colour = 'green')]
    print(vh.ctext.nline) #new line
    #converting images to np.array object
    images_list = [img_to_array(image) for image in tqdm_bar(images_list, desc="Converting images to numpy-arrays", colour = 'green')]
    print(vh.ctext.nline) #new line
    #subtracting the mean RGB value
    image_list = [preprocess_input(image) for image in tqdm_bar(images_list, desc="Subtracting the mean RGB value", colour = 'green')]
    print(vh.ctext.nline) #new line

    #Needs to be numpy array/tensor "str" is incompatible type
    labels_list = [image_path.split("/")[folder_step] for image_path in image_paths_to_proces]
    return images_list, labels_list

def load_vgg16():
    # loading the model
    print(vh.colorbank.blue + "Loading/Downloading VGG16 model" + vh.colorbank.default)
    model = VGG16(include_top=False, 
              pooling='avg',
              input_shape=(224, 224, 3))

    # mark loaded layers as not trainable
    for layer in model.layers:
        layer.trainable = False

    # add new classifier layers
    flat1 = Flatten()(model.layers[-1].output)
    class1 = Dense(128, activation='relu')(flat1)
    output = Dense(10, activation='softmax')(class1)

    # define new model
    model = Model(inputs=model.inputs, 
                outputs=output)

    print(vh.colorbank.hackergreen + "Model loaded" + vh.colorbank.default)
    return model

def plot_history(H, epochs):
    plt.figure(figsize=(12,6))
    plt.subplot(1,2,1)
    plt.plot(np.arange(0, epochs), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, epochs), H.history["val_loss"], label="val_loss", linestyle=":")
    plt.title("Loss curve")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.tight_layout()
    plt.legend()

    plt.subplot(1,2,2)
    plt.plot(np.arange(0, epochs), H.history["accuracy"], label="train_acc")
    plt.plot(np.arange(0, epochs), H.history["val_accuracy"], label="val_acc", linestyle=":")
    plt.title("Accuracy curve")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.tight_layout()
    plt.legend()
    plt.show()
    plt.savefig('../out/Figure2')

vh.work_here()

directory = ["..", "in", "Tobacco3482"]
directory_path = os.path.join(*directory)
step = len(directory)

#Goes through files and check file-type and prompts user to remove --- creates a list of files to be processed
files_to_proces = check_files(file_list=list_files(directory_path), wanted_filetype=".jpg")
labels = create_labels_list(directory_path)
print(f"Labels (from folder structure): {labels}")

# X = the processed images, y = the labels 
X, y = image_loader(files_to_proces, folder_step=step)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#The dataset copy is garbage collected
del X, y
gc.collect()

X_train = np.array(X_train)
X_test = np.array(X_test)

lb = LabelBinarizer()
y_train = lb.fit_transform(y_train)
y_test = lb.fit_transform(y_test)

print(X_train.shape)

model = load_vgg16()

lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate=0.01,
    decay_steps=10000,
    decay_rate=0.9)
sgd = SGD(learning_rate=lr_schedule)
model.compile(optimizer=sgd,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# summarize
model.summary()


#train
H = model.fit(X_train, y_train, 
            validation_split=0.1,
            batch_size=128,
            epochs=10,
            verbose=1)


plot_history(H, 10)

predictions = model.predict(X_test, batch_size=128)

print(classification_report(y_test.argmax(axis=1),
                            predictions.argmax(axis=1),
                            target_names=labels))

with open("../out/report3.txt", "w") as file:
        file.write(classification_report(y_test.argmax(axis=1),
                            predictions.argmax(axis=1),
                            target_names=labels))

print("Classification report saved!")



print("saving model")
model.save('../model/model2.h5')
print("model saved")


'''

def create_directory_overlook_df(directory):
    folders = os.listdir(directory)
    idx = 0

    for folder in folders:

        #Get files from a folder in a list
        files = os.listdir(os.path.join(directory, folder))

        if idx == 0:
            #Creates initial dataframe which can be concatted later
            df = pl.DataFrame({folder: files})
        else:
            #Create dataframe with columns name = folder and files in values
            df_add = pl.DataFrame({folder: files})
            df = pl.concat([df, df_add], how="horizontal")
        
        idx += 1

    return df

'''