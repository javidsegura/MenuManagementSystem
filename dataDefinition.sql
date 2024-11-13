-- User table
CREATE TABLE user (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    userName VARCHAR(50) UNIQUE NOT NULL,
    userPassword VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(3) NOT NULL,
    zip VARCHAR(5) NOT NULL,
    street VARCHAR(50) NOT NULL,
    joinedDate TIMESTAMP NOT NULL
);

-- Posts table
CREATE TABLE posts (
    post_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    uploadTime TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);

-- Restaurant table
CREATE TABLE restaurant (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(50),
    country VARCHAR(50),
    city VARCHAR(50),
    state_region VARCHAR(3),
    zip VARCHAR(5),
    street VARCHAR(50)
);

-- Menu table
CREATE TABLE menu (
    menu_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT NOT NULL,
    section VARCHAR(50),
    type ENUM('breakfast', 'lunch', 'dinner', 'other') NOT NULL,
    activeStatus BOOL DEFAULT TRUE,
    available_until DATE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id) ON DELETE CASCADE
);

-- Menu Version table for version control
CREATE TABLE menu_version (
    version_id INT PRIMARY KEY AUTO_INCREMENT,
    menu_id INT NOT NULL,
    version_number INT NOT NULL,
    modified_by_user_id INT NOT NULL,
    modifiedDate TIMESTAMP NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id) ON DELETE CASCADE,
    FOREIGN KEY (modified_by_user_id) REFERENCES user(user_id) ON DELETE SET NULL,
    UNIQUE (menu_id, version_number)
);

-- Audit Log table for logging changes
CREATE TABLE audit_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    menu_id INT NOT NULL,
    status ENUM('received', 'processed', 'uploaded') NOT NULL,
    action VARCHAR(99) NOT NULL,
    entity_affected VARCHAR(99) NOT NULL,
    old_value JSON,
    new_value JSON,
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id) ON DELETE CASCADE
);

-- Menu Section table
CREATE TABLE menu_section (
    section_id INT PRIMARY KEY AUTO_INCREMENT,
    menu_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id) ON DELETE CASCADE
);

-- Menu Item table with adjusted data type for price
CREATE TABLE menu_item (
    menu_item_id INT PRIMARY KEY AUTO_INCREMENT,
    section_id INT NOT NULL,
    name VARCHAR(99) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status ENUM('active', 'inactive') NOT NULL,
    FOREIGN KEY (section_id) REFERENCES menu_section(section_id) ON DELETE CASCADE
);

-- Opening Hours table directly linked to restaurant
CREATE TABLE opening_hours (
    opening_hours_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT NOT NULL,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id) ON DELETE CASCADE
);
