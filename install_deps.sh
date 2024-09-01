#!/bin/bash

# Ensure Homebrew is installed
if ! command -v brew &> /dev/null
then
    echo "Homebrew not found. Please install Homebrew first from https://brew.sh/"
    exit 1
fi

# Update Homebrew and install necessary tools
echo "Updating Homebrew..."
brew update

# Install exiftool and ffmpeg
echo "Installing exiftool and ffmpeg..."
brew install exiftool ffmpeg

# Function to install Python packages
install_python_packages() {
    echo "Installing Python packages with pip..."
    pip install pillow moviepy exifread pyheif tifffile

    if [ $? -ne 0 ]; then
        echo "pip installation failed. Trying pip3..."
        pip3 install pillow moviepy exifread pyheif tifffile
    fi
}

# Install Python packages
install_python_packages

echo "All dependencies have been installed."