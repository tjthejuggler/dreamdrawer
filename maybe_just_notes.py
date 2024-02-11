from auto1111sdk import StableDiffusionPipeline

pipe = StableDiffusionPipeline("<Path to your local safetensors or checkpoint file>")

prompt = "a picture of a brown dog"
output = pipe.generate_txt2img(prompt = prompt, height = 1024, width = 768, steps = 10)

output[0].save("image.png")