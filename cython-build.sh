#!/bin/bash

# The simulation speed can be increased by using compiled classes.
# Cython generates and then compiles c files from py files.
# Cython uses some special annotations. Therefore we have the pyx files
# of the time critical classes. By using this script the classes will
# be compiled.

# Initialization:
# Step 1: Install Cython by entering "pip install Cython"
# Step 2: Replace "python3" below by the path to your Python installation if needed.

python3 setup.py build_ext --inplace