from flask import Flask, redirect, render_template, jsonify, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'checkproductexpiration.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = "}:I{n,)PFQ(OYV[sW[Mh-ZShd-cO.R}4" # Required for flash messages

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Use db.Date for YYYY-MM-DD format
    expiration_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

with app.app_context():
    # Create the table
    db.create_all()

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/viewaddproduct', methods=['GET'])
def view_add_product():
    return render_template('view_add_product.html')

@app.route('/viewexpiredproducts', methods=['GET'])
def view_expired_products():
    all_products = Product.query.order_by(Product.expiration_date.asc()).all()
    # Pass them to the template as a variable named 'products'
    return render_template('view_expired_products.html', products=all_products)

@app.route('/add_product', methods=['POST'])
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

@app.route('/update-expired-product', methods=['POST'])
def update_expired_product():
    data = request.json
    product_id = data.get('id')
    field = data.get('field')
    value = data.get('value')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404

    try:
        if field == 'name':
            product.name = value
        elif field == 'expiration_date':
            # Convert the string "YYYY-MM-DD" back to a Python date object
            product.expiration_date = datetime.strptime(value, '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400

@app.after_request
def add_header(response):
    response.headers['Permissions-Policy'] = 'unload=(self)'
    return response

if __name__ == '__main__':
    app.run(debug=True)
