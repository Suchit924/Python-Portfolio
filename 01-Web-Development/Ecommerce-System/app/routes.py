from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app import db
from app.models import User, Product, CartItem
from app.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
import stripe
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)
stripe.api_key = Config.STRIPE_SECRET_KEY

@main.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main.route('/product/<int:id>')
def product(id):
    item = Product.query.get_or_404(id)
    return render_template('product.html', product=item)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Account created. Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Login failed.')
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found.')
        return redirect(url_for('main.index'))

    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('main.cart'))

@main.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    # Filter out items with invalid products
    items = [item for item in items if item.product is not None]
    total = sum(item.product.price * item.quantity for item in items)
    return render_template('cart.html', items=items, total=total)

@main.route('/checkout', methods=['POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    items = [item for item in items if item.product is not None]  # Filter out invalid

    total = sum(item.product.price * item.quantity for item in items)

    line_items = [{
        'price_data': {
            'currency': 'usd',
            'product_data': {'name': item.product.name},
            'unit_amount': item.product.price
        },
        'quantity': item.quantity
    } for item in items]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=url_for('main.success', _external=True),
        cancel_url=url_for('main.cart', _external=True)
    )

    return redirect(session.url)

@main.route('/success')
@login_required
def success():
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return render_template('checkout.html', message="Payment successful!")

