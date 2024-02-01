import telegram_service
import ComfyUI_image_gen

#load the prompts from a file
with open ("/home/lunkwill/projects/dreamdrawer/processed_sd_prompts.txt", "r") as f:
    processed_sd_prompts = f.read().splitlines()
print("PROCESSED_SD_PROMPTS:\n\n")
print("\n".join(processed_sd_prompts))
prompts_printed = 0
for processed_sd_prompt in processed_sd_prompts:
    print(str(prompts_printed) + "/" + str(len(processed_sd_prompts)))
    print(processed_sd_prompt)
    ComfyUI_image_gen.generate_images_XL(processed_sd_prompt)
    prompts_printed += 1
    #ComfyUI_image_gen.generate_images_XL_turbo(sd_prompt)

#this is only for XL_turbo - but why? shouldnt it also be for XL?
#subprocess.run(["pkill", "-f", "/home/lunkwill/projects/ComfyUI/main.py"], check=True)

telegram_service.send_telegram_text_as_me_to_bot("Finished generating dr. images")