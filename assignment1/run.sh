#!/usr/bin/bash

# activate the environment
source assignment1_venv/bin/activate

# run the code
python src/nearest_neighbor.py
python src/open_cv_compare_hist.py

# close the environment
deactivate