#!/bin/bash

# Exit on error
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Building executable..."
# --onefile: Create a single executable
# --name: Name of the output binary
# --clean: Clean PyInstaller cache before building
pyinstaller --onefile --name mpeg2gif --clean --copy-metadata imageio main.py

echo "Build complete! The binary is located in dist/mpeg2gif"
