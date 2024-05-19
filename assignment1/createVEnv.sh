#!/usr/bin/bash


# create virtual env
python -m venv assignment1_venv
# activate env
source ./assignment1_venv/bin/activate
# install requirements
pip install -r requirements.txt
# close the environment

deactivate


echo Environment is all set up!




