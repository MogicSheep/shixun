from sqlalchemy import Column, String, create_engine,Integer,ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
database_name="shixun"
database_path = os.environ.get('DATABASE_URL',"mysql://{}:{}@{}/{}".format('yxn', 'bilibili','118.195.233.143:3306', database_name))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.app = app
    db.init_app(app)
    db.create_all()


class Marbre(db.Model):
    __tablename__ = "Marbre"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80))
    image = db.Column(db.String(200))
    price = db.Column(db.Integer())
    origin = db.Column(db.String(80))
    tag = db.Column(db.String(80))
    description = db.Column(db.String(500),nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'), default=-1) # 所属订单 
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
        'id': self.id,
        'title': self.title,
        'image': self.image,
        'tag': self.tag,
        'price': self.price,
        'origin': self.origin,
        'description':self.description,
        }



class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    item_sell = db.relationship('Marbre', backref='user')  # 出售商品外键关系关联
    orders = db.relationship('Order', backref='user')  # 订单外键关系关联
    
    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)

class Order(db.Model):
    __tablename__ = "Order"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    sell_id  = db.Column(db.Integer, db.ForeignKey('user.id'))  # 卖家编号
    buy_id  = db.Column(db.Integer, db.ForeignKey('user.id'))  # 买家编号
    info = db.Column(db.String(80)) # 订单信息
    time = db.Column(db.DateTime, index=True, default=datetime.now)  # 交易时间
    item_sell = db.relationship('Marbre', backref='Order')  # 出售商品外键关系关联

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
        'id': self.id,
        'sell_id': self.sell_id,
        'buy_id': self.buy_id,
        'info': self.info,
        'time': self.time
        }