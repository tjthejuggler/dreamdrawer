#!/bin/bash

source /home/lunkwill/miniconda3/etc/profile.d/conda.sh  # Replace with the path to your conda.sh
conda activate base

# Read from clipboard
clipboard_content=$(xclip -o)

# Define the path to your Python script
# If your .sh script is in the same directory as your Python script, you can use:
# script_path="./main.py"
# Otherwise, use the absolute path with $HOME
script_path="$HOME/projects/dreamdrawer/generate_prompts_after_crash.py"

# Run the Python script with the clipboard content as an argument
python "$script_path" "$clipboard_content"
