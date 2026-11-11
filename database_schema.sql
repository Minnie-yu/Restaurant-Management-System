CREATE DATABASE IF NOT EXISTS restaurant_test1;
USE restaurant_test1;

CREATE TABLE customer (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    customer_phone_number VARCHAR(20) NOT NULL,
    customer_email VARCHAR(100) UNIQUE,
    customer_address VARCHAR(255),
    customer_registration_date DATE NOT NULL
);

ALTER TABLE customer AUTO_INCREMENT = 100001;


CREATE TABLE meal (
    meal_id INT PRIMARY KEY AUTO_INCREMENT,
    meal_name VARCHAR(100) NOT NULL,
    meal_price DECIMAL(10, 2) NOT NULL,
    description TEXT
);

ALTER TABLE meal AUTO_INCREMENT = 701;


CREATE TABLE ingredient (
    ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
    ingredient_name VARCHAR(100) NOT NULL
);

ALTER TABLE ingredient AUTO_INCREMENT = 100;


CREATE TABLE customer_order (
    customer_order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    customer_order_date DATETIME NOT NULL,
    customer_delivery_date DATETIME,
    customer_delivery_address VARCHAR(255),
    customer_order_status ENUM('pending', 'processing', 'completed', 'cancelled') NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

ALTER TABLE customer_order AUTO_INCREMENT = 9001;


CREATE TABLE order_line_item (
    order_line_item_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_order_id INT NOT NULL,
    meal_id INT NOT NULL,
    meal_price DECIMAL (10,2),
    customer_quantity_ordered INT NOT NULL,
    FOREIGN KEY (customer_order_id) REFERENCES customer_order(customer_order_id),
    FOREIGN KEY (meal_id) REFERENCES meal(meal_id)
);

ALTER TABLE order_line_item AUTO_INCREMENT = 601;


CREATE TABLE meal_ingredient (
    meal_ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
    ingredient_id INT NOT NULL,
    meal_id INT NOT NULL,
    quantity_required FLOAT NOT NULL,
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id),
    FOREIGN KEY (meal_id) REFERENCES meal(meal_id)
);

ALTER TABLE meal_ingredient AUTO_INCREMENT = 501;


CREATE TABLE ingredient_purchase (
    ingredient_purchase_id INT PRIMARY KEY AUTO_INCREMENT,
    ingredient_id INT NOT NULL,
    unit_price FLOAT NOT NULL,
    quantity_on_hand INT NOT NULL,
    ingredient_expiration_date DATE,
    purchase_date DATE NOT NULL,
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
);

ALTER TABLE ingredient_purchase AUTO_INCREMENT = 801;


CREATE TABLE expense (
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    expense_type ENUM('ingredient', 'salary', 'utility', 'other') NOT NULL,
    expense_name VARCHAR(100) NOT NULL,
    expense_amount DECIMAL(10, 2) NOT NULL,
    expense_date DATE NOT NULL
);

ALTER TABLE expense AUTO_INCREMENT = 901;


INSERT INTO customer (first_name, last_name, customer_phone_number, customer_email, customer_address, customer_registration_date)
VALUES
('Emma', 'Johnson', '+1 (555) 123-4567', 'emma.johnson@example.com', '123 Elm St, San Francisco, CA 94101', '2023-01-15'),
('Michael', 'Smith', '+1 (555) 987-6543', 'michael.smith@example.com', '456 Oak Ave, New York, NY 10001', '2023-02-20'),
('Sarah', 'Williams', '+1 (555) 567-8901', 'sarah.williams@example.com', '789 Pine Rd, Chicago, IL 60601', '2023-03-10'),
('Daniel', 'Brown', '+1 (555) 234-5678', 'daniel.brown@example.com', '321 Cedar Ln, Houston, TX 77001', '2023-04-05'),
('Jennifer', 'Davis', '+1 (555) 678-9012', 'jennifer.davis@example.com', '654 Maple St, Los Angeles, CA 90001', '2023-05-22');

INSERT INTO meal (meal_name, meal_price, description)
VALUES
('Clam Chowder', 30.00, 'Creamy, savory, and often packed with flavor. Perfect for a cold day.'),
('Lobster Roll', 45.00, 'A luxurious treat with tender lobster meat, usually served with a buttery roll.'),
('Apple Pie', 25.00, 'A timeless dessert, warm, spiced, and comforting.'),
('Pot Roast', 50.00, 'Slow-cooked meat (like beef) that''s tender and flavorful, often served with vegetables.'),
('Cornbread', 15.00, 'A great side dish, often sweet or savory, adding a nice texture and flavor.');

INSERT INTO ingredient (ingredient_name)
VALUES
('Container'),
('Clams'),
('Potatoes'),
('Onions'),
('Celery'),
('Heavy Cream'),
('Bread Bowl'),
('Lobster Meat'),
('Mayonnaise'),
('Warm Butter'),
('Toasted Split-Top Buns'),
('Coleslaw or Kettle Chips'),
('Apples'),
('Cinnamon'),
('Nutmeg'),
('Butter'),
('Flour'),
('Sugar'),
('Beef Chuck Roast'),
('Carrots'),
('Red Wine or Broth'),
('Beef Bouillon Cube'),
('Cornmeal'),
('Buttermilk'),
('Eggs'),
('Peppers'),
('Sesame or Scallions');

INSERT INTO meal_ingredient (ingredient_id, meal_id, quantity_required)
VALUES
(101, 701, 2),
(102, 701, 4),
(103, 701, 1),
(104, 701, 2),
(105, 701, 1),
(106, 701, 1),
(100, 701, 1),
(107, 702, 1),
(108, 702, 0.25),
(109, 702, 0.25),
(110, 702, 4),
(111, 702, 0.5),
(100, 702, 1),
(112, 703, 6),
(113, 703, 1.5),
(114, 703, 0.5),
(115, 703, 0.5),
(116, 703, 2.5),
(117, 703, 0.75),
(100, 703, 1),
(118, 704, 3),
(119, 704, 4),
(120, 704, 2),
(121, 704, 2),
(103, 704, 3),
(104, 704, 2),
(100, 704, 1),
(122, 705, 1.5),
(123, 705, 1.5),
(124, 705, 0.25),
(125, 705, 2),
(126, 705, 0.5),
(115, 705, 0.5),
(100, 705, 1);

INSERT INTO ingredient_purchase (ingredient_id, unit_price, quantity_on_hand, ingredient_expiration_date, purchase_date)
VALUES
(100, 1, 500, '2026-08-30', '2025-05-01'),
(101, 5.5, 120, '2025-07-25', '2025-06-25'),
(101, 5.5, 60, '2025-07-19', '2025-06-19'),
(101, 5.5, 150, '2025-07-02', '2025-06-02'),
(102, 0.75, 100, '2025-06-30', '2025-06-01'),
(103, 0.5, 130, '2025-06-30', '2025-06-01'),
(104, 0.3, 80, '2025-06-23', '2025-06-01'),
(104, 0.3, 40, '2025-07-29', '2025-07-01'),
(105, 3.5, 40, '2027-06-10', '2025-06-03'),
(106, 2.5, 40, '2025-07-28', '2025-06-19'),
(106, 2.5, 50, '2025-06-28', '2025-06-02'),
(107, 19, 50, '2025-06-28', '2025-06-01'),
(107, 19, 0, '2025-07-15', '2025-06-15'),
(108, 2.5, 80, '2026-06-19', '2025-06-02'),
(108, 2.5, 40, '2025-07-04', '2025-06-15'),
(109, 3.5, 40, '2026-08-29', '2025-07-01'),
(109, 3.5, 80, '2026-03-12', '2025-06-01'),
(110, 1.75, 130, '2025-07-15', '2025-06-24'),
(110, 1.75, 150, '2025-06-20', '2025-06-03'),
(111, 1.5, 80, '2025-09-30', '2025-06-03'),
(112, 1.75, 40, '2025-07-14', '2025-06-01'),
(113, 0.75, 50, '2025-08-30', '2025-06-01'),
(113, 0.75, 30, '2025-11-30', '2025-08-01'),
(114, 0.75, 80, '2025-08-20', '2025-06-01'),
(115, 3.5, 90, '2025-12-24', '2025-06-30'),
(115, 3.5, 120, '2025-09-18', '2025-06-01'),
(116, 0.75, 120, '2025-08-14', '2025-06-03'),
(117, 0.4, 50, '2025-12-30', '2025-06-03'),
(118, 5.5, 50, '2025-07-30', '2025-07-01'),
(118, 5.5, 100, '2025-06-30', '2025-06-01'),
(119, 0.75, 110, '2025-06-27', '2025-06-02'),
(120, 8, 80, '2025-09-11', '2025-06-01'),
(121, 1, 70, '2026-08-13', '2025-06-01'),
(121, 1, 40, '2025-09-20', '2025-06-25'),
(122, 2, 50, '2025-10-14', '2025-06-03'),
(123, 1, 40, '2025-11-14', '2025-06-01'),
(124, 0.3, 30, '2025-08-05', '2025-06-25'),
(124, 0.3, 80, '2025-07-05', '2025-06-01'),
(125, 0.5, 40, '2025-07-15', '2025-07-01'),
(125, 0.5, 60, '2025-06-13', '2025-06-01'),
(126, 1, 40, '2025-12-14', '2025-06-02');

INSERT INTO expense (expense_type, expense_name, expense_amount, expense_date)
VALUES
('salary', 'Labor Costs', 10000.00, '2025-07-15'),
('other', 'Rent', 3500.00, '2025-07-15'),
('utility', 'Utilities', 2000.00, '2025-07-15'),
('other', 'Overhead Costs', 1000.00, '2025-07-15');

-- customer order 9001
INSERT INTO customer_order (customer_id, customer_order_date, customer_delivery_date, customer_delivery_address, customer_order_status)
VALUES (100001, '2023-06-01 00:00:00', '2023-06-03 14:30:00', '123 Elm St, San Francisco, CA 94101', 'completed');
SET @current_customer_order_id = LAST_INSERT_ID();
INSERT INTO order_line_item (customer_order_id, meal_id, meal_price, customer_quantity_ordered) VALUES (@current_customer_order_id, 701, 12, 2);
INSERT INTO order_line_item (customer_order_id, meal_id, meal_price, customer_quantity_ordered) VALUES (@current_customer_order_id, 703, 5.5, 1);

-- customer order 9002
INSERT INTO customer_order (customer_id, customer_order_date, customer_delivery_date, customer_delivery_address, customer_order_status)
VALUES (100002, '2023-06-02 00:00:00', '2023-06-05 10:15:00', '456 Oak Ave, New York, NY 10001', 'completed');
SET @current_customer_order_id = LAST_INSERT_ID();
INSERT INTO order_line_item (customer_order_id, meal_id, meal_price, customer_quantity_ordered) VALUES (@current_customer_order_id, 702, 32, 1);
INSERT INTO order_line_item (customer_order_id, meal_id, meal_price, customer_quantity_ordered) VALUES (@current_customer_order_id, 705, 7, 2);

-- customer order 9003
INSERT INTO customer_order (customer_id, customer_order_date, customer_delivery_date, customer_delivery_address, customer_order_status)
VALUES (100003, '2023-06-03 00:00:00', '2023-06-04 16:45:00', '789 Pine Rd, Chicago, IL 60601', 'completed');
SET @current_customer_order_id = LAST_INSERT_ID();
INSERT INTO order_line_item (customer_order_id, meal_id, meal_price, customer_quantity_ordered) VALUES (@current_customer_order_id, 704, 18.5, 3);
INSERT INTO order_line_item (customer_order_id, meal_id, meal_price, customer_quantity_ordered) VALUES (@current_customer_order_id, 701, 12, 1);

-- customer order 9004
INSERT INTO customer_order (customer_id, customer_order_date, customer_delivery_date, customer_delivery_address, customer_order_status)
VALUES (100004, '2023-06-04 00:00:00', '2023-06-06 09:00:00', '321 Cedar Ln, Houston, TX 77001', 'completed');
SET @current_customer_order_id = LAST_INSERT_ID();
INSERT INTO order_line_item (customer_order_id, meal_id, meal_price, customer_quantity_ordered) VALUES (@current_customer_order_id, 705, 7, 4);

-- customer order 9005
INSERT INTO customer_order (customer_id, customer_order_date, customer_delivery_date, customer_delivery_address, customer_order_status)
VALUES (100005, '2023-06-05 00:00:00', '2023-06-07 11:30:00', '654 Maple St, Los Angeles, CA 90001', 'completed');
SET @current_customer_order_id = LAST_INSERT_ID();
INSERT INTO order_line_item (customer_order_id, meal_id, meal_price, customer_quantity_ordered) VALUES (@current_customer_order_id, 703, 5.5, 2);

-- customer order 9006
INSERT INTO customer_order (customer_id, customer_order_date, customer_delivery_date, customer_delivery_address, customer_order_status)
VALUES (100001, '2023-06-06 00:00:00', '2023-06-08 15:00:00', '123 Elm St, San Francisco, CA 94101', 'completed');
SET @current_customer_order_id = LAST_INSERT_ID();
INSERT INTO order_line_item (customer_order_id, meal_id, meal_price, customer_quantity_ordered) VALUES (@current_customer_order_id, 702, 32, 1);

-- customer order 9007
INSERT INTO customer_order (customer_id, customer_order_date, customer_delivery_date, customer_delivery_address, customer_order_status)
VALUES (100003, '2023-06-07 00:00:00', '2023-06-09 13:15:00', '789 Pine Rd, Chicago, IL 60601', 'completed');
SET @current_customer_order_id = LAST_INSERT_ID();
INSERT INTO order_line_item (customer_order_id, meal_id, meal_price, customer_quantity_ordered) VALUES (@current_customer_order_id, 704, 18.5, 2);
