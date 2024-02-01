from diffusers import DiffusionPipeline
import torch
from torchvision.utils import save_image
from torchvision import transforms

import json
from urllib import request, parse
import random
import subprocess
import time
import os

home_directory = os.path.expanduser('~')

def generate_images_XL(prompt, num_images=2, batch_size=1):
    # Optimizing CUDA operations
    torch.backends.cudnn.benchmark = True
    pipe = DiffusionPipeline.from_pretrained("/home/lunkwill/.cache/huggingface/hub/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/462165984030d82259a11f4367a4eed129e94a7b", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
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
            filename = filename.replace("\n", "_")
            filename = filename.replace(",", "_")
            filename = filename.replace("/", "_")
            filename = filename.replace("\\", "_")
            # Save each tensor to a file
            save_image(tensor, home_directory + f"/projects/dreamdrawer/output_images/{filename}")

        # Clear CUDA cache
        torch.cuda.empty_cache()

def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    print("req", req)
    server_process = None
    try:
        print("try")
        request.urlopen(req)
        #server_process = "try"
    except:
        print("except")
        # Replace 'path_to_script' with the actual path to your server script
        server_process = subprocess.Popen(["python", "/home/lunkwill/projects/ComfyUI/main.py"])
        # Wait for the server to start
        time.sleep(10)  # Adjust this value as needed
        # Retry sending the request
        request.urlopen(req)
    #time.sleep(5)
    # Monitor the output directory
    output_dir = home_directory + "/projects/ComfyUI/output"
    files_before = os.listdir(output_dir)
    print("files_before", str(len(files_before)))
    while True:
        
        files_after = os.listdir(output_dir)
        print("files_after", str(len(files_after)))
        if len(files_after) > len(files_before):
            break
        time.sleep(1)  # Check every second


def generate_images_XL_turbo(incoming_text):
    prompt = incoming_text
    # read workflow api data from file and convert it into dictionary 
    # assign to var prompt_workflow
    prompt_workflow = json.load(open('/home/lunkwill/projects/dreamdrawer/XL_turbo_api.json'))

    # create a list of prompts
    prompt_list = []
    prompt_list.append(prompt)

    prompt_pos_node = prompt_workflow["6"]
    # empty_latent_img_node = prompt_workflow["5"]
    SamplerCustom_node = prompt_workflow["13"]
    save_image_node = prompt_workflow["27"]

    filepaths = []
    # for every prompt in prompt_list...
    for index, prompt in enumerate(prompt_list):
        # set the text prompt for positive CLIPTextEncode node
        prompt_pos_node["inputs"]["text"] = prompt
        seed = random.randint(1, 18446744073709551614)
        # set a random seed in KSampler node 
        SamplerCustom_node["inputs"]["noice_seed"] = seed

        # set filename prefix to be the same as prompt
        # (truncate to first 100 chars if necessary)
        fileprefix = prompt.replace(" ", "_")
        if len(fileprefix) > 80:
            fileprefix = fileprefix[:80].replace(" ", "_")
            fileprefix = fileprefix.replace("\n", "_")
        print("fileprefix", fileprefix)
        save_image_node["inputs"]["filename_prefix"] = fileprefix
        #make a random number
        filepaths.append("/home/lunkwill/projects/ComfyUI/output/"+fileprefix+"_"+str(seed)+".png")

    # everything set, add entire workflow to queue.
    queue_prompt(prompt_workflow)

    #return filepaths

#generate_images_XL_turbo("a guy walks into a coffee shop. he orders a coffee. he sits down at a table. he drinks his coffee. he leaves the coffee shop.")