# Importing PyTorch library
import torch

# Importing StableDiffusionPipeline to use pre-trained Stable Diffusion models
from diffusers import StableDiffusionPipeline

# Image is a class for the PIL module to visualize images in a Python Notebook
from PIL import Image
import os

# Get the home directory of the current user
home_directory = os.path.expanduser('~')

# Creating pipeline
pipeline = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",
                                                  torch_dtype=torch.float16)

# Specify the path to your model file
#model_path = "~/projects/ComfyUI/models/checkpoints"
model_path = os.path.join(home_directory, 'projects', 'ComfyUI', 'models', 'checkpoints')

# Load the model's state dictionary from the local file
model_state_dict = torch.load(model_path)

# Update the pipeline's model with the loaded state dictionary
pipeline.model.load_state_dict(model_state_dict)

# Defining function for the creation of a grid of images
def image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols
    
    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    
    return grid

# Moving pipeline to GPU
pipeline = pipeline.to('cuda')

n_images = 6  # Let's generate 6 images based on the prompt below
prompt = ['Sunset on a beach'] * n_images

images = pipeline(prompt).images

grid = image_grid(images, rows=2, cols=3)
grid
