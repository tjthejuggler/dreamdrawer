import base64
import requests
import json

# Path to your image
image_path = '/home/lunkwill/Pictures/Wallpapers/ai_art/ComfyUI_05756_.png'
image_path = '/home/lunkwill/projects/ComfyUI/output/Two_alert_goats_wearing_thinking_caps,_one_beaming_with_a_smile_while_the_other__00001_.png'

def get_image_description(image_path):
    # Convert image to base64
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # API endpoint
    url = 'http://localhost:11434/api/generate'


    data = {
        "model": "llava",
        "prompt": "tell me in extreme detail exactly what this is an image of. omit nothing that you are able to observe in this picture.",
        "stream": False,
        "options": {"num_predict": 150},
        "images": [encoded_string]
    }

    # Headers
    headers = {'Content-Type': 'application/json'}

    # POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    #convert response.text to json

    json_response = response.json()


    print(json_response["response"])
    return json_response["response"]
    print("\n" + "="*50 + "\n")
