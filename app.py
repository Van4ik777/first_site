from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import timedelta, datetime

import secrets

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    remember_token = db.Column(db.String(100), unique=True)


@login_manager.user_loader
def load_user(user_id):
    if 'remember_token' in session:
        user = User.query.get(int(user_id))
        if user.remember_token == session['remember_token']:
            return user
    return User.query.get(int(user_id))


@app.route('/')
def main_site():
    return render_template("main_site.html")

@app.route('/sale')
def sale():
    if not current_user.is_authenticated:
        flash('Для получить скидки необходимо войти в систему', 'error')
        return redirect(url_for('main_site'))
    return render_template("sale.html")


@app.route('/product_page_1')
def product_page_1():
    return render_template("product_page_1.html")

@app.route('/product_page_2')
def product_page_2():
    return render_template("product_page_2.html")

@app.route('/product_page_3')
def product_page_3():
    return render_template("product_page_3.html")

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if not current_user.is_authenticated:
        flash('Для доступа к корзине необходимо войти в систему', 'error')
        return redirect(url_for('main_site'))
    if request.method == 'POST':
        product = request.form.get('product')
        price = request.form.get('price')

        if 'cart_items' not in session:
            session['cart_items'] = []

        cart_items = session['cart_items']

        existing_item = next((item for item in cart_items if item['product'] == product), None)
        if existing_item:
            existing_item['quantity'] += 1
        else:
            cart_items.append({'product': product, 'price': price, 'quantity': 1})

        session['cart_items'] = cart_items

        return redirect(url_for('main_site'))


@app.route('/cart')
def cart():
    if not current_user.is_authenticated:
        flash('Для доступа к корзине необходимо войти в систему', 'error')
        return redirect(url_for('main_site'))

    if 'cart_items' in session:
        cart_items = session['cart_items']
        total_cost = sum(float(item['price']) * item['quantity'] for item in cart_items)
    else:
        cart_items = []
        total_cost = 0
    return render_template('cart.html', cart_items=cart_items, total_cost=total_cost)


@app.route('/clear_cart', methods=['POST'])
@login_required
def clear_cart():
    session.pop('cart_items', None)
    return redirect(url_for('cart'))


@app.route('/update_cart/<product>', methods=['POST'])
@login_required
def update_cart(product):
    action = request.form['action']
    if 'cart_items' in session:
        cart_items = session['cart_items']
        for item in cart_items:
            if item['product'] == product:
                if action == '+':
                    item['quantity'] += 1
                elif action == '-':
                    item['quantity'] -= 1
                    if item['quantity'] == 0:
                        cart_items.remove(item)
                break
        session['cart_items'] = cart_items

    return redirect(url_for('cart'))


@app.route('/Register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_site'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Пароли не совпадают', 'error')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Пользователь с таким именем уже существует', 'error')
            return redirect(url_for('register'))

        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user_email:
            flash('Пользователь с таким email уже существует', 'error')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        remember_me = request.form.get('remember_me') == 'on'
        if remember_me:
            remember_token = secrets.token_hex(16)
            new_user.remember_token = remember_token
            db.session.commit()

            session['remember_token'] = remember_token

        return redirect(url_for('main_site'))

    return render_template('Register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)

            remember_me = request.form.get('remember_me') == 'on'
            if remember_me:
                remember_token = secrets.token_hex(16)
                user.remember_token = remember_token
                db.session.commit()

                session['remember_token'] = remember_token
            else:
                session.pop('remember_token', None)

            return redirect(url_for('profile'))
        else:
            flash('Неправильный логин или пароль', 'error')
    return render_template('login.html')


@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        flash('Для доступа к профилю необходимо войти в систему', 'error')
        return redirect(url_for('main_site'))
    return render_template('profile.html', username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()

    session.pop('remember_token', None)

    return redirect(url_for('main_site'))


if __name__ == '__main__':
    app.run(debug=True)
