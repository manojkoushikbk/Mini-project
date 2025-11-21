-- Create the database
CREATE DATABASE IF NOT EXISTS billing_system;
USE billing_system;

-- Create shop_owners table
CREATE TABLE IF NOT EXISTS shop_owners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL,  -- For SHA-256 hashed passwords
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create items table
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category ENUM('grocery', 'snacks', 'hygiene') NOT NULL,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_no VARCHAR(20) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    total_amount DECIMAL(10, 2) NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user (password: admin123)
INSERT INTO shop_owners (username, password) 
VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9')
ON DUPLICATE KEY UPDATE username=username;

-- Insert sample items
INSERT INTO items (category, name, price) VALUES
('grocery', 'Rice 1kg', 2.50),
('grocery', 'Wheat Flour 1kg', 1.80),
('grocery', 'Sugar 1kg', 1.20),
('snacks', 'Potato Chips', 1.00),
('snacks', 'Chocolate Bar', 0.75),
('hygiene', 'Soap', 0.90),
('hygiene', 'Shampoo', 3.50),
('hygiene', 'Toothpaste', 2.00)
ON DUPLICATE KEY UPDATE name=name;