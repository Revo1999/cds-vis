#!/usr/bin/bash

# activate the environment
source assignment3_venv/bin/activate

cd src/

# run the code
python document_classifier.py

cd ..
# close the environment
deactivate