from diffusers import DiffusionPipeline
import torch
from torchvision.utils import save_image
from torchvision import transforms

def generate_images(prompt, num_images=8, batch_size=2):
    # Optimizing CUDA operations
    torch.backends.cudnn.benchmark = True

    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
    pipe.to("cuda")

    for batch_start in range(0, num_images, batch_size):
        batch_end = min(batch_start + batch_size, num_images)
        batch_prompts = [prompt] * (batch_end - batch_start)
        images = pipe(prompt=batch_prompts, num_inference_steps=30).images

        for i, image in enumerate(images, start=batch_start):
            # Convert the PIL Image to a PyTorch tensor
            transform = transforms.ToTensor()
            tensor = transform(image)

            # Create a truncated filename for each image
            filename = f"{prompt[:50].replace(' ', '_')}_{i}_{batch_start}.png"

            # Save each tensor to a file
            save_image(tensor, f"./output_images/{filename}")

        # Clear CUDA cache
        torch.cuda.empty_cache()

generate_images("A strange little man huddled in the corder with toothpicks")
