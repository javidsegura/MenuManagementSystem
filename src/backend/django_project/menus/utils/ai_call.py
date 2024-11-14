import base64
import os
from openai import OpenAI
from menus.utils.process_ai import populate_menu_data

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

        print(f"OpenAI Response: {response.choices[0].message.content}")
        return response.choices[0].message.content
                
    except Exception as e:
        print(f"Error in ai_call: {str(e)}")
        raise
                