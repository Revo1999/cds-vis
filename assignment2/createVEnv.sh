#!/usr/bin/bash


# create virtual env
python -m venv assignment2_venv
# activate env
source ./assignment2_venv/bin/activate
# install requirements
pip install -r requirements.txt
# close the environment

deactivate


echo Environment is all set up!




