-- 1. Retrieve Complete Menu Information for a Restaurant
-- This query fetches all menu items, organized by sections, for a specific restaurant.
SELECT 
    r.name AS restaurant_name,
    m.menu_id,
    ms.section_id,
    ms.name AS section_name,
    mi.menu_item_id,
    mi.name AS item_name,
    mi.description,
    mi.price,
    mi.currency,
    mi.status
FROM 
    restaurant r
JOIN 
    menu m ON r.restaurant_id = m.restaurant_id
JOIN 
    menu_section ms ON m.menu_id = ms.menu_id
JOIN 
    menu_item mi ON ms.section_id = mi.section_id
WHERE 
    r.restaurant_id = ? AND m.activeStatus = TRUE
ORDER BY 
    ms.name, mi.name;

-- 2. Filter Menu Items by Dietary Restrictions
-- Assuming dietary restrictions are tracked in a separate table or with an ENUM, 
-- this query filters items by a specific restriction (e.g., "vegetarian").
SELECT 
    mi.menu_item_id,
    mi.name AS item_name,
    mi.description,
    mi.price,
    mi.currency,
    ms.name AS section_name,
    r.name AS restaurant_name
FROM 
    menu_item mi
JOIN 
    menu_section ms ON mi.section_id = ms.section_id
JOIN 
    menu m ON ms.menu_id = m.menu_id
JOIN 
    restaurant r ON m.restaurant_id = r.restaurant_id
JOIN 
    MenuItemRestriction mir ON mi.menu_item_id = mir.item_id
JOIN 
    dietary_restriction dr ON mir.restriction_id = dr.restriction_id
WHERE 
    dr.restriction_type = ?; -- replace ? with the restriction type, e.g., "vegetarian"

-- 3. Track PDF Processing Status
-- This query retrieves the status of the PDF processing for a specific menu.
SELECT 
    al.log_id,
    al.menu_id,
    al.status,
    al.action,
    al.entity_affected,
    al.old_value,
    al.new_value,
    al.timestamp
FROM 
    audit_log al
JOIN 
    menu m ON al.menu_id = m.menu_id
WHERE 
    m.menu_id = ? -- replace ? with the target menu_id
ORDER BY 
    al.timestamp DESC;

-- 4. Generate Reports on Menu Items and Prices
-- Generates a report that shows each menu item with its price and currency.
SELECT 
    r.name AS restaurant_name,
    ms.name AS section_name,
    mi.name AS item_name,
    mi.price,
    mi.currency,
    mi.status
FROM 
    restaurant r
JOIN 
    menu m ON r.restaurant_id = m.restaurant_id
JOIN 
    menu_section ms ON m.menu_id = ms.menu_id
JOIN 
    menu_item mi ON ms.section_id = mi.section_id
ORDER BY 
    r.name, ms.name, mi.name;

-- 5. Handle Menu Updates and Versioning
-- a) Insert a new version of the menu
INSERT INTO menu_version (menu_id, version_number, modified_by_user_id, modifiedDate)
VALUES (?, ?, ?, NOW());

-- b) Retrieve a specific version of a menu
SELECT 
    mv.version_id,
    mv.version_number,
    mv.modifiedDate,
    mv.modified_by_user_id,
    m.menu_id,
    ms.section_id,
    ms.name AS section_name,
    mi.menu_item_id,
    mi.name AS item_name,
    mi.description,
    mi.price,
    mi.currency,
    mi.status
FROM 
    menu_version mv
JOIN 
    menu m ON mv.menu_id = m.menu_id
JOIN 
    menu_section ms ON m.menu_id = ms.menu_id
JOIN 
    menu_item mi ON ms.section_id = mi.section_id
WHERE 
    mv.menu_id = ? AND mv.version_number = ? -- replace with specific menu_id and version number
ORDER BY 
    ms.name, mi.name;

-- 6. Mark a Menu as Inactive
-- This query deactivates a menu by setting `activeStatus` to FALSE.
UPDATE 
    menu 
SET 
    activeStatus = FALSE 
WHERE 
    menu_id = ?;

-- 7. Retrieve Restaurant Opening Hours
-- Retrieves the opening hours of a restaurant by day of the week.
SELECT 
    r.name AS restaurant_name,
    oh.day_of_week,
    oh.open_time,
    oh.close_time
FROM 
    opening_hours oh
JOIN 
    restaurant r ON oh.restaurant_id = r.restaurant_id
WHERE 
    r.restaurant_id = ? -- replace ? with the target restaurant_id
ORDER BY 
    FIELD(oh.day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
