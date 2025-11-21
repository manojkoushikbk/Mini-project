-- Create database
CREATE DATABASE IF NOT EXISTS billing_system;
USE billing_system;

-- Create shop_owners table
CREATE TABLE shop_owners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create items table
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category ENUM('grocery', 'snacks', 'hygiene') NOT NULL,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Create customers table
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_no VARCHAR(20) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    total_amount DECIMAL(10, 2) NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create billing_items table
CREATE TABLE billing_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_no VARCHAR(20) NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(id)
);

-- Insert admin user
INSERT INTO shop_owners (username, password) VALUES ('admin', 'admin123');

-- Insert Grocery Items
INSERT INTO items (category, name, price) VALUES
('grocery', 'Rice 1kg', 45.00),
('grocery', 'Wheat Flour 1kg', 40.00),
('grocery', 'Sugar 1kg', 35.00),
('grocery', 'Toor Dal 1kg', 120.00),
('grocery', 'Cooking Oil 1L', 180.00),
('grocery', 'Salt 1kg', 20.00),
('grocery', 'Milk 1L', 60.00),
('grocery', 'Tea Powder 250g', 55.00),
('grocery', 'Coffee Powder 250g', 150.00),
('grocery', 'Turmeric Powder 100g', 35.00),
('grocery', 'Red Chilli Powder 100g', 40.00),
('grocery', 'Basmati Rice 1kg', 90.00),
('grocery', 'Moong Dal 1kg', 130.00),
('grocery', 'Rajma 500g', 80.00),
('grocery', 'Poha 500g', 45.00);

-- Insert Snacks Items
INSERT INTO items (category, name, price) VALUES
('snacks', 'Lays Chips Large', 40.00),
('snacks', 'Kurkure Large', 30.00),
('snacks', 'Biscuits Parle-G', 10.00),
('snacks', 'Good Day Cookies', 30.00),
('snacks', 'Hide & Seek', 35.00),
('snacks', 'Maggi Noodles', 14.00),
('snacks', 'Haldiram Mixture 200g', 50.00),
('snacks', 'Bourbon Biscuits', 25.00),
('snacks', 'Uncle Chips', 20.00),
('snacks', 'Pringles', 85.00),
('snacks', 'Oreo Cookies', 30.00),
('snacks', 'Nachos', 40.00),
('snacks', 'Popcorn', 20.00),
('snacks', 'Choco Pie (Pack of 6)', 60.00),
('snacks', 'Dark Fantasy', 40.00);

-- Insert Hygiene Items
INSERT INTO items (category, name, price) VALUES
('hygiene', 'Dettol Soap', 35.00),
('hygiene', 'Dove Soap', 45.00),
('hygiene', 'Colgate Toothpaste', 55.00),
('hygiene', 'Pepsodent Toothpaste', 45.00),
('hygiene', 'Closeup Toothpaste', 50.00),
('hygiene', 'Head & Shoulders Shampoo 200ml', 160.00),
('hygiene', 'Dove Shampoo 200ml', 180.00),
('hygiene', 'Clinic Plus Shampoo 200ml', 140.00),
('hygiene', 'Dettol Hand Wash', 99.00),
('hygiene', 'Lifebuoy Hand Sanitizer', 50.00),
('hygiene', 'Gillette Shaving Cream', 140.00),
('hygiene', 'Pears Soap', 45.00),
('hygiene', 'Nivea Body Lotion 200ml', 180.00),
('hygiene', 'Vaseline Body Lotion 200ml', 170.00),
('hygiene', 'Dettol Antiseptic Liquid 100ml', 80.00); 