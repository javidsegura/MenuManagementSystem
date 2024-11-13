
-- Please note, this code has not compleltey being reviewed and may contain errors

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

CREATE TABLE restaurant (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    menu_id INT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state_region VARCHAR(50) NOT NULL,
    zip SMALLINT NOT NULL,
    street VARCHAR(50) NOT NULL
);

CREATE TABLE opening_hours (
    opening_hours_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT NOT NULL,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id)
);

CREATE TABLE opening_hours_bridge (
    restaurant_id INT NOT NULL,
    opening_hours_id INT NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id),
    FOREIGN KEY (opening_hours_id) REFERENCES opening_hours(opening_hours_id)
);

CREATE TABLE menu (
    menu_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT NOT NULL,
    section VARCHAR(50) NOT NULL,
    type ENUM('breakfast', 'lunch', 'dinner', 'other') NOT NULL,
    activeStatus BOOLEAN DEFAULT TRUE,
    available_until DATE,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state_region VARCHAR(50) NOT NULL,
    zip SMALLINT NOT NULL,
    street VARCHAR(50) NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id)
);

CREATE TABLE menu_version (
    version_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    menu_id INT NOT NULL,
    modifiedDate TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
);

CREATE TABLE menu_section (
    section_id INT PRIMARY KEY AUTO_INCREMENT,
    menu_id INT NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
);

CREATE TABLE menu_item (
    menu_item INT PRIMARY KEY AUTO_INCREMENT,
    section_id INT NOT NULL,
    name VARCHAR(99) NOT NULL,
    description VARCHAR(99) NOT NULL,
    price INT NOT NULL,
    currency VARCHAR(99) DEFAULT 'dollar',
    status BOOLEAN NOT NULL,
    FOREIGN KEY (section_id) REFERENCES menu_section(section_id)
);

CREATE TABLE posts (
    post_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    menu_id INT NOT NULL,
    uploadTime TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE audit_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    menu_id INT NOT NULL,
    status ENUM('received', 'processed', 'uploaded') NOT NULL,
    action VARCHAR(99) NOT NULL,
    entity_affected VARCHAR(99) NOT NULL,
    old_value VARCHAR(99),
    new_value VARCHAR(99),
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
);
