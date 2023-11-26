import os

# Get the home directory of the current user
home_directory = os.path.expanduser('~')

def rename_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('png'):
            new_filename = filename[:-3] + '.png'  # remove the last 3 characters (png) and add .png
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

#rename_files('~/Pictures/Wallpapers/mon')
rename_files(os.path.join(home_directory, 'Pictures', 'Wallpapers', 'mon'))