import requests
import json
import base64
import os

# Your OpenAI API key
api_location = '~/projects/autogen/openai_api_key.txt'
api_location = os.path.expanduser(api_location)
with open(api_location, 'r') as f:
    api_key = f.read().strip()

# The API endpoint for DALL-E image generation
api_url = 'https://api.openai.com/v1/images/generations'

# The headers to be sent with the request
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# The payload with the prompt and other parameters
payload = {
    "prompt": "A futuristic cityscape at sunset, with flying cars and towering skyscrapers, all bathed in a golden light.",
    "size": "1024x1024",
    "n": 2
}

# Make the POST request to the API
response = requests.post(api_url, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Load the response data into a dict
    data = response.json()
    
    # Download and save the image data to a file
    for i, image_data in enumerate(data['data']):
        # Get the image URL
        image_url = image_data['url']
        
        # Make a GET request to the image URL
        image_response = requests.get(image_url)
        
        # Check if the image request was successful
        if image_response.status_code == 200:
            # Write the image to a file
            with open(f'image_{i}.png', 'wb') as f:
                f.write(image_response.content)
            print(f'Image {i} saved.')
        else:
            print(f'Failed to download image {i}: {image_response.status_code}')

else:
    # Print the error if something went wrong
    print(f'Error: {response.status_code}')
    print(response.text)