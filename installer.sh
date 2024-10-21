#!/bin/bash

# Define the virtual environment directory
VENV_DIR="myenv"

# Create the virtual environment
echo "Creating virtual environment: $VENV_DIR"
python3 -m venv $VENV_DIR

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Check if requirements.txt exists and install dependencies
if [[ -f "requirements.txt" ]]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

# Install tkinter (if not already installed)
echo "Installing tkinter and ttkbootstrap..."
pip install tk
pip install ttkbootstrap

echo "Installation completed. You can now use the virtual environment by running 'source $VENV_DIR/bin/activate'."
