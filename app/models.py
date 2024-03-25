import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
from flask_login import UserMixin
from app import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    items_bought: so.WriteOnlyMapped['Item'] = so.relationship(back_populates='owner')
    items_in_cart: so.WriteOnlyMapped['Cart'] = so.relationship(back_populates='user_cart')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)
    

class Item(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    item_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    item_description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(512))
    price: so.Mapped[int] = so.mapped_column(sa.Integer)
    img_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String)
    quantity: so.Mapped[int] = so.mapped_column(sa.Integer, default=1)

    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True, unique=False, nullable=True)

    owner: so.Mapped[User] = so.relationship(back_populates='items_bought')
    cart_items: so.WriteOnlyMapped['Cart'] = so.relationship(back_populates='item', passive_deletes=True)

    def __repr__(self) -> str:
        return '<Item {}>'.format(self.item_name)
    

class Cart(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    quantity: so.Mapped[int] = so.mapped_column(sa.Integer, default=1)

    item_id: so.Mapped[Item] = so.mapped_column(sa.ForeignKey(Item.id), index=True, unique=False)
    user_id: so.Mapped[User] = so.mapped_column(sa.ForeignKey(User.id), index=True, unique=False)
    
    user_cart: so.Mapped[User] = so.relationship(back_populates='items_in_cart')
    item: so.Mapped[Item] = so.relationship(back_populates='cart_items')

    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))