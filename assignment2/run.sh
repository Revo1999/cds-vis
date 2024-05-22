#!/usr/bin/bash

# activate the environment
source assignment2_venv/bin/activate

# run the code
python src/lr.py
python src/mlp.py

# close the environment
deactivate