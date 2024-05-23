#!/usr/bin/bash

# activate the environment
source assignment4_venv/bin/activate

# run the code
cd src
python mtcnn_face_detection.py
cd ..

# close the environment
deactivate