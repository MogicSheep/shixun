# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Addres(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    createat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updateat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    deleteat = db.Column(db.DateTime)



class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    commodity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.String(500), nullable=False, server_default=db.FetchedValue())
    createat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updateat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    deleteat = db.Column(db.DateTime)



class Commodity(db.Model):
    __tablename__ = 'commodity'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    title = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.String(500), nullable=False, server_default=db.FetchedValue())
    tag = db.Column(db.String(500), nullable=False, server_default=db.FetchedValue())
    createat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updateat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    deleteat = db.Column(db.DateTime)



class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    commodity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    createat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updateat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    deleteat = db.Column(db.DateTime)



class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    courier = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    seller = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    buyer = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    commodity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    createat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updateat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    deleteat = db.Column(db.DateTime)



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50, 'utf8_general_ci'), nullable=False, server_default=db.FetchedValue())
    phone = db.Column(db.BigInteger, nullable=False)
    region = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    pwd = db.Column(db.String(50))
    createat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updateat = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    deleteat = db.Column(db.DateTime)
