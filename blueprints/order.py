import os
import sys
from types import BuiltinMethodType
sys.path.append("..")
from flask import Flask,jsonify,request,abort, redirect, render_template, url_for, flash, Blueprint
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import db, Address,User, setup_db, Order, Image
from flask_login import current_user, login_user, logout_user, login_required


order_bp = Blueprint('order', __name__)


#查看所有订单
@order_bp.route('/api/v1/order/<user_id>', methods = ['GET'])
def check_all_order(user_id):
    orders = Order.query.filter(Order.buyer == user_id)
    formatted_orders = [orders.format() for order in orders]
    return jsonify({
        'Success':True,
        'orders': formatted_orders
    })

#购买（发起订单）
@order_bp.route('/api/v1/order/buy/', methods = ['POST'])
def order_buy():
    body = request.get_json()
    new_id = Order.query(func.max(Order.id)).first() + 1
    return


#查看单个订单情况
@order_bp.route('/api/v1/order/single_order/<order_id>', methods = ['GET'])
def check_single_order(order_id):
    single_order = Order.query.get(order_id)
    return jsonify({
        'Success':True,
        'single_order': single_order.format()
    })

#发货（卖家端）
@order_bp.route('/api/v1/order/deliver', methods = ['GET'])
def check_deliver():
    return 

#确认收货
@order_bp.route('/api/v1/order/take', methods = ['GET'])
def take_order():
    return 