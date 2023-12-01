import requests
# from diffusers import DiffusionPipeline
# from torchvision.utils import save_image
# from torchvision import transforms
import json
import subprocess
import time
#THIS CODE USES LITELLAMA IF IT IS RUNNING, AND IF IT ISN'T RUNNING THEN IT STARTS IT AND STOPS IT AFTERWARDS



#you have to run this command in terminal- litellm --model ollama/mistral
def send_prompt_to_llm_litellm(user_prompt, system_prompt = None):
    server_started_now = False
    url = "http://0.0.0.0:8000"
    # Check if the server is running
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Server is running")
            
    except requests.exceptions.RequestException as err:
        server_started_now = True
        print("Server is not running, starting it now...")
        subprocess.Popen(["litellm", "--model", "ollama/mistral"])
        time.sleep(5)

    url = "http://0.0.0.0:8000/chat/completions"
    headers = {"Content-Type": "application/json"}
    if system_prompt is None:
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        }
    else:
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": user_prompt},
                {"role": "system", "content": system_prompt}
            ]
        }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # Convert the response to JSON
    response_json = response.json()
    # Get the content string

    if server_started_now:
        # Kill the server
        subprocess.run(["pkill", "-f", "litellm"])
        print("Server killed")
        time.sleep(5)
    return response_json['choices'][0]['message']['content']

#print(send_prompt_to_llm("What is the largest animal?"))










#!!DEPREICATED!!
#if for some reason we want to go back to doing this with local llm then we can use this and we need to uncomment the import statements above
def send_prompt_to_llm(system_prompt, user_prompt):
    
    url = "http://localhost:1234/v1/chat/completions"
    #url = "http://0.0.0.0:8000"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data).json()
    print(response)

    return response['choices'][0]['message']['content']