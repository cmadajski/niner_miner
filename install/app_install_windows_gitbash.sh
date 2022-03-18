#!/bin/sh
# create virtual environment
python -m venv ../env
echo "* python virtual environment created *"
# activate virtual environment
source ../env/Scripts/activate
echo "* python virtual environment activated *"
# install dependencies
pip install -r requirements.txt
echo "* dependencies installed *"
# set up initial database
cd ../src/
python setup_db.py
echo "* database initialized *"
# process complete
echo "* initial setup process completed *"