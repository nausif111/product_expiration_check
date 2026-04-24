import os
from datetime import datetime
from flask import Flask, redirect, render_template, jsonify, request, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Product # Importing from our new models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'checkproductexpiration.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "}:I{n,)PFQ(OYV[sW[Mh-ZShd-cO.R}4"

# Initialize DB and LoginManager
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Where to redirect unauthorized users

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- AUTH ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main'))
        
        flash("Invalid username or password", "error")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- PRODUCT ROUTES (NOW PROTECTED) ---

@app.route('/')
@login_required
def main():
    return render_template('home.html')

@app.route('/viewexpiredproducts', methods=['GET'])
@login_required
def view_expired_products():
    all_products = Product.query.order_by(Product.expiration_date.asc()).all()
    # Pass them to the template as a variable named 'products'
    return render_template('view_expired_products.html', products=all_products)


@app.route('/update-expired-product', methods=['POST'])
@login_required
def update_expired_product():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid payload'}), 400

    product_id = data.get('id')
    field = data.get('field')
    value = data.get('value')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'status': 'error', 'message': 'Product not found'}), 404

    try:
        if field == 'name':
            product.name = value
        elif field == 'expiration_date':
            product.expiration_date = datetime.strptime(value, '%Y-%m-%d').date()
        else:
            return jsonify({'status': 'error', 'message': 'Invalid field'}), 400

        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/viewaddproduct', methods=['GET'])
@login_required
def view_add_product():
    return render_template('view_add_product.html')


@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    name = request.form.get('name')
    expiry_str = request.form.get('expiry')
    
    try:
        if not name or not expiry_str:
            flash("Please fill out all fields!", "error")
        else:
            expiry_date = datetime.strptime(expiry_str, '%Y-%m-%d').date()
            new_product = Product(name=name, expiration_date=expiry_date)
            db.session.add(new_product)
            db.session.commit()
            flash(f"Product '{name}' added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error adding product: {str(e)}", "error")
        
    return redirect(url_for('view_add_product'))

# Helper to create tables and a dummy user
with app.app_context():
    db.create_all()
    # Create a test user if one doesn't exist
    if not User.query.filter_by(username='admin').first():
        test_user = User(username='admin')
        test_user.set_password('admin123')
        db.session.add(test_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)