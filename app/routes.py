from flask import render_template, redirect, flash, url_for, request, abort
from flask_login import login_required, current_user, login_user, logout_user
import sqlalchemy as sa
from urllib.parse import urlsplit
from app import app, db
from app.models import User, Item, Cart
from app.forms import LoginForm, RegisterForm, AddItemForm


def admin_only(f):
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous or current_user.email != app.config['ADMIN_EMAIL']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))

        if user == None or not user.check_password(form.password.data):
            flash("Incorrect email or password.")
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '' or next_page=='logout':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/shop')
@login_required
def shop():
    items = db.session.scalars(sa.Select(Item)).all()
    return render_template('shop.html', items=items)


@app.route('/shop/add-item', methods=['GET', 'POST'], endpoint='add_item')
@admin_only
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        item = Item(
            item_name = form.item_name.data,
            item_description = form.item_description.data,
            price = form.price.data,
            img_url = form.img_url.data
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('shop'))
    return render_template("add_item.html", form=form)


@app.route('/shop/remove/<item_id>', endpoint='remove_item')
@admin_only
def remove_item(item_id):
    item = db.session.get(Item, item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('shop'))

@app.route('/shop/cart')
def cart():
    cart_items = db.session.scalars(current_user.items_in_cart.select()).all()
    return render_template('cart.html', cart_items=cart_items)


@app.route('/shop/cart/add/<item_id>')
def add_to_cart(item_id):
    cart_item = Cart(user_id=current_user.id, item_id=item_id)
    if db.session.scalar(sa.select(Cart).where(Cart.user_id == current_user.id, Cart.item_id == item_id)):
        print("Inside")
        flash("Item already in the cart.")
    else:
        db.session.add(cart_item)
        db.session.commit()
    return redirect(url_for('shop'))


@app.route('/shop/cart/remove.<cart_id>')
def remove_from_cart(cart_id):
    cart_item = db.session.get(Cart, cart_id)
    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/shop/buy')
def buy():
    return 'Buy'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))