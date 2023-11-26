import os
import shutil
from datetime import datetime


# Get the home directory of the current user
home_directory = os.path.expanduser('~')

# Join paths in a platform-independent way
directory = os.path.join(home_directory, 'Pictures', 'Wallpapers', 'drmz')


# Create a set to track which directories have been created
created_directories = set()

# Iterate through all files in the directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)

    # Skip directories
    if os.path.isdir(file_path):
        continue

    # Get the modified date of the file
    modified_time = os.path.getmtime(file_path)
    date = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d')

    # Create a new subdirectory for this date if it doesn't exist
    new_directory = os.path.join(directory, date)
    if date not in created_directories and not os.path.exists(new_directory):
        os.makedirs(new_directory)
        created_directories.add(date)

    # Move the file to the new directory
    shutil.move(file_path, new_directory)
