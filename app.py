from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create SQLite database connection and cursor
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        unit TEXT,
        rate REAL,
        quantity INTEGER,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
''')
conn.commit()

@app.route('/grocery_store')
def grocery_store():
    return render_template('grocery_store.html')

'''@app.route('/manager_login')
def manager_login():
    return render_template('manager_login.html')'''

@app.route('/user_login')
def user_login():
    return render_template('user_login.html')

@app.route('/manager_login', methods=['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Perform user authentication here (e.g., query your database)
        # Replace this with your authentication logic
        if username == 'manager' and password == 'password':
            session['username'] = username
            return redirect('/manager_dashboard')

    return render_template('manager_login.html')


@app.route('/manager_dashboard')
def manager_dashboard():
    if 'username' in session:
        # Fetch categories from the database
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        return render_template('manager_dashboard.html', username=session['username'], categories=categories)
    else:
        return redirect('/manager_login')

@app.route('/manage_category', methods=['GET', 'POST'])
def manage_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
        conn.commit()
        return redirect('/manager_dashboard')
    return render_template('manage_category.html', username='Manager')

@app.route('/manage_product/<int:category_id>', methods=['GET', 'POST'])
def manage_product(category_id):
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        unit = request.form.get('unit')
        rate = float(request.form.get('rate'))
        quantity = int(request.form.get('quantity'))

        cursor.execute("INSERT INTO products (name, unit, rate, quantity, category_id) VALUES (?, ?, ?, ?, ?)",
                       (product_name, unit, rate, quantity, category_id))
        conn.commit()
        return redirect('/manager_dashboard')
    
    # Fetch category details
    cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
    category = cursor.fetchone()

    return render_template('manage_product.html', username='Manager', category=category)
@app.route('/user_dashboard/<username>')
def user_dashboard(username):
    # Fetch categories and products from the database
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    return render_template('user_dashboard.html', username=username, categories=categories)

@app.route('/buy_product/<int:product_id>', methods=['GET', 'POST'])
def buy_product(product_id):
    # Fetch product details from the database
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if request.method == 'POST':
        quantity = int(request.form.get('quantity'))
        if quantity <= product['quantity']:
            # Perform the buying action (add to cart, update quantity, etc.)
            return redirect(url_for('cart'))
        else:
            error_message = "This quantity is out of stock."
            return render_template('buy_product.html', username='User', product=product, error_message=error_message)
    
    return render_template('buy_product.html', username='User', product=product)

@app.route('/user_profile/<username>')
def user_profile(username):
    # Fetch user profile data from the database
    # Assuming you have a users table with a username and password columns
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_profile_data = cursor.fetchone()
    
    return render_template('user_profile.html', username=username, user_profile_data=user_profile_data)

@app.route('/cart')
def cart():
    # Fetch user's cart data from the database
    # Implement the logic to retrieve cart items, quantities, prices, etc.
    cart_data = []  # Placeholder
    
    return render_template('cart.html', username='User', cart_data=cart_data)

# ... (Add more routes as needed)


if __name__ == '__main__':
    app.run(debug=True)
