
"""
After pdf info has been extracted, write it to the database. 
"""

import json
from menus.models import Menu, MenuItem, MenuSection, DietaryRestriction, AuditLog

def populate_menu_data(menu: Menu, menu_data: dict):
    print(f"Populating menu data for {menu}")
    # ai_process_log = AuditLog.objects.create(
    #     menu_version=menu.version,
    #     phase="Populating data",
    #     status="Processing"
    # )
    try:
        # Populate the restaurant info that was left empty from the restaurant info in the menu version
        restaurant_info = menu_data.get('restaurant_info', {})
        if restaurant_info:
            restaurant = menu.restaurant
            restaurant.name = restaurant_info.get('restaurant_name', restaurant.name)
            restaurant.phone = restaurant_info.get('phone', restaurant.phone)
            restaurant.street = restaurant_info.get('address', restaurant.street)
            restaurant.website = restaurant_info.get("website", restaurant.website)
            restaurant.save() # Write to the database 
        
        # Create menu sections and populate them with items 
        for section_data in menu_data.get('menu_sections', []):
            section = MenuSection.objects.create(
                menu=menu,
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
                
                # Handle dietary restrictions properly
                dietary_restrictions = item_data.get('dietary_restrictions', [])
                if dietary_restrictions:
                    for restriction in dietary_restrictions:
                        restriction_obj, _ = DietaryRestriction.objects.get_or_create(
                            name=restriction
                        )
                        menu_item.dietary_restrictions.add(restriction_obj)
            
        # ai_process_log.status = "Processed"
        # ai_process_log.save()
                
    except Exception as e:
        print(f"Error in populate_menu_data: {str(e)}")
        # ai_process_log.status = "Failed"
        # ai_process_log.other = str(e)
        # ai_process_log.save()
        raise ValueError(f"Error processing menu data: {str(e)}")
