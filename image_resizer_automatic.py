import os
import sys
from PIL import Image
from datetime import date

def process_images(image_paths, canvas_width, canvas_height, output_directory, originals_backed_up_dir):
    # Sort the images by their last modified time
    image_paths_sorted = sorted(
        image_paths,
        key=lambda x: os.path.getmtime(x),
        reverse=False
    )

    #get todays date in this format yyyy-mm-dd
    
    today = date.today()

    #full output directory path is output_directory/today
    output_directory = os.path.join(output_directory, str(today))

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    num_images = len(image_paths_sorted)

    # Calculate the total height that all images will occupy and the remaining space
    total_image_height = 0
    for image_path in image_paths_sorted:
        with Image.open(image_path) as img:
            original_width, original_height = img.size
            if original_width == original_height:
                total_image_height += canvas_width  # For square images
            else:
                aspect_ratio = original_height / original_width
                total_image_height += int(canvas_width * aspect_ratio)  # For non-square images

    remaining_space = canvas_height - total_image_height

    # Calculate spacing between images
    if num_images > 1:
        spacing = remaining_space // (num_images - 1)
    else:
        spacing = 0  # Center the image if only one

    # Process each image
    for i, image_path in enumerate(image_paths_sorted):
        # Open the image
        image = Image.open(image_path)

        # Resize square and non-square images
        original_width, original_height = image.size
        if original_width == original_height:
            image = image.resize((canvas_width, canvas_width), Image.ANTIALIAS)
        else:
            aspect_ratio = original_height / original_width
            new_height = int(canvas_width * aspect_ratio)
            image = image.resize((canvas_width, new_height), Image.ANTIALIAS)

        # Calculate the top position for each image, including spacing
        top_position = sum([canvas_width + spacing for _ in range(i)]) if original_width == original_height else sum([int(canvas_width * (original_height / original_width)) + spacing for _ in range(i)])

        # Adjust top_position if the image goes beyond the bottom of the canvas
        if top_position + image.height > canvas_height:
            top_position = canvas_height - image.height

        # Create a new canvas with a transparent background
        canvas = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))

        # Paste the resized image onto the canvas
        canvas.paste(image, (0, top_position), image if image.mode == 'RGBA' else None)
        
        # Prepare the image filename
        image_filename = os.path.basename(image_path)
        image_filename = image_filename.replace(" ", "_")
        image_filename = ''.join(e for e in image_filename if e.isalnum() or e == '_')
        image_filename = image_filename[:50]
        image_filename = image_filename + ".png"

        # Save the new image with a transparent background
        new_image_path = os.path.join(output_directory, image_filename)
        canvas.save(new_image_path, format='PNG')

        # Adjust the modified time of the new image
        minutes_ago = num_images - i
        os.utime(new_image_path, (os.path.getatime(new_image_path), os.path.getmtime(new_image_path) - (minutes_ago * 60)))

        # Backup the original image
        if originals_backed_up_dir:
            if not os.path.exists(originals_backed_up_dir):
                os.makedirs(originals_backed_up_dir)
            os.rename(image_path, os.path.join(originals_backed_up_dir, os.path.basename(new_image_path)))

        #delete the original image
        #os.remove(image_path)


    print(f"Processed {num_images} images. They are saved in the '{output_directory}' directory.")

if __name__ == "__main__":
    # Set the output directory and sizes
    
    home_directory = os.path.expanduser('~')

    #output_dir = '~/Pictures/Wallpapers/drmz'  # The directory where the processed images will be saved
    output_dir = os.path.join(home_directory, 'Pictures', 'Wallpapers', 'drmz')
    #originals_backed_up_dir = '~/Pictures/Wallpapers/originals'  # The directory where the original images will be backed up
    originals_backed_up_dir = os.path.join(home_directory, 'Pictures', 'Wallpapers', 'originals')
    canvas_width = 1440  # Width of the canvas
    canvas_height = 3088  # Height of the canvas

    # Collect image paths from the command line arguments
    image_paths = sys.argv[1:]

    # Call the function to process images
    process_images(image_paths, canvas_width, canvas_height, output_dir, originals_backed_up_dir)
