
















import subprocess
import nltk
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from pprint import pprint
import re
import sys
import json
import os
import time

from ask_local_llm import *
import telegram_service
import ComfyUI_image_gen

import ask_ollama

import kill_ollama
import getpass

def install_pydantic():
    subprocess.run(["pip", "install", "--upgrade", "pydantic"], check=True)
    print("installed pydantic")
install_pydantic()

# Get the home directory of the current user
home_directory = os.path.expanduser('~')

story = sys.argv[1]

print("story", story)
# With the current setup it just uses whatver story is in the clipboard when main.py is run, but you can also just put it in as a string for story
# story = "A guy walks into a coffee shop. He orders a coffee. He sits down at a table. He drinks his coffee. He leaves the coffee shop."

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

    return ask_ollama.llm_request(system_prompt, sentence)
    
    #story_context = f"Story: {story}\nCharacter Descriptions: {name_rules}\nPhrases: {phrases}"
    #return send_prompt_to_llm(sentence, system_prompt)

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

def send_prompt(sentence, story, system_prompt, response_label):
    combined_sentence = 'Background story:\n' + story + '\n\nSpecific Sentence: ' + sentence + '\n\nRespond only with a single sentence.'
    response = send_prompt_to_llm(combined_sentence, system_prompt)
    print("Original sentence:\n", sentence, f"\n{response_label} response:\n", response, "\n\n")
    #processed_response = process_description(response)
    return response

def shorten_this_prompt(sentence):
    system_prompt = "You are a text editor. You follow directions exactly. You only ever say a single sentence. You receive some text and you respond with less than 350 characters."
    shortened_sentence = send_prompt_to_llm(sentence, system_prompt)
    print("Original sentence:\n", sentence,"\n\nShortened sentence:\n", shortened_sentence, "\n\n")
    return shortened_sentence

def process_description(response):
    #description = description_function(sentence, ' '.join(swapped_sentences))
    if len(response) > 350:
        response = shorten_this_prompt(response)
    return(response + ",realistic color photograph")

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

def check_if_sentence_contains_pronouns(sentence):
    pronouns = ['i', 'i\'m', 'me', 'we', 'us', 'my', 'mine', 'our', 'ours', 'he', 'she', 'they', 'them', 'his', 'her', 'hers', 'their', 'theirs']
    sentence = sentence.lower()
    for pronoun in pronouns:
        if pronoun in sentence.split():
            return True
    return False

def check_and_start_service(service_name):
    # Check if the service is running
    result = subprocess.run(['systemctl', 'is-active', service_name], stdout=subprocess.PIPE)
    if result.stdout.decode('utf-8').strip() != 'active':
        # If the service is running, stop it
        subprocess.run(['sudo', 'systemctl', 'start', service_name])

# Main pipeline function
def story_to_sd_prompts(story):
    sudo_password = getpass.getpass("Enter sudo password: ")
    
    sentences = sent_tokenize(story)
    print("sentences:\n" + '\n'.join(sentences))

    # Comment this to let the copied in dream get turned into a json
    with open (home_directory + "/projects/dreamdrawer/json_descriptions20240211-134043.json", "r") as f:
        json_descriptions = f.read()

    if not json_descriptions:
        swapped_sentences = []
        #replaced_pronouns_sentences = []
        #connect_to_llm()
        for sentence in sentences:
            if check_if_first_person_pronoun(sentence):
                sentence = me_swapped_intelligently(sentence)
            sentence = automated_name_swapping(sentence)
            swapped_sentences.append(sentence)
        #combine swapped_sentences into a single string
        swapped_sentences = ' '.join(swapped_sentences)
        json_descriptions = ask_ollama.get_json_descriptions_from_story(swapped_sentences)

    #make this be a json if it isn't json_descriptions
    json_descriptions = json.loads(json_descriptions)
    #save the json_descriptions to a file that uses the current time and date in the name
    current_time = time.strftime("%Y%m%d-%H%M%S")

    with open (home_directory + "/projects/dreamdrawer/json_descriptions"+current_time+".json", "w") as f:
        json.dump(json_descriptions, f)
    print("json_descriptions:")
    print(json_descriptions)

    #iterate through the json_descriptions and replace the pronouns with the descriptions
    item_count = 0
    passed_images = 0
    generation_method = 1
    if generation_method == 0:
        for key, value in json_descriptions.items():
            image_looks_good = False
            image_prompt = value
            original_sentence = key
            image_generation_attempts = 0
            item_count += 1
            while not image_looks_good and image_generation_attempts < 3:
                
                print('-----item ' + str(item_count) + '/' + str(len(json_descriptions)) + ' gen atmpt: ' + str(image_generation_attempts) + ' image_prompt: ' + image_prompt)
                prompt_to_generate = ask_ollama.prompt_generator(image_prompt, original_sentence)
                prompt_to_generate = prompt_to_generate + ", realistic color photograph"
                #ask_ollama.reduce_memory_usage()
                kill_ollama.kill_ollama_processes(sudo_password)
                #time.sleep(10)
                filepath = ComfyUI_image_gen.generate_images_XL(prompt_to_generate)
                print('here is the filepath', filepath)
                #time.sleep(10)
                #check_and_start_service('ollama.service')
                #ask_ollama.reduce_memory_usage()
                image_description = ask_ollama.get_image_description_ollama(filepath[0])
                #reduce_memory_usage()
                #print("image_description", image_description)
                question = "Does a photo with this description: '"+image_description+"' make sense as a visual representation of this line '"+key+"' in this story '"+swapped_sentences+"'?"
                image_quality_response = ask_ollama.image_description_checker(question)
                #print('image_quality_response', image_quality_response)
                if "pass" in image_quality_response:
                    print('PASS')
                    image_looks_good = True
                    passed_images += 1
                else:
                    image_prompt = ask_ollama.prompt_improver("This prompt '"+image_prompt+"' does not generate a good enough image for this reason: '"+image_quality_response+"'. Please slightly adjust the original prompt with the feedback in mind. Respond with only the modified prompt.")
                    print('NEW IMAGE PROMPT\n', image_prompt)
                    image_generation_attempts += 1
        print("passed_images", passed_images)
    if generation_method == 1:
        list_of_list_of_prompts = []
        item_count = 0
        for key, value in json_descriptions.items():
            image_looks_good = False
            image_prompt = value
            original_sentence = key
            item_count += 1
            print('-----prompt made ' + str(item_count) + '/' + str(len(json_descriptions)) + ' image_prompt: ' + image_prompt)
            prompt_to_generate = ask_ollama.prompt_generator(image_prompt, original_sentence)
            prompt_to_generate = prompt_to_generate + ", realistic color photograph"
            list_of_list_of_prompts.append(prompt_to_generate)
            #ask_ollama.reduce_memory_usage()

        kill_ollama.kill_ollama_processes(sudo_password)
        item_count = 0
        for prompt in list_of_list_of_prompts:
            item_count += 1
            print('-----art made ' + str(item_count) + '/' + str(len(json_descriptions)) + ' image_prompt: ' + image_prompt)
            #time.sleep(10)
            filepath = ComfyUI_image_gen.generate_images_XL(prompt)

    # sd_prompts = []
    # num_sentences_before_after = 1  # Adjust this variable to change the number of sentences before and after
    # print("replaced_pronouns_sentences:\n" + '\n'.join(replaced_pronouns_sentences))
    # for i, replaced_pronouns_sentence in enumerate(replaced_pronouns_sentences):
    #     # Get the sentences before and after the current one
    #     start = max(0, i - num_sentences_before_after)
    #     end = min(len(replaced_pronouns_sentences), i + num_sentences_before_after + 1)
    #     surrounding_sentences = replaced_pronouns_sentences[start:end]
        
    #     # Combine the sentences into the story
    #     story = ' '.join(surrounding_sentences)
    #     sd_prompts.append(send_prompt(replaced_pronouns_sentence, story, 
    #         "You are a creative visual scene creator. You will receive a background story and a specific sentence. By using the context, you create a visual of description of the specific sentence. Your response is an unlabeled list of of short, comma separated phrases. Your unlabeled response includes key information such as setting, characters, actions, objects. respond with a single, unlabeled list of short, comma separated phrases. Only describe the target sentence. ",
    #         "Scene phrases 1: "))
    #     sd_prompts.append(send_prompt(replaced_pronouns_sentence, story, 
    #         "You create a list of short visual descriptions about a sentence that you are given. Your focus is the sentence, but you are also given a background story in case you need help filling in any missing context. You include everything that would be needed to reconstruct the sentence visually. You only respond with a single, unlabeled list of short, comma separated phrases. Only describe the target sentence.",
    #         "Visual description 2: "))
    #     sd_prompts.append(send_prompt(replaced_pronouns_sentence, story, 
    #         "You are a creative scene creator. You follow directions exactly. You only ever say a single sentence. You are an artist. You receive a background story and a specific sentence and you respond with a visual description that portrays a single picture that could be taken of a scene from that specific sentence. You only respond with one sentence.", 
    #         "Original Visual Scene 3: "))

    # processed_sd_prompts = []
    # for sd_prompt in sd_prompts:
    #     #replace any special characters that might cause problems
    #     sd_prompt = sd_prompt.replace('.', '')
    #     sd_prompt = sd_prompt.replace('*', ',')
    #     sd_prompt = sd_prompt.replace('\n', ' ')
    #     processed_sd_prompts.append(process_description(sd_prompt))

    # # this is the model that is being run just to lower the ram usage after we use the better model
    # orca_mini = subprocess.Popen(["ollama", "run", "orca-mini:3b"], preexec_fn=os.setsid)
    # time.sleep(5)
    # orca_mini.terminate()

    # #save the prompts to a file
    # with open (home_directory + "/projects/dreamdrawer/processed_sd_prompts.txt", "w") as f:
    #     f.write("\n".join(processed_sd_prompts))


    # print("PROCESSED_SD_PROMPTS:\n\n")
    # print("\n".join(processed_sd_prompts))
    # prompts_printed = 0
    # for processed_sd_prompt in processed_sd_prompts:
    #     print(str(prompts_printed) + "/" + str(len(processed_sd_prompts)))
    #     print(processed_sd_prompt)
    #     ComfyUI_image_gen.generate_images_XL(processed_sd_prompt)
    #     prompts_printed += 1
    #     #ComfyUI_image_gen.generate_images_XL_turbo(sd_prompt)

    #this is only for XL_turbo - but why? shouldnt it also be for XL?
    #subprocess.run(["pkill", "-f", "/home/lunkwill/projects/ComfyUI/main.py"], check=True)

    telegram_service.send_telegram_text_as_me_to_bot("Finished generating dr. images")

story_to_sd_prompts(story)