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

# def reduce_memory_usage():

#     url = "http://localhost:11434/api/generate"
#     data = {
#         "model": "tinyllama",
#         "prompt": "Why is the sky blue?",
#         "stream": False,
#         "keep_awake": "0",
#     }
#     response = requests.post(url, data=json.dumps(data))
#     json_response = json.loads(response.text)
#     print(json_response["response"])


def generate_request(model, system_prompt, user_prompt, image = None):
    print("Generating request")
    url = "http://localhost:11434/api/generate"
    if image:
        data = {
            "model": model,
            "system": system_prompt,
            "prompt": user_prompt,
            "stream": False,
            "keep_awake": "0",
            "images": [image]
        }
    else:
        data = {
            "model": model,
            "system": system_prompt,
            "prompt": user_prompt,
            "stream": False,
            "keep_awake": "0",
        }
    response = requests.post(url, data=json.dumps(data))
    #print(response.text)
    json_response = json.loads(response.text)
    print("-----------------SYSTEM PROMPT")
    print(system_prompt)
    print("-----------------USER PROMPT")
    print(user_prompt)
    print("------------------RESPONSE")
    # print(json_response)
    print(json_response["response"])
    return json_response["response"]

def reduce_memory_usage():
    response = generate_request("tinyllama", "You reduce GPU usage", "Why is the sky blue?")
    return response

def get_json_descriptions_from_story(user_prompt):
    
    system_prompt = '''Your input is a story, and you output a JSON that divides it into visual aspects and their descriptions. Here are some examples: \n\n
    'INPUT:\n
    A 30 year old man with long blond hair is with Turkish girl with long dark hair, they are traveling and seeing family. They are deciding to break up. They are in a bedroom, just the two of them. For some reason, A 30 year old man with long blond hair gives her his electronic weed pen in the breakup. A bit later, A 30 year old man with long blond hair decides that he wants it back. A 30 year old man with long blond hair goes and asks her for the pen he gave her earlier. A 30 year old man with long blond hair doesn't want to be obvious because she is talking to a father figure. The father figure is quite interested in why A 30 year old man with long blond hair keeps asking her about a pen. She doesn't seem to know what A 30 year old man with long blond hair is talking about. Finally, she realizes and she throws the pen in a fire. The father figure realizes and gets very angry. The father starts to turn into a fiery devil. A 30 year old man with long blond hair runs to the bathroom to escape him. It is pitch black in the small bathroom. A 30 year old man with long blond hair doesn't know why, but the devil begins chanting infanticide over and over.
    'OUTPUT:\n
    {
  "a 30-year old man with long blond hair is with a Turkish girl with long dark hair, they are traveling and seeing family.": "A picturesque scene of a 30-year-old man with sun-kissed blond hair and a Turkish woman with cascading dark locks, sharing a moment of joy and companionship against a backdrop of travel and familial connections.",
  "the 30-year old man with long blond hair and his partner are making the decision to separate.": "A heart-wrenching moment captured at a metaphorical crossroads, where a man with flowing blond hair and his companion face each other, the air heavy with the decision of parting ways, encapsulating the gravity of their farewell.",
  "a 30-year old man with long blond hair and another person are in a bedroom together.": "An intimate and personal scene unfolds in a softly lit bedroom, where a 30-year-old with blond hair shares a private moment, hinting at the complexities of human connections behind closed doors.",
  "in the breakup, a 30-year old man with long blond hair gives her his electronic weed pen.": "In a poignant gesture of separation, the blond man solemnly hands over an electronic weed pen to his partner, a symbolic act of parting gifts and shared memories coming to an end.",
  "a bit later, the 30-year old man with long blond hair decides that he wants the particular item back.": "A scene of reflection and reconsideration as the blond man contemplates his previous decision, the desire to reclaim the electronic pen symbolizing a deeper yearning for lost connections.",
  "the 30-year old man with long blond hair goes and asks her for the pen he gave her earlier.": "A delicate encounter unfolds as the man, with his distinctive blond hair, approaches his former partner to ask for the electronic pen, revealing layers of unresolved feelings and attachment.",
  "the 30-year old man with long blond hair doesn't want the situation to appear obvious because he understands that she is conversing with an individual who holds a fatherly role or significance in her life.": "Amidst a sensitive conversation, the blond man tactfully navigates the complex dynamics, wary of the presence of a paternal figure in his ex-partner's life, highlighting his cautious approach to avoid misunderstandings.",
  "the 30-year old man with long blond hair's father figure is quite interested in why he keeps asking the woman about a pen.": "Curiosity piques as the father figure observes the blond man's persistent inquiries about the pen, adding a layer of intrigue and tension to the unfolding narrative.",
  "the 30-year old man with long blond hair doesn't seem to know what he is talking about.": "Confusion and ambiguity mark the conversation, as the blond man struggles to articulate his reasons, his uncertainty casting a shadow over his intentions.",
  "finally she realizes and she throws the pen in a fire.": "A dramatic climax as the woman, upon grasping the full import of the request, decisively throws the electronic pen into the flames, symbolizing the irreversible severing of their ties.",
  "the father figure realizes and gets very angry. the father figure realizes and gets very angry.": "A sudden surge of anger overwhelms the father figure as he comprehends the situation, his fury embodying the emotional intensity of the moment.",
  "the father starts to turn into a fiery devil.": "A supernatural twist as the father figure undergoes a terrifying transformation into a devil of flames, introducing a fantastical element to the narrative's climax.",
  "the 30-year old man with long blond hair runs to the bathroom to escape him.": "In a desperate bid for safety, the blond man flees to the confines of a bathroom, seeking refuge from the infernal wrath unleashed upon him.",
  "it is pitch black in the small bathroom.": "A palpable sense of dread fills the air as darkness engulfs the small bathroom, the absence of light mirroring the man's fear and isolation.",
  "the 30-year old man with long blond hair doesn't know why, but the devil begins chanting infanticide over and over.": "An eerie atmosphere envelops the scene as the devil, amidst flames, ominously chants 'infanticide', the repetition of the word adding a chilling resonance to the encounter's climax."
}
INPUT:\n
A 30 year old man with long blond hair is on a small vacation with family. They are on a boat at a boat dock. The young nieces are there on the boat dock. One little girl falls in the water and A 30 year old man with long blond hair helps her out. Uncle Alan shows up, A 30 year old man with long blond hair feels bad about Logan dying and A 30 year old man with long blond hair holds his hand. It is awkward, they switch to holding pinky fingers.
OUTPUT:\n
{
  "a 30-year old man with long blond hair is on a small vacation with his family.": "Surrounded by the tranquil sea, a man in his thirties with sunlit blonde hair enjoys a serene moment on a boat, the essence of family vacation surrounding him.",
  "a 30-year old man with long blond hair and another person are on a boat at a boat dock.": "A serene dock scene, where a man adorned with long blonde hair and a companion stand together on a boat, the wooden planks of the dock beneath them telling stories of many such departures.",
  "the young nieces are there on the boat dock.": "Excitement and joy fill the air as young girls, the man's nieces, play and laugh on the dock, their youthful energy infectious.",
  "a 30-year old man with long blond hair helps a little girl who has fallen in the water to get out.": "In a moment of quick action, the man with flowing blonde hair reaches into the water to rescue a little girl, ensuring her safety with a gentle embrace.",
  "a 30-year old man with long blond hair feels bad about logan dying when uncle alan shows up, and he holds logan's hand in consolation.": "A poignant scene unfolds as the blonde man, touched by sorrow, offers comfort to Logan through a tender handhold, the arrival of Uncle Alan adding depth to the moment of grief.",
  "it is awkward as the 30-year old man with long blond hair switches to holding pinky fingers.": "In a delicate shift of connection, the blonde man and the child exchange a pinky promise, an awkward yet deeply meaningful gesture that bridges their moment of discomfort."
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

    response = generate_request("mixtral", system_prompt, "INPUT:\n"+user_prompt)

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
    response = generate_request("llava", "You describe images", "tell me in extreme detail exactly what this is an image of. Omit nothing that you are able to observe in this picture.", encoded_string)
    return response
# image_path = "/home/lunkwill/Pictures/Wallpapers/ai_art/_The_30-year-old_man's_face_contorts_in_horror_as__1_1.png"
# print(get_image_description_ollama(image_path))
#print(separate_sentence(story))

def prompt_generator(user_prompt, original_sentence):

    system_prompt = '''You receive some text and your respond with ONLY the indicated visually descriptive prompt. You want the prompt to be about 30 words or less, so remove any words that do not add significantly to the visual description. You also receive the SOURCE SENTENCE which you use to make any adjustments to the prompt. The prompt is meant to depict some aspect of the SOURCE SENTENCE. You do not submit any text other than the prompt. You do not make any preface to the prompt, the only text that you respond with is the prompt.'''  
    
    user_prompt = "SOURCE SENTENCE:\n"+original_sentence+"\nINPUT TEXT:\n"+user_prompt+"\nRESPONSE PROMPT:\n" 

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
    response = generate_request("mixtral", system_prompt, user_prompt)
    return response

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
# import time
# for i in range(100):
#     print(i)
#     print(reduce_memory_usage())
#     time.sleep(10)
#     print(get_image_description_ollama("/home/lunkwill/Pictures/Wallpapers/ai_art/_The_30-year-old_man's_face_contorts_in_horror_as__1_1.png"))   
#     print(image_description_checker("The sky is blue because of rayleigh scattering"))
#     print(prompt_improver("I am a weak model"))
