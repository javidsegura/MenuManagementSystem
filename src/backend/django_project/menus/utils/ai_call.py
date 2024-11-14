import base64
import os
from openai import OpenAI
from menus.utils.process_ai import populate_menu_data

def ai_call(file):
    print(f"AI call for {file.menuPdf.path}")
    try:
        # Read image file
        #with open(file.menuPdf.path, 'rb') as image_file:
            #base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # OpenAI API call
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Say hello"""
                        },
                    ]
                }
            ],
            max_tokens=4096
        )

        print(f"OpenAI Response: {response.choices[0].message.content}")
        menu_data = response.choices[0].message.content
        populate_menu_data(file, menu_data)
                
    except Exception as e:
        print(f"Error in ai_call: {str(e)}")
        raise