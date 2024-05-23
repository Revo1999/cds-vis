#!/usr/bin/bash

# Ask the user a question
echo "What would you like to run? Example: nearest_neighbor.py -I image_0001.jpg"

# Read the user's response
read run_this

# activate the environment
source assignment1_venv/bin/activate

# run the code
cd src
python $run_this
cd ..

# close the environment
deactivate