from litellm import completion

response = completion(
            model="ollama/mixtral", 
            messages = [{ "content": "Hello, how are you?","role": "user"}], 
            api_base="http://localhost:11434",
            stream=True,
)

for chunk in response: 
    print(chunk)