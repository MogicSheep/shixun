import os
import sys
sys.path.append("..")
from flask import Flask,jsonify,request,abort, redirect, render_template, url_for, flash, Blueprint
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import db, Address,User, setup_db, Commodity, Image
from flask_login import current_user, login_user, logout_user, login_required



product_bp = Blueprint('product', __name__)

#查看单个商品信息
@product_bp.route('/api/v1/product/show/<commodity_id>',methods=['GET'])
def show_commodity_info(commodity_id):
    info = Commodity.query.get(commodity_id)
    return jsonify({
        'Success':True,
        'Info': info.format()
    })

#查看单个商品所有评论
@product_bp.route('/api/v1/product/comments/<commodity_id>',methods=['GET'])
def show_commodity_comments(commodity_id):
    comments = Comment.query.filter(Comment.commodity == commodity_id).all()
    formatted_comments = [comment.format() for comment in comments] 
    return jsonify({
        'Success':True,
        'comments': formatted_comments
    })
#评论商品信息
@product_bp.route('/api/v1/product/add_comment',methods=['POST'])
def add_comment():
    body = request.get_json()
    product_id = body.get("commodity",None)
    content = body.get("content",None)
    new_id = Comment.query(func.max(Comment.id)).first() + 1
    comment = Comment(id = new_id, commodity = product_id, content = content)
    try:
        comment.insert()
    except:
        print(" ")
    return jsonify({
        'Success':True,
        'Comment': comment.format
    })

# 发布信息
@product_bp.route('/api/v1/product/add', methods=['POST'])
def add_product():
    success, retid = product_add(request)
    return jsonify({
        'success' : success,
        'id': retid
    })