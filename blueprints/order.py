import os
import sys
from types import BuiltinMethodType
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import update
from sqlalchemy import func
from sqlalchemy.sql.functions import user
sys.path.append("..")
from flask import Flask,jsonify,request,abort, redirect, render_template, url_for, flash, Blueprint
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import Commodity, db, Address,User, setup_db, Order, Image
from flask_login import current_user, login_user, logout_user, login_required
import logging

logger = logging.getLogger(__name__)

order_bp = Blueprint('order', __name__)


#查看所有订单
@order_bp.route('/api/v1/order/<user_id>', methods = ['GET'])
def check_all_order(user_id):
    try:
        orders = Order.query.filter(Order.buyer == user_id)
        formatted_orders = [order.format() for order in orders]
        return jsonify({
            'Success':True,
            'orders': formatted_orders
        })
    except Exception as e:
        return jsonify({
            'Success':False,
            'info': repr(e)
        })

#查看作为卖家的订单
@order_bp.route('/api/v1/order/sale/<user_id>', methods = ['GET'])
def check_all_sale_order(user_id):
    try:
        orders = Order.query.filter(Order.seller == user_id)
        formatted_orders = [order.format() for order in orders]
        return jsonify({
            'Success': True,
            'orders': formatted_orders
        })
    except Exception as e:
        return jsonify({
            'Success':False,
            'info': repr(e)
        })

#购买（发起订单）
@order_bp.route('/api/v1/order/buy/<user_id>', methods = ['POST'])
def order_buy(user_id):
    try:
        product_id = request.form.get("commodity",None)
        address_id = request.form.get("address_id",None)
        max_order_id = db.session.query(func.max(Order.id)).first()[0]
        new_id = (0 if max_order_id == None else max_order_id)  + 1
        print(new_id)
        create_time = func.now()
        update_time = func.now()
        seller_id = Commodity.query.filter(Commodity.id == product_id).first().seller
        order = Order(id = new_id,buyer = user_id,destination = address_id, seller=seller_id,\
            commodity = product_id,createat = create_time,updateat = update_time,\
                status = 0)
        order.insert()
        return jsonify({
            'Success':True,
            'Order': order.format
        })
    except Exception as e:
        logger.exception("Order buy error!")
        return jsonify({
            'Success':False,
            'info': repr(e)
        })


#查看单个订单情况
@order_bp.route('/api/v1/order/single_order/<order_id>', methods = ['GET'])
def check_single_order(order_id):
    # TODO：不能查看别人的订单
    try:
        single_order = Order.query.get(order_id)
        return jsonify({
            'Success':True,
            'single_order': single_order.format()
        })
    except:
        return jsonify({
            'Success':False
        })

#发货（卖家端）
@order_bp.route('/api/v1/order/deliver/<order_id>', methods = ['GET'])
def check_deliver(order_id):
    try:
        single_order = Order.query.get(order_id)
        single_order.status = 1
        single_order.insert()
        single_order.update()
    except:
        return jsonify({
                'Success':False
            })

#确认收货
@order_bp.route('/api/v1/order/take/<order_id>', methods = ['GET'])
def take_order(order_id):
    try:
        single_order = Order.query.get(order_id)
        single_order.status = 2
        single_order.insert()
        single_order.update()
    except:
        return jsonify({
                'Success':False
            })