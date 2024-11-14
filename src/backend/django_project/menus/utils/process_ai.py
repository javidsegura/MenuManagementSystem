
import json
from menus.models import Menu, MenuItem, MenuSection, DietaryRestriction

def populate_menu_data(menu_obj: Menu, menu_data: dict):
    print(f"Populating menu data for {menu_obj}")
    try:
        # Update restaurant info in the existing restaurant
        restaurant_info = menu_data.get('restaurant_info', {})
        if restaurant_info:
            restaurant = menu_obj.menu_version.restaurant
            restaurant.name = restaurant_info.get('restaurant_name', restaurant.name)
            restaurant.phone = restaurant_info.get('phone', restaurant.phone)
            restaurant.street = restaurant_info.get('address', restaurant.street)
            restaurant.save()
        
        # Now create menu sections and items
        for section_data in menu_data.get('menu_sections', []):
            section = MenuSection.objects.create(
                menu=menu_obj,
                name=section_data.get('name', '')
            )
            
            # Create menu items for this section
            for item_data in section_data.get('items', []):
                menu_item = MenuItem.objects.create(
                    menu_section=section,
                    name=item_data.get('name', ''),
                    description=item_data.get('description', ''),
                    price=item_data.get('price', 0.0),
                    available=True
                )
                
                """# Handle dietary restrictions properly
                dietary_restrictions = item_data.get('dietary_restrictions', [])
                if dietary_restrictions:
                    for restriction in dietary_restrictions:
                        restriction_obj, _ = DietaryRestriction.objects.get_or_create(
                            name=restriction
                        )
                        menu_item.dietary_restrictions.add(restriction_obj)
                """
    except Exception as e:
        print(f"Error in populate_menu_data: {str(e)}")
        raise ValueError(f"Error processing menu data: {str(e)}")