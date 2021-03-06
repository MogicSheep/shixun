# coding: utf-8
from sqlalchemy import Column, String, create_engine, Integer, ForeignKey
from sqlalchemy.sql.expression import nullslast
from werkzeug.exceptions import default_exceptions
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import func
import base64

database_name = "db_v3"
database_path = os.environ.get(
    "DATABASE_URL",
    "mysql://{}:{}@{}/{}".format(
        "yxn", "bilibili", "118.195.233.143:3306", database_name
    ),
)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.app = app
    db.init_app(app)
    db.create_all()


class Address(db.Model):
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    tags = db.Column(db.String(100))
    content = db.Column(
        db.String(200), nullable=False,
    )
    createat = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updateat = db.Column(db.TIMESTAMP)
    deleteat = db.Column(db.DateTime)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "city": self.city,
            "tags": self.tags,
            "content": self.content,
        }


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    commodity = db.Column(db.Integer, nullable=False,)
    content = db.Column(
        db.String(1000), nullable=False,
    )
    createat = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updateat = db.Column(db.TIMESTAMP)
    deleteat = db.Column(db.DateTime)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {"id": self.id, "user": self.user, "commodity": self.commodity, "content": self.content}


class Commodity(db.Model):
    __tablename__ = "commodity"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False,)
    title = db.Column(db.String(100), nullable=False,)
    content = db.Column(
        db.String(1000), nullable=False,
    )
    tag = db.Column(db.String(1000), nullable=False,)
    seller = db.Column(db.Integer, nullable=False)
    createat = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updateat = db.Column(db.TIMESTAMP)
    deleteat = db.Column(db.DateTime)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "tag": self.tag,
            "price": self.price,
            "seller": self.seller,
            "content": self.content,
        }


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.LargeBinary(length=(2 ** 32) - 1))
    commodity = db.Column(db.Integer, nullable=True,)
    createat = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updateat = db.Column(db.TIMESTAMP)
    deleteat = db.Column(db.DateTime)


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    courier = db.Column(db.String(50), nullable=True,)
    # status ???????????????0???????????????????????????,1???????????????????????????, 2??????????????????
    status = db.Column(db.Integer, nullable=False,)
    seller = db.Column(db.Integer, nullable=False,)
    buyer = db.Column(db.Integer, nullable=False,)
    destination = db.Column(
        db.Integer, nullable=False,
    )  # ????????????????????????id
    commodity = db.Column(db.Integer, nullable=False,)
    createat = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updateat = db.Column(db.TIMESTAMP)
    deleteat = db.Column(db.DateTime)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "seller": self.seller,
            "buyer": self.buyer,
            "commodity": self.commodity,
            "destination": self.destination,
            "createat": self.createat.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
            "courier": self.courier,
        }


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)  # ????????????id
    name = db.Column(
        db.String(50), nullable=True,
    )  # ????????????
    phone = db.Column(db.String(15), nullable=False)  # ????????????
    gravatar =db.Column(db.Integer, nullable=True) #?????????????????????id
    region = db.Column(
        db.String(50), nullable=True,
    )  # ??????????????????
    signature = db.Column(
        db.String(100), nullable=True,
    )  # ??????????????????
    pwd = db.Column(db.String(200))  # ????????????
    # pwd = db.Column(db.Integer)
    sex = db.Column(db.Integer)  # ????????????
    default_address = db.Column(db.Integer)  # ????????????id
    createat = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updateat = db.Column(db.TIMESTAMP)
    deleteat = db.Column(db.DateTime)

    def __repr__(self):
        return "<User %r>" % self.name

    def set_pwd(self, pwd):
        self.pwd = generate_password_hash(str(pwd))

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, str(pwd))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        ret = {
            "id": self.id,
            "name": self.name,
            "region": self.region,
            "default_address": self.default_address,
            "sex": self.sex,
            "signature": self.signature,
            "gravatar": self.gravatar
        }
        
        return ret


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # author = db.relationship('User', back_populates='messages') ???????????????
