import base64
import os
from openai import OpenAI
from menus.utils.process_ai import populate_menu_data
import json

# TO DO: get a dict with all the info. Then write it to the db

def ai_call(menu_file):
    """ Send the menu file to OpenAI to process """
    print(f"AI call for uploaded file")
    try:
        # OpenAI API call
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Read image file directly from the InMemoryUploadedFile
        base64_image = base64.b64encode(menu_file.file.read()).decode('utf-8')
        
        # Reset file pointer for future reads
        menu_file.file.seek(0)

        messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Please analyze this menu image and return a JSON with the following structure:
                            {
                                "menu_sections": [
                                    {
                                        "name": "section name",
                                        "items": [
                                            {
                                                "name": "item name",
                                                "description": "item description",
                                                "price": float,
                                                "dietary_restrictions": ["restriction1", "restriction2"]
                                            }
                                        ]
                                    }
                                ]
                                "restaurant_info":{
                                    "resturant_name": "restaurant name", #may be extracted from the webiste url
                                    "address": "restaurant address",
                                    "phone": "restaurant phone",
                                    "website": "restaurant website"
                                }
                            }"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
                
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=4096
        )

        content = response.choices[0].message.content.replace('```json', '').replace('```', '').strip()

        print(f"Content: {content}")
    
        # Extract just the JSON part
        json_str = content[content.find('{'):content.rfind('}')+1] # get just ext
        json_response = json.loads(json_str)
        print(f"JSON Response: {json_response}")

        return json_response
    
    except Exception as e:
        print(f"Error in ai_call: {str(e)}")
        raise
                