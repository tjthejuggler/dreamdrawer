
















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
    sudo_password = input("Enter sudo password: ")
    sentences = sent_tokenize(story)
    print("sentences:\n" + '\n'.join(sentences))
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
#     json_descriptions = ''' {
#   "a 30-year-old man with long blond hair finds himself in a location surrounded by other individuals whom he doesn't have particularly close relationships with.": "A lone figure with long, flowing blond hair stands amidst a group of unfamiliar faces, exuding a sense of separation and aloofness.",
#   "there are kids there": "A backdrop of children playing in the distance, their laughter audible, adding vibrant energy to the scene.",
#   "a 30-year old man with long blond hair has two nice gel pens that he really likes.": "Admiring a pair of exquisite gel pens, gleaming under the light, treasured by their long-haired owner for their distinctiveness.",
#   "a 30-year-old man with long blond hair was delighted to find a pack of gel pens that he had been looking for, discarded between his car seats.": "A fortunate discovery of a cherished pack of gel pens, abandoned and overlooked between the car seats, now embraced by its grateful owner.",
#   "but they are expensive": "The two valuable gel pens stand out among their mundane surroundings, symbolizing something precious yet pricey.",
#   "there are some kids there": "Innocent children in the background, blissfully unaware of the value and desire surrounding the pair of unique gel pens.",
#   "as a 30-year-old man with long blond hair, i understand your concern about protecting your expensive gel pens from potential damage due to use by young children.": "A thoughtful long-haired individual contemplating the welfare of their valuable gel pens and considering ways to safeguard them from the unintentional harm caused by curious young hands.",
#   "to prevent any possible issues and preserve your collection of nice gel pens, you could consider keeping them in a safe place out of reach for the kids.": "A visualization of safely storing the precious gel pens on a high shelf or within a secure box, away from children's grasp to protect their integrity.",
#   "alternatively, provide separate, less expensive pens specifically designated for their use": "A display of affordable pens arranged neatly in a container, reserved and accessible just for young creatives to explore their artistic talents.",
#   "they press too hard and mess up the tips of the gel pens": "An illustration of children gripping gel pens with excessive force, causing the tips to become misshapen or damaged, while their long-haired guardian looks on disheartened.",
#   "the gel pen tips get flattened": "A close-up view of a once pristine gel pen tip now distorted and flattened due to rough handling by young artists, symbolizing the importance of responsible care.",
#   "a 30-year-old man with long blond hair tries out the pens one by one to examine their functionality and performance.": "A diligent long-haired individual carefully testing each gel pen in turn, ensuring they perform as expected, exuding a sense of dedication towards preserving their quality.",
#   "he notices that some of them are severely malfunctioning, leaking ink or failing to write smoothly": "An image of the disappointed long-haired person discovering an array of gel pens that have fallen short of expectations due to various performance issues.",
#   "the 30-year-old man continues testing each pen, mentally taking note of which ones need replacement in his collection": "A determination on the part of the long-haired individual to rectify the subpar gel pens by methodically evaluating their condition and making mental notes for future improvements.",
#   "the 30-year-old man with long blond hair is feeling a bit disheartened as he discovers that his initial harvest from the coconut tree is lesser than anticipated": "A picture of disappointment etched on the long-haired person's face upon realizing the meager yield from the coconut tree, yet maintaining hope and optimism for future harvests."
# }'''
    
    #make this be a json if it isn't json_descriptions
    json_descriptions = json.loads(json_descriptions)
    print("json_descriptions:")
    print(json_descriptions)

    #iterate through the json_descriptions and replace the pronouns with the descriptions
    item_count = 0
    for key, value in json_descriptions.items():
        image_looks_good = False
        image_prompt = value
        image_generation_attempts = 0
        item_count += 1
        while not image_looks_good and image_generation_attempts < 3:
            print('-----item ' + str(item_count) + '/' + str(len(json_descriptions)) + ' gen atmpt: ' + str(image_generation_attempts) + ' image_prompt: ' + image_prompt)
            #ask_ollama.reduce_memory_usage()
            kill_ollama.kill_ollama_processes(sudo_password)
            #time.sleep(10)
            filepath = ComfyUI_image_gen.generate_images_XL(image_prompt)
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
            else:
                image_prompt = ask_ollama.prompt_improver("This prompt '"+image_prompt+"' does not generate a good enough image for this reason: '"+image_quality_response+"'. Please slightly adjust the original prompt with the feedback in mind. Respond with only the modified prompt.")
                print('NEW IMAGE PROMPT\n', image_prompt)
                image_generation_attempts =+ 1


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