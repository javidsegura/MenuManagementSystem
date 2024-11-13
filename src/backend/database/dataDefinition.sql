
CREATE DATABASE IF NOT EXISTS menu_manager;

USE menu_manager;


-- User Table
CREATE TABLE IF NOT EXISTS user (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    userName VARCHAR(50) UNIQUE NOT NULL,
    PasswordHash VARCHAR(50) NOT NULL,        
    email VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(3) NOT NULL,         
    zip SMALLINT NOT NULL,
    street VARCHAR(50) NOT NULL,
    joinedDate TIMESTAMP NOT NULL,
    permissions ENUM('admin', 'user') NOT NULL 
);

-- Posts Table
CREATE TABLE IF NOT EXISTS posts (
    post_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    uploadTime TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- Menu Version Table
CREATE TABLE IF NOT EXISTS menu_version (
    menu_version INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    post_id INT,
    timeUpload TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

-- Restaurant Table
CREATE TABLE IF NOT EXISTS restaurant (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(3) NOT NULL,               
    zip SMALLINT NOT NULL,
    street VARCHAR(50) NOT NULL
);

-- Opening Hours Table
CREATE TABLE IF NOT EXISTS opening_hours (
    opening_hours_id INT PRIMARY KEY AUTO_INCREMENT,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
);

-- Opening Hours Bridge Table
CREATE TABLE IF NOT EXISTS opening_hours_bridge (
    restaurant_id INT NOT NULL,
    opening_hours_id INT NOT NULL,
    PRIMARY KEY (restaurant_id, opening_hours_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id),
    FOREIGN KEY (opening_hours_id) REFERENCES opening_hours(opening_hours_id)
);

-- Menu Table
CREATE TABLE IF NOT EXISTS menu_info (
    menu_id INT PRIMARY KEY AUTO_INCREMENT,
    menu_section INT NOT NULL,                  
    section VARCHAR(50),
    activeStatus BOOLEAN DEFAULT TRUE,
    available_until DATE,
    available_from DATE,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(3) NOT NULL,                 
    zip SMALLINT NOT NULL,
    street VARCHAR(50) NOT NULL,
    FOREIGN KEY (menu_section) REFERENCES menu_section(section_id)
);

-- Menu Section Table
CREATE TABLE IF NOT EXISTS menu_section (
    section_id INT PRIMARY KEY AUTO_INCREMENT,
    menu_id INT NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
);

-- Menu Item Table
CREATE TABLE IF NOT EXISTS menu_item (
    menu_item_id INT PRIMARY KEY AUTO_INCREMENT,
    section_id INT NOT NULL,
    name VARCHAR(99) NOT NULL,
    description VARCHAR(99) NOT NULL,
    price INT NOT NULL,
    currency VARCHAR(99) DEFAULT 'dollar',
    available BOOLEAN NOT NULL,
    FOREIGN KEY (section_id) REFERENCES menu_section(section_id)
);

-- Dietary Restrictions Table
CREATE TABLE IF NOT EXISTS dietary_restrictions (
    dietary_restrict_id INT PRIMARY KEY AUTO_INCREMENT,
    description VARCHAR(99) NOT NULL,
);

-- Item Dietary Restrictions Bridge Table
CREATE TABLE IF NOT EXISTS item_dietary_restrictions (
    menu_item_id INT NOT NULL,
    dietary_restrict_id INT NOT NULL,
    PRIMARY KEY (menu_item_id, dietary_restrict_id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_item(menu_item_id),
    FOREIGN KEY (dietary_restrict_id) REFERENCES dietary_restrictions(dietary_restrict_id)
);

-- Audit Log Table
CREATE TABLE IF NOT EXISTS audit_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    menu_id INT NOT NULL,
    status ENUM('received', 'processed', 'uploaded') NOT NULL,
    action VARCHAR(99) NOT NULL,
    entity_affected VARCHAR(99) NOT NULL,
    old_value VARCHAR(99),
    new_value VARCHAR(99),
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
);