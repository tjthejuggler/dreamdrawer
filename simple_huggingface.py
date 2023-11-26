from diffusers import DiffusionPipeline
import torch
from torchvision.utils import save_image
from torchvision import transforms

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
pipe.to("cuda")

prompt = "An astronaut riding a red horse"

image = pipe(prompt=prompt).images[0]

# Convert the PIL Image to a PyTorch tensor
transform = transforms.ToTensor()
tensor = transform(image)

# Save the tensor to a file
save_image(tensor, 'generated_image2.png')
