import os
from PIL import Image

def process_images(image_directory, new_image_size, canvas_size, output_directory):
    image_files = sorted(
        [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))],
        key=lambda x: os.path.getmtime(os.path.join(image_directory, x)),
        reverse=False
    )

    # Determine the number of images
    num_images = len(image_files)
    
    # Calculate the space that will be occupied by all images
    images_total_height = new_image_size[1] * num_images
    
    # Calculate the remaining space on the canvas after the images are placed
    remaining_space = canvas_size[1] - images_total_height
    
    # Calculate the spacing between the images
    if num_images > 1:
        spacing = remaining_space // (num_images - 1)
    else:
        spacing = 0  # If there is only one image, it will be centered on the canvas

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Process each image
    for i, image_filename in enumerate(image_files):
        # Open and resize the image
        image_path = os.path.join(image_directory, image_filename)
        image = Image.open(image_path).resize(new_image_size, Image.ANTIALIAS)
        
        # Create a new canvas with a transparent background
        canvas = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
        
        # Calculate the position where the image will be placed on the canvas
        top_position = i * (new_image_size[1] + spacing)
        
        # Paste the resized image onto the canvas at the calculated position
        canvas.paste(image, (0, top_position), image if image.mode == 'RGBA' else None)
        
        #remove all punctuation from image_filename
        image_filename = image_filename.replace(" ", "_")

        #replace all characters that are not alphanumeric or underscore with nothing
        image_filename = ''.join(e for e in image_filename if e.isalnum() or e == '_')

        #remove all characters more than 50 characters
        image_filename = image_filename[:50]

        #add .png to the end of the image_filename
        image_filename = image_filename + ".png"

        # Save the new image with transparent background
        new_image_path = os.path.join(output_directory, image_filename)
        canvas.save(new_image_path, format='PNG')

        minutes_ago = num_images - i
        #change the modified time of the new image to be minutes_ago
        os.utime(new_image_path, (os.path.getatime(new_image_path), os.path.getmtime(new_image_path) - (minutes_ago * 60)))

    print(f"Processed {num_images} images. They are saved in the '{output_directory}' directory.")

# Set the directories
input_dir = 'input_images/' # The directory where the original images are located
output_dir = 'output_images/' # The directory where the processed images will be saved

# Call the function
process_images(input_dir, (1440, 1440), (1440, 3088), output_dir)
#process_images(input_dir, (1024, 1024), (1440, 3088), output_dir)
