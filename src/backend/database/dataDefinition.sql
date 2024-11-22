-- See documentation of indexes here: 
-- https://docs.google.com/spreadsheets/d/1uw-jabrRVzGIta0XbzHYRbZJI8LuYw87DzQga-fYs1c/edit?usp=sharing

CREATE DATABASE IF NOT EXISTS menu_management_system;

USE menu_management_system;

-- User Table
CREATE TABLE IF NOT EXISTS user (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    userName VARCHAR(50) UNIQUE NOT NULL, -- Unique Index for quick lookup
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
    permissions ENUM('admin', 'user') NOT NULL,
    INDEX (email), -- Index for frequent email lookups
    INDEX user_id_name_email (user_id, userName, email), -- Composite Index
    INDEX user_location (country, city, state, zip, street) -- Composite Index
);

-- Menu Info Table
CREATE TABLE IF NOT EXISTS menu (
    menu_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT NOT NULL,
    section VARCHAR(50) NOT NULL,
    activeStatus BOOLEAN DEFAULT TRUE,
    available_until DATE,
    available_from DATE,
    timeUpload TIMESTAMP,
    menu_version INT NOT NULL,
    user_id INT NOT NULL,
    menu_file BLOB NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id),
    FOREIGN KEY (menu_version) REFERENCES menu_version(counter),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    INDEX availability (available_from, available_until) -- Composite Index
);

-- Menu Section Table
CREATE TABLE IF NOT EXISTS menu_section (
    section_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(99) NOT NULL
);

-- Menu Sections Bridge
CREATE TABLE IF NOT EXISTS menu_sections_menus (
    menu_id INT NOT NULL,
    section_id INT NOT NULL,
    PRIMARY KEY (menu_id, section_id), -- Composite primary key
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id),
    FOREIGN KEY (section_id) REFERENCES menu_section(section_id),
    INDEX (menu_id), -- Index for frequent menu lookups
    INDEX (section_id) -- Index for frequent section lookups
);

-- Menu Version Table
CREATE TABLE IF NOT EXISTS menu_version (
    restaurant_id INT NOT NULL,
    counter INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (restaurant_id, counter), -- Composite primary key that enforces uniqueness
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id)
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
    FOREIGN KEY (section_id) REFERENCES menu_section(section_id),
    INDEX (name), -- Index for frequent item name lookups
    INDEX (section_id) -- Index for joining with menu_section
);

-- Dietary Restrictions Table
CREATE TABLE IF NOT EXISTS dietary_restrictions (
    dietary_restrict_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(99) NOT NULL
);

-- Item Dietary Restrictions Bridge Table
CREATE TABLE IF NOT EXISTS item_dietary_restrictions (
    menu_item_id INT NOT NULL,
    dietary_restrict_id INT NOT NULL,
    PRIMARY KEY (menu_item_id, dietary_restrict_id), -- Composite Primary Key
    FOREIGN KEY (menu_item_id) REFERENCES menu_item(menu_item_id),
    FOREIGN KEY (dietary_restrict_id) REFERENCES dietary_restrictions(dietary_restrict_id),
    INDEX (menu_item_id), -- Index for joins
    INDEX (dietary_restrict_id) -- Index for joins
);

-- Restaurant Table
CREATE TABLE IF NOT EXISTS restaurant (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(50),
    country VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(3),
    zip SMALLINT,
    street VARCHAR(50),
    website VARCHAR(99),
    INDEX (name), -- Index for restaurant name search
    INDEX restaurant_location (country, city, state, zip, street), -- Composite Index for location
    INDEX contact_info (name, phone, email, website) -- Composite Index for contact details
);

-- Audit Log Table
CREATE TABLE IF NOT EXISTS audit_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    menu_id INT NOT NULL,
    status ENUM('received', 'processed', 'uploaded') NOT NULL,
    time_registered TIMESTAMP NOT NULL,
    other VARCHAR(99),
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id),
    INDEX (menu_id) -- Index to speed up joins with menu
);
