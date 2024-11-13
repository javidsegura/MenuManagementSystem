from openai import OpenAI
import os
from base64 import b64encode
import json

def summarize_content(image_path: str) -> json:
    """ 
    Definition: Send image and text for LLM summarization 
    Parameters:
        - image_path = image of the menu (must be PDF/PNG)
    Returns:
        - JSON object with the following structure:
            {
                
            }
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
    
    # Read and encode the image
    with open(image_path, "rb") as image_file:
        image_data = b64encode(image_file.read()).decode('utf-8')
    
    # Prepare the message for GPT-4 Vision
    messages = [
        {
            "role": "system",
            "content": ""
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f""" """
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_data}"
                    }
                }
            ]
        }
    ]
    
    # Make the API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500
    )
    
    # Extract the summary and clean it up
    content = response.choices[0].message.content

    # Remove markdown code block indicators if present
    content = content.replace('```json', '').replace('```', '').strip()
    
    #  Return JSON
    return json.loads(content)
    
