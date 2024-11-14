
import json
from menus.models import Menu, MenuItem

def populate_menu_data(menu_obj, menu_data_str):
    print(f"Populating menu data for {menu_obj} and {menu_data_str}")
    try:
        menu_data = json.loads(menu_data_str)
        
        # Update menu details
        if 'restaurant_name' in menu_data:
            menu_obj.restaurant.name = menu_data['restaurant_name']
            menu_obj.restaurant.save()
        
        # Create menu items
        if 'menu_items' in menu_data:
            for item in menu_data['menu_items']:
                MenuItem.objects.create(
                    menu=menu_obj,
                    name=item['name'],
                    price=item['price'],
                    category=item.get('category', '')
                )
                
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from OpenAI")