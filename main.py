import subprocess
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from pprint import pprint
import re
from diffusers import DiffusionPipeline
import torch
from torchvision.utils import save_image
from torchvision import transforms
import sys
import json
import os
from ask_local_llm import send_prompt_to_llm
import time

import LMstudio_RPA

# Get the home directory of the current user
home_directory = os.path.expanduser('~')

story = sys.argv[1]

print("story", story)
# With the current setup it just uses whatver story is in the clipboard when main.py is run, but you can also just put it in as a string for story
# story = "A guy walks into a coffee shop. He orders a coffee. He sits down at a table. He drinks his coffee. He leaves the coffee shop."

#load SD_system_prompt from file
# with open("~/projects/dreamdrawer/system_prompts/SD_system_prompt.txt", "r") as f:
#     SD_system_prompt = f.read()

with open(home_directory + "/projects/dreamdrawer/system_prompts/SD_system_prompt.txt", "r") as f:
    SD_system_prompt = f.read()

def check_if_first_person_pronoun(sentence):
    first_person_pronouns = ['i', 'i\'m', 'me', 'we', 'us', 'my', 'mine', 'our', 'ours']
    sentence = sentence.lower()
    for pronoun in first_person_pronouns:
        if pronoun in sentence.split():
            return True
    return False

def me_swapped_intelligently(sentence):
    #with open ("~/projects/dreamdrawer/system_prompts/me_swapped_prompt.txt", "r") as f:
    #    system_prompt = f.read()
    with open (home_directory + "/projects/dreamdrawer/system_prompts/me_swapped_prompt.txt", "r") as f:
        system_prompt = f.read()
    
    #story_context = f"Story: {story}\nCharacter Descriptions: {name_rules}\nPhrases: {phrases}"
    return send_prompt_to_llm(sentence, system_prompt)

def automated_name_swapping(sentence):
    print('sentence',sentence)
    # with open ("~/projects/dreamdrawer/system_prompts/my_replacements_dict.json", "r") as f:
    #     replacements = json.load(f)
    with open (home_directory + "/projects/dreamdrawer/my_replacements_dict.json", "r") as f:
        replacements = json.load(f)
    sentence = sentence.lower()
    for name, description in replacements.items():
        sentence = sentence.replace(name, description)
    return sentence

def format_llm_output_as_list(llm_output):
    try:
        # Explicitly convert llm_output to string
        llm_output_str = str(llm_output)

        # Remove square brackets and split by commas not inside quotes
        cleaned_output = re.sub(r'\[|\]', '', llm_output_str)
        potential_list_items = re.split(r',\s*(?![^"]*\"\,)', cleaned_output)

        # Trim whitespace and remove any empty strings
        list_items = [item.strip() for item in potential_list_items if item.strip()]
        return list_items
    except Exception as e:
        # Handle any exception (log it if necessary)
        print(f"Error processing LLM output: {e}")
        return []  # Return an empty list or some default value

def replace_pronouns_based_on_context(sentence, story):
    system_prompt = "You are an expert editor. You follow directions exactly. You only ever say a single sentence. You Receive a story and a sentence. You replace pronouns in the sentence with any relevant specifics from the story."
    combined_sentence = 'Story:\n' + story + '\n\nSentence to be edited: ' + sentence + '\n\nRespond only with a single sentence.'
    replace_pronouns_based_on_context_sentence = send_prompt_to_llm(combined_sentence, system_prompt)
    print("Original sentence:\n", sentence,"\nReplaced pronouns response:\n", replace_pronouns_based_on_context_sentence, "\n\n")
    return replace_pronouns_based_on_context_sentence

def story_board_creator_picture_description(sentence, story):
    system_prompt = "You are a creative scene creator. You follow directions exactly. You only ever say a single sentence. You are an artist. You receive a background story and a specific sentence and you respond with a visual description that portrays a single picture that could be taken of a scene from that specific sentence."
    combined_sentence = 'Background story:\n' + story + '\n\nSpecific Sentence: ' + sentence + '\n\nRespond only with a single sentence.'
    story_board_key_description = send_prompt_to_llm(combined_sentence, system_prompt)
    print("Original sentence:\n", sentence,"\nKey description response:\n", story_board_key_description, "\n\n")
    return story_board_key_description

def story_board_creator_key_description(sentence, story):
    system_prompt = "You are a creative story board creator. You follow directions exactly. You only ever say a single sentence. You are an artist. You receive a background story and a specific sentence and you respond with a visual description that encompases a key aspect of that specific sentence."
    combined_sentence = 'Background story:\n' + story + '\n\nSpecific Sentence: ' + sentence + '\n\nRespond only with a single sentence.'
    story_board_key_description = send_prompt_to_llm(combined_sentence, system_prompt)
    print("Original sentence:\n", sentence,"\nKey description response:\n", story_board_key_description, "\n\n")
    return story_board_key_description

def story_board_creator_important_object_description(sentence, story):
    system_prompt = "You are an image description creator. You follow directions exactly. You only ever say a single discription. You never write a complete sentence. You receive a background story and a specific sentence and you respond with a visual description of an important object that would be found in this scene."
    combined_sentence = 'Background story:\n' + story + '\n\nSpecific Sentence: ' + sentence + '\n\nRespond only with a single sentence.'
    story_board_minor_description = send_prompt_to_llm(combined_sentence, system_prompt)
    print("Original sentence:\n", sentence,"\Importnat object description response:\n", story_board_minor_description, "\n\n")
    return story_board_minor_description

def story_board_creator_minor_description(sentence, story):
    system_prompt = "You are an image description creator. You follow directions exactly. You only ever say a single discription. You never write a complete sentence. You receive a background story and a specific sentence and you respond with a visual description of a minor object that would be found in this scene."
    combined_sentence = 'Background story:\n' + story + '\n\nSpecific Sentence: ' + sentence + '\n\nRespond only with a single sentence.'
    story_board_minor_description = send_prompt_to_llm(combined_sentence, system_prompt)
    print("Original sentence:\n", sentence,"\nMinor object description response:\n", story_board_minor_description, "\n\n")
    return story_board_minor_description

def shorten_this_prompt(sentence):
    system_prompt = "You are a text editor. You follow directions exactly. You only ever say a single sentence. You receive some text and you respond with less than 350 characters."
    shortened_sentence = send_prompt_to_llm(sentence, system_prompt)
    print("Original sentence:\n", sentence,"\nShortened sentence:\n", shortened_sentence, "\n\n")
    return shortened_sentence

def process_description(sentence, swapped_sentences, description_function):
    description = description_function(sentence, ' '.join(swapped_sentences))
    if len(description) > 350:
        description = shorten_this_prompt(description)
    return(description + ",realistic color photograph")

def generate_images(prompt, num_images=4, batch_size=2):
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
            #save_image(tensor, f"~/projects/dreamdrawer/output_images/{filename}")
            save_image(tensor, home_directory + f"/projects/dreamdrawer/output_images/{filename}")

        # Clear CUDA cache
        torch.cuda.empty_cache()

# Redefining the function to split the string on commas outside of double quotes
def split_string_on_commas(input_string):
    # List to store the split strings
    result = []
    # Temporary string to store characters between commas
    temp_str = ""
    # Flag to track whether we are inside a double-quoted section
    inside_quotes = False

    for char in input_string:
        if char == '"':
            # Toggle the inside quotes flag
            inside_quotes = not inside_quotes
            # Add the quote to the temp string
            temp_str += char
        elif char == ',' and not inside_quotes:
            # If we find a comma and we're not inside quotes, add the temp string to the result
            # and reset the temp string
            result.append(temp_str.strip())
            temp_str = ""
        else:
            # Add the character to the temp string
            temp_str += char

    # Add the last temp string to the result if it's not empty
    if temp_str:
        result.append(temp_str.strip())

    return result

# Main pipeline function
def story_to_sd_prompts(story):
    # Start the LLM server
    LMstudio_RPA.start_server()
    
    #subprocess.Popen(["litellm", "--model", "ollama/mistral"])
    time.sleep(5)
    sentences = sent_tokenize(story)
    print("sentences:\n" + '\n'.join(sentences))
    swapped_sentences = []
    replaced_pronouns_sentences = []
    for sentence in sentences:
        if check_if_first_person_pronoun(sentence):
            sentence = me_swapped_intelligently(sentence)
        sentence = automated_name_swapping(sentence)
        swapped_sentences.append(sentence)
    for swapped_sentence in swapped_sentences:
        replaced_pronouns_sentences.append(replace_pronouns_based_on_context(swapped_sentence, ' '.join(swapped_sentences)))
    sd_prompts = []
    for replaced_pronouns_sentence in replaced_pronouns_sentences:        
        sd_prompts.append(process_description(replaced_pronouns_sentence, replaced_pronouns_sentences, story_board_creator_key_description))
        sd_prompts.append(process_description(replaced_pronouns_sentence, replaced_pronouns_sentences, story_board_creator_picture_description))
        #sd_prompts.append(process_description(replaced_pronouns_sentence, replaced_pronouns_sentences, story_board_creator_minor_description))
        sd_prompts.append(process_description(replaced_pronouns_sentence, replaced_pronouns_sentences, story_board_creator_important_object_description))

    #shut down llm server
    #subprocess.run(["pkill", "-f", "litellm"])
    LMstudio_RPA.stop_server()
    #prompts = story_to_sd_prompts(story)
    print("prompts", sd_prompts)
    for sd_prompt in sd_prompts:
        generate_images(sd_prompt)


story_to_sd_prompts(story)