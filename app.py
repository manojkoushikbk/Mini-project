from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import mysql.connector
import random
from datetime import datetime
from functools import wraps
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Simple secret key for development

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'billing_system'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    return mysql.connector.connect(**db_config)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Home Page
@app.route('/')
def home():
    if session.get('logged_in'):
        return redirect(url_for('choose_action'))
    return render_template('home.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('choose_action'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM shop_owners WHERE username = %s AND password = %s", 
                      (username, password))
        owner = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if owner:
            session['logged_in'] = True
            session['username'] = username
            flash('Welcome back!', 'success')
            return redirect(url_for('choose_action'))
        flash('Invalid credentials. Please try again.', 'error')
        return redirect(url_for('login'))
    
    return render_template('login.html')

# Choose Action Page
@app.route('/choose-action')
@login_required
def choose_action():
    return render_template('choose_action.html', username=session.get('username'))

# Billing Page
@app.route('/billing')
@login_required
def billing():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items ORDER BY category, name")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    bill_no = str(random.randint(1000, 9999))
    return render_template('billing.html', items=items, bill_no=bill_no)

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get all items
    cursor.execute("SELECT * FROM items ORDER BY category, name")
    items = cursor.fetchall()
    
    # Get recent transactions
    cursor.execute("""
        SELECT * FROM customers 
        ORDER BY purchase_date DESC 
        LIMIT 10
    """)
    transactions = cursor.fetchall()
    
    # Get total sales
    cursor.execute("SELECT SUM(total_amount) as total_sales FROM customers")
    total_sales = cursor.fetchone()['total_sales'] or 0
    
    # Get category-wise item counts
    cursor.execute("""
        SELECT category, COUNT(*) as count, SUM(price) as total 
        FROM items 
        GROUP BY category
    """)
    category_stats = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', 
                         items=items,
                         transactions=transactions,
                         total_sales=total_sales,
                         category_stats=category_stats,
                         username=session.get('username'))

# Calculate Bill
@app.route('/calculate_bill', methods=['POST'])
@login_required
def calculate_bill():
    try:
        data = request.json
        customer_name = data['customer_name']
        phone = data['phone']
        bill_no = data['bill_no']
        items_purchased = data['items']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        total_amount = 0
        bill_details = []
        
        for item_id, qty in items_purchased.items():
            cursor.execute("SELECT name, price, category FROM items WHERE id = %s", (item_id,))
            item = cursor.fetchone()
            if item and qty > 0:
                price = float(item['price']) * qty
                total_amount += price
                bill_details.append({
                    'name': item['name'],
                    'qty': qty,
                    'price': price,
                    'category': item['category']
                })

        # Calculate taxes
        snacks_total = sum(item['price'] for item in bill_details if item['category'] == 'snacks')
        grocery_total = sum(item['price'] for item in bill_details if item['category'] == 'grocery')
        hygiene_total = sum(item['price'] for item in bill_details if item['category'] == 'hygiene')

        snacks_tax = snacks_total * 0.05
        grocery_tax = grocery_total * 0.01
        hygiene_tax = hygiene_total * 0.10

        total_amount += snacks_tax + grocery_tax + hygiene_tax

        # Save to Database
        cursor.execute("""
            INSERT INTO customers (bill_no, customer_name, phone, total_amount)
            VALUES (%s, %s, %s, %s)
        """, (bill_no, customer_name, phone, total_amount))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            'bill_no': bill_no,
            'customer_name': customer_name,
            'phone': phone,
            'items': bill_details,
            'total': total_amount,
            'snacks_tax': snacks_tax,
            'grocery_tax': grocery_tax,
            'hygiene_tax': hygiene_tax
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/add_item', methods=['POST'])
@login_required
def add_item():
    try:
        data = request.form
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (category, name, price) VALUES (%s, %s, %s)",
                      (data['category'], data['name'], data['price']))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Item added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding item: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/delete_item/<int:item_id>')
@login_required
def delete_item(item_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Item deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting item: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)