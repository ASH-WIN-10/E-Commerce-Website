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

    # items: so.WriteOnlyMapped['Items'] = so.relationship(back_populates='owner')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)
    
# class Items(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     item_name: so.Mapped[str] = so.mapped_column(sa.String(64))
#     price: so.Mapped[int] = so.mapped_column(sa.Integer)
#     owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True, nullable=True)

#     owner: so.Mapped[User] = so.relationship(back_populates='items')

#     def __repr__(self) -> str:
#         return '<Items {}>'.format(self.item_name)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))