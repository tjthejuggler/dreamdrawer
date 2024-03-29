import requests
import json
import subprocess
import time


def connect_to_llm():
    #subprocess.Popen(["litellm", "--model", "ollama/mistral"])
    subprocess.Popen(["litellm", "--model", "ollama/solar"])
    #subprocess.Popen(["litellm", "--model", "ollama/mixtral"])
    #subprocess.Popen(["ollama", "serve"])
    
    time.sleep(10)

#you have to run this command in terminal- litellm --model ollama/mistral
def send_prompt_to_llm(user_prompt, system_prompt = None): #IT IS LIKE IT IS LOOKING FOR SOLAR HERE FOR SOME REASON? CHECK LOG
    # url = "http://0.0.0.0:8000"    
    # try: # Check if the server is running
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         print("Server is running")            
    # except requests.exceptions.RequestException as err:
    #     print("Server is not running, starting it now...")
    #     subprocess.Popen(["litellm", "--model", "ollama/neural-chat:7b-v3.2-fp16"])
    #     time.sleep(5)
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
    response_json = response.json()
    return response_json['choices'][0]['message']['content']

#print(send_prompt_to_llm("What is the largest animal?"))










#!!DEPREICATED!!
#if for some reason we want to go back to doing this with local llm then we can use this and we need to uncomment the import statements above
def send_prompt_to_llm_orig(system_prompt, user_prompt):
    
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