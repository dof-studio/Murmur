# Project whispertxt
# src/setup
# Version 0.0.1 built 240821
# DOF Studio, 2024

# Import libraries
import os
import sys
from cx_Freeze import setup, Executable

# Set recursion limit
sys.setrecursionlimit(4500)

# Entrypoint

# 1. Create a setup.py file in the root directory of your project.
setup(
    name="Murmur",
    version="0.0.1",
    description="Murmur - captures your voice",
    executables=[Executable(os.path.dirname(os.path.abspath(__file__)) + "\\" + "pipeline.py")],
)

# 2. Execute python setup.py build