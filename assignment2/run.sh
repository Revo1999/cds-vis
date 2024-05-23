#!/usr/bin/bash

# activate the environment
source assignment2_venv/bin/activate

# run the code
cd src
python lr.py
python mlp.py
cd ..

# close the environment
deactivate