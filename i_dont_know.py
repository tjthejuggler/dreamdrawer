import ollama
from nltk.tokenize import sent_tokenize
import base64
import requests
import json


story = "Hatice and I are on our way to a juggling convention, but we need to get food first. We have no car and so for some reason we ask someone with a car who is going to take our phones. We manage to make it to a store, they have Doritos and a chicken restaurant. We buy Doritos and ask if the restaurant has vegan food. They say no. A customer tells us that when they came long ago they were stuck eating Doritos as well."

def llm_request(system_prompt, user_prompt):

    stream = ollama.chat(
        model='solar',
        messages=[{'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}],
        stream=False,
    )

    print(stream['message']['content'])

    return stream['message']['content']

def generate_request(model, system_prompt, user_prompt, image = None):
    print("Generating request")
    url = "http://localhost:11434/api/generate"
    if image:
        data = {
            "model": model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            #"stream": False,
            "keep_awake": "0",
            "images": [image]
        }
    else:
        data = {
            "model": model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            #"stream": False,
            "keep_awake": "0",
        }
    response = requests.post(url, data=json.dumps(data))
    json_response = json.loads(response.text)
    print(json_response)
    print(json_response["response"])
    return json_response["response"]

def reduce_memory_usage():
    response = generate_request("tinyllama", "You reduce GPU usage", "Why is the sky blue?")
    return response

def get_json_descriptions_from_story(user_prompt):
    
    system_prompt = '''Your input is a story, and you output a JSON that divides it into visual aspects and their descriptions. Here are some examples: \n\n
    'INPUT:\n
    'I\'m in highschool, I get a job fast-food place. It starts at 2pm. That\'s the same time school ends. The fast-food restaurant is just across the street from the school. The boss at the fast-food restaurant seems pretty intimidating. I\'m at my last class of the day at school and a student says they have to go because it is 2pm. I didn\'t realize it was so late, I\'m disappointed. I have to put on my fast-food work shirt. I hurry over to work, but get there late. I decide I will ask for later start times. I have some thought about starting later meaning that I will have to stay very late.\n\n
    'OUTPUT:\n
    '{
  "I'm in highschool, I get a job fast-food place.": "A teenager standing outside a bustling fast-food restaurant, looking intrigued yet slightly apprehensive.",
  "It starts at 2pm. That's the same time school ends.": "A school bell ringing with students streaming out, the fast-food restaurant visible across the street, clock showing 2:00 PM.",
  "The fast-food restaurant is just across the street from the school.": "A busy street scene with a high school on one side and a fast-food restaurant on the other, students crossing between them.",
  "The boss at the fast-food restaurant seems pretty intimidating.": "An imposing figure looming over the fast-food counter, casting a shadow, with a stern expression.",
  "I'm at my last class of the day at school and a student says they have to go because it is 2pm.": "A classroom with a clock showing 2:00 PM, a student hastily packing up, while others look on.",
  "I didn't realize it was so late, I'm disappointed.": "A close-up of a dismayed student glancing at a clock, realization and disappointment evident on their face.",
  "I have to put on my fast-food work shirt.": "A hurried change into a fast-food uniform, logo visible, in a cramped and nondescript space.",
  "I hurry over to work, but get there late.": "Rushing across the street towards the fast-food restaurant, looking anxious, with the restaurant's sign in the background.",
  "I decide I will ask for later start times.": "Standing determined in front of a daunting fast-food manager, ready to negotiate a change in schedule.",
  "I have some thought about starting later meaning that I will have to stay very late.": "Contemplating the empty, dimly lit interior of the fast-food restaurant late at night, broom in hand."
}

INPUT:\n
I'm homeless in nyc, walking through parks and such. Finally , I decide I will go for a swim to clean off. I want to put on my bathing suit before I head to the beach, so I go behind a building, I decide I will be super fast, take off my underwear, then try to quickly put on the swim shorts. They are so tight, it is slow  the parking lot is on a huge hill, people see me, I can see them pointing, I am really hoping no. Cop drives by. Finally I get them on.
OUTPUT:\n
{
  "I'm homeless in nyc, walking through parks and such.": "A lone figure meanders through a lush, green park in the heart of New York City, surrounded by towering skyscrapers under a clear blue sky.",
  "Finally, I decide I will go for a swim to clean off.": "A determined individual stands at the edge of a serene urban waterfront, gazing at the water's gentle waves, ready to take a refreshing swim.",
  "I want to put on my bathing suit before I head to the beach, so I go behind a building,": "Behind a secluded urban building, a person prepares for a swim, creating a makeshift changing room amidst the concrete landscape.",
  "I decide I will be super fast, take off my underwear, then try to quickly put on the swim shorts.": "In a blur of motion, an individual attempts to swiftly change into swimwear, capturing a moment of urgency and haste.",
  "They are so tight, it is slow": "Struggling with the swim shorts, the individual battles with the tight fabric, a visible struggle against the constricting garment.",
  "the parking lot is on a huge hill, people see me, I can see them pointing,": "From a high vantage point, onlookers in a sloped parking lot catch sight of the changing individual, pointing and observing from afar.",
  "I am really hoping no. Cop drives by.": "An anxious glance is cast towards the street, filled with the hope that no police car appears, under the watchful eyes of the city.",
  "Finally I get them on.": "Triumphantly, the swim shorts are on, the person stands ready, a small victory against the backdrop of an urban challenge."
}
INPUT:\n
Rode the bus with two friends trying to find our hotel. In the bus showing some strangers some magic tricks, but i didn't know many. They were only somewhat impressed. The muscle pass didn't really work well since I'm out of practice and my callous is gone. We were not sure which stop to use, but we got off eventually. While walking through a mall with a stranger who was helping us find our hotel I saw a sick or wounded dog on a blanket and I thought it was a veterinarian in the mall. Then I noticed large raw meat near the dog and realized they were killing dogs for food.
OUTPUT:\n
{
  "Rode the bus with two friends trying to find our hotel.": "Three friends seated on a bus, looking around with maps in hand, portraying a sense of adventure and mild confusion.",
  "In the bus showing some strangers some magic tricks, but i didn't know many.": "A small group of passengers gathered around, watching a person attempting magic tricks with cards, expressions mixed with mild interest.",
  "They were only somewhat impressed.": "Spectators with polite smiles, clapping lightly, not fully captivated by the performance.",
  "The muscle pass didn't really work well since I'm out of practice and my callous is gone.": "A close-up of a hand trying to perform the muscle pass with a coin, faltering, highlighting the absence of a callous.",
  "We were not sure which stop to use, but we got off eventually.": "The group of friends hesitating at the bus door, then stepping off onto a busy street, looking uncertainly in different directions.",
  "While walking through a mall with a stranger who was helping us find our hotel": "A group of friends following a helpful stranger through a bustling mall, luggage in tow, passing shops and kiosks.",
  "I saw a sick or wounded dog on a blanket and I thought it was a veterinarian in the mall.": "A poignant scene of a sick dog lying on a blanket in the corner of a busy mall, with people passing by, a sign of veterinary care assumed nearby.",
  "Then I noticed large raw meat near the dog and realized they were killing dogs for food.": "A shocking revelation as the viewpoint shifts to reveal not a vet's care but large pieces of raw meat nearby, hinting at a grim purpose, under the harsh mall lighting."
}


'''  
    
    # stream = ollama.chat(
    #     model='mixtral',
    #     messages=[{'role': 'system', 'content': system_prompt},
    #                 {'role': 'user', 'content': "INPUT:\n"+user_prompt}],
    #     stream=False,
    # )

    # print(stream['message']['content'])

    # return stream['message']['content']

    # stream = ollama.generate(
    #     model='solar',
    #     prompt="INPUT:\n"+user_prompt,
    #     system=system_prompt,
    #     format="json",
        
    #     # messages=[{'role': 'system', 'content': system_prompt},
    #     #             {'role': 'user', 'content': user_prompt}],
    #     stream=False,
    #     #keep_awake= "0",
    # )

    # print(stream['response'])

    # return stream['response']

    response = generate_request("solar", system_prompt, "INPUT:\n"+user_prompt)

    return response






# def prompt_improver(user_prompt):
#     system_prompt = '''You improve a prompt by taking the advice given to you'''  
    
#     stream = ollama.chat(
#         model='solar',
#         messages=[{'role': 'system', 'content': system_prompt},
#                     {'role': 'user', 'content': user_prompt}],
#         stream=False,
#     )

#     print(stream['message']['content'])

#     return stream['message']['content']

def prompt_improver(user_prompt):
    # system_prompt = '''You improve a prompt by taking the advice given to you'''  
    
    # stream = ollama.generate(
    #     model='solar',
    #     prompt=user_prompt,
    #     system=system_prompt,
    #     # messages=[{'role': 'system', 'content': system_prompt},
    #     #             {'role': 'user', 'content': user_prompt}],
    #     stream=False,
    #     #keep_awake= "0",
    # )

    # print(stream['response'])

    # return stream['response']

    response = generate_request("solar", "You improve a prompt by taking the advice given to you", user_prompt)
    return response

# def image_description_checker(user_prompt):
#     system_prompt = '''You determine if a description of an image is representative of a given line in a story. If you are happy with it then just say PASS, otherwise explain why it is not a representative image'''  
    
#     stream = ollama.chat(
#         model='solar',
#         messages=[{'role': 'system', 'content': system_prompt},
#                     {'role': 'user', 'content': user_prompt}],
#         stream=False,
#     )

#     print(stream['message']['content'])

#     return stream['message']['content']

def image_description_checker(user_prompt):
    system_prompt = '''You determine if a description of an image is representative of a given line in a story. If you are happy with it then just say PASS, otherwise explain why it is not a representative image'''  
    
    # stream = ollama.generate(
    #     model='solar',
    #     prompt=user_prompt,
    #     system=system_prompt,
    #     # messages=[{'role': 'system', 'content': system_prompt},
    #     #             {'role': 'user', 'content': user_prompt}],
    #     stream=False,
    #     #keep_awake= "0",
    # )

    # print(stream['response'])

    # return stream['response']
    response = generate_request("solar", system_prompt, user_prompt)
    return response

def get_image_description_ollama(image_path):
    # Convert image to base64
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # data = {
    #     "model": "llava",
    #     "prompt": "tell me in extreme detail exactly what this is an image of. omit nothing that you are able to observe in this picture.",
    #     "stream": False,
    #     "options": {"num_predict": 150},
    #     "images": [encoded_string]
    # }

    # stream = ollama.generate(
    #     model="llava",
    #     prompt="tell me in extreme detail exactly what this is an image of. Omit nothing that you are able to observe in this picture:",
    #     images=[image_path],
    #     stream= False,
    #     #keep_awake= "0",
    # )


    # print(stream['response'])

    # return(stream['response'])
    response = generate_request("llava", "You descrive images", "tell me in extreme detail exactly what this is an image of. Omit nothing that you are able to observe in this picture.", encoded_string)
    return response
# image_path = "/home/lunkwill/Pictures/Wallpapers/ai_art/_The_30-year-old_man's_face_contorts_in_horror_as__1_1.png"
# print(get_image_description_ollama(image_path))
#print(separate_sentence(story))

# sentences = sent_tokenize(story)
# visual_aspects = []
# for sentence in sentences:
#     new_visual_aspect = separate_sentence(sentence)
#     #new_visual_aspect = new_visual_aspect.replace('\"','\\\"')
#     new_visual_aspect = new_visual_aspect.replace('\'','\\\'')
#     #convert new_visual_aspects to a list if it is not already a list
#     if not isinstance(new_visual_aspect, list):
#         new_visual_aspect = ast.literal_eval(new_visual_aspect)
#     print('new_visual_aspect',new_visual_aspect)
#     visual_aspects.extend(new_visual_aspect)

#     print(visual_aspects)

#print(ollama.embeddings(model='mistral', prompt='They sky is blue because of rayleigh scattering'))
import time
for i in range(100):
    print(i)
    print(reduce_memory_usage())
    time.sleep(10)
    print(get_image_description_ollama("/home/lunkwill/Pictures/Wallpapers/ai_art/_The_30-year-old_man's_face_contorts_in_horror_as__1_1.png"))   
    print(image_description_checker("The sky is blue because of rayleigh scattering"))
    print(prompt_improver("I am a weak model"))
