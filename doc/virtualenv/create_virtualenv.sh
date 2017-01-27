#!/bin/bash

echo "Deleting and creating venv/ folder..."
rm -rf venv/
mkdir venv/
touch venv/.stub

echo "Creating Python3 virtualenv at venv/"
virtualenv venv --python=python3

echo "Entering virtualenv..."
. venv/bin/activate

echo "Installing dependencies..."
pip install -r doc/virtualenv/requirements.txt

