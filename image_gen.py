# Import the necessary libraries
import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
import os

# Get the home directory of the current user
home_directory = os.path.expanduser('~')

model_id = "stabilityai/stable-diffusion-xl-base-1.0"
pipeline = StableDiffusionXLPipeline.from_pretrained(model_id)

# Set the random seed for reproducibility
torch.manual_seed(0)

# Specify the path to your model
#model_path = "~/projects/ComfyUI/models/checkpoints"
model_path = os.path.join(home_directory, 'projects', 'ComfyUI', 'models', 'checkpoints')

# Create an instance of the pipeline with the desired settings
pipe = StableDiffusionXLPipeline.from_pretrained(model_path, sampler="euler")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.generator = torch.Generator("cuda").manual_seed(0)
pipe.to("cuda")

# Generate images by passing prompts to the pipeline
prompts = ["A beautiful sunset over the ocean", "A cute puppy playing with a ball"]
images = []
for i, prompt in enumerate(prompts):
    image = pipe(prompt, generator=pipe.generator, num_inference_steps=20).images[0]
    image.save(f'result_{i}.jpg')
    images.append(image)
