#!/usr/bin/bash

# activate the environment
source assignment1_venv/bin/activate

# run the code
cd src
python nearest_neighbor.py
python open_cv_compare_hist.py
cd ..

# close the environment
deactivate