
"""
After png info has been extracted, write it to the database. 
"""

from menus.models import MenuItem, MenuSection, DietaryRestriction, AuditLog, Restaurant

def populate_menu_data(menu, menu_data: dict):
    print(f"Populating menu data for {menu}")
    try:
        # Get or create restaurant based on name
        restaurant_info = menu_data.get('restaurant_info', {})
        phone = restaurant_info.get('phone')
        address = restaurant_info.get('address')
        website = restaurant_info.get('website')
        if restaurant_info:
            restaurant_name = restaurant_info.get('restaurant_name')
            if restaurant_name:
                # Try to find existing restaurant
                existing_restaurant = Restaurant.objects.filter(name=restaurant_name).first()
                if existing_restaurant:
                    menu.restaurant = existing_restaurant 
                    if menu.restaurant.phone != phone: # Filter through possible updates
                        menu.restaurant.phone = phone
                    if menu.restaurant.street != address:
                        menu.restaurant.street = address
                    if menu.restaurant.website != website:
                        menu.restaurant.website = website
                    menu.restaurant.save()
                else:
                    # Create new restaurant if it doesn't exist
                    menu.restaurant = Restaurant.objects.create(
                        name=restaurant_name,
                        phone=phone,
                        street=address,
                        website=website
                    )
                menu.save()  # Save the menu with the restaurant reference; IS THIS NECESSARY?
        
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
