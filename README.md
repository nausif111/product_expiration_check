# Product Expiration Check

![GitHub](https://img.shields.io/badge/GitHub-Public-green)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-brightgreen)

A simple Flask app to track product expiration dates and edit inventory from the browser.

## 🌟 What it does

- Provides a login page for authenticated access
- Lets you add new products with expiration dates
- Displays all products sorted by expiration date
- Lets you edit product names and expiration dates inline

## ✅ Features

- Flask-based web app
- SQLite database (`checkproductexpiration.db`)
- Flask-Login authentication
- Inline editing for product name and expiration date
- Flash notifications for actions

## 🚀 Setup

```bash
cd /Users/user/Documents/Projects/Python/product_expiration_check
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> If you don't have a `requirements.txt` file yet, install:
>
> ```bash
> pip install flask flask-login flask-sqlalchemy
> ```

## ▶️ Run the app

```bash
source venv/bin/activate
python app.py
```

Then open: `http://127.0.0.1:5000`

## 🔐 Default login

The app creates an admin user from your `.env` file:

- Username: `ADMIN_USERNAME` (default: `admin`)
- Password: `ADMIN_PASSWORD` (default: `admin123`)

> Create a `.env` file in the project root with your own credentials:
>
> ```env
> ADMIN_USERNAME=your_username
> ADMIN_PASSWORD=your_secure_password
> ```

## 📁 Important files

- `app.py` — main Flask app and route definitions
- `models.py` — SQLAlchemy models for `User` and `Product`
- `templates/` — HTML pages for login, home, add product, expired products
- `css/` — app styling
- `checkproductexpiration.db` — local SQLite database file

## 🧠 Routes

- `/login` — login page
- `/logout` — log out
- `/` — main dashboard (requires login)
- `/viewaddproduct` — add new product form
- `/viewexpiredproducts` — list products and edit them
- `/add_product` — POST route to add a product
- `/update-expired-product` — POST route to save inline edits
- `/viewcurrentmonthexpiredproducts` — GET route to fetch current month products about to expire


## 💡 Notes

- The edit table sends edits using JavaScript fetch requests to the backend.
- Inline editing works for both the product name and expiration date.
- If you want CSRF protection, install `Flask-WTF` and add `CSRFProtect`.

## 📦 Dependencies

A lightweight dependency file is included so the project is easy to install:

```bash
pip install -r requirements.txt
```

## 📌 Publish to GitHub

If your project is not already initialized as a repo:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
```

Then create a GitHub repository and add the remote:

```bash
git remote add origin https://github.com/<your-username>/product_expiration_check.git
git push -u origin main
```

If you use GitHub CLI:

```bash
gh auth login
gh repo create <your-username>/product_expiration_check --public --source=. --remote=origin --push
```

## 💡 Notes

- `requirements.txt` contains the core Flask dependencies used by this app.
- Replace `<your-username>` with your GitHub account name.

Enjoy building and publishing your repo!