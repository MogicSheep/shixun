import os
import sys
import pickle

from sqlalchemy.sql.elements import Null
sys.path.append("..")
from flask import Flask,jsonify,request,abort, redirect, render_template, url_for, flash, Blueprint
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import db, Address,User, setup_db, Commodity, Image, Comment
from flask_login import current_user, login_user, logout_user, login_required
import logging
import base64

product_bp = Blueprint('product', __name__)
logger = logging.getLogger(__name__)

#查看单个商品信息
@product_bp.route('/api/v1/product/show/<commodity_id>',methods=['GET'])
def show_commodity_info(commodity_id):
    try:
        info = Commodity.query.get(commodity_id)
        ret_dic = {
            'Success':True,
            'Info': info.format()
        }
        photos = Image.query.filter(Image.commodity==commodity_id).all()
        photo_file = [photo.content for photo in photos]
        logger.info(type(photo_file[0]))
        for _, file in enumerate(photo_file):
            logger.info(str(base64.b64encode(file)))
            ret_dic[str(_)] = str(base64.b64encode(file))
        ret_dic["num_of_pic"] = len(photo_file)
        return jsonify(ret_dic)
    except Exception as e:
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })

#查看单个商品所有评论
@product_bp.route('/api/v1/product/comments/<commodity_id>',methods=['GET'])
def show_commodity_comments(commodity_id):
    try:
        comments = Comment.query.filter(Comment.commodity == commodity_id).all()
        formatted_comments = [comment.format() for comment in comments] 
        return jsonify({
            'Success':True,
            'comments': formatted_comments
        })
    except Exception as e:
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })

#查看用户发布的所有商品id
@product_bp.route('/api/v1/product/show_all/',defaults={'user_id':None},methods=['GET'])
@product_bp.route('/api/v1/product/show_all/<user_id>',methods=['GET'])
def show_all(user_id):
    try:
        if user_id is None:
            user_id = int(current_user.get_id())
        pros = Commodity.query.filter(Commodity.seller == user_id)
        ret = [int(pro.id) for pro in pros]
        return jsonify({
            'Success': True,
            'ids': ret
        })
    except Exception as e:
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })
    
#评论商品信息
@product_bp.route('/api/v1/product/add_comment',methods=['POST'])
def add_comment():
    try:
        product_id = request.form.get("commodity",None)
        content = request.form.get("content",None)
        comment = Comment(commodity = product_id, content = content)
        try:
            comment.insert()
        except:
            logger.exception('Add commedity failed!')
            success = False
            db.session.rollback()    
        return jsonify({
            'Success':True,
            'Comment': comment.id
        })
    except Exception as e:
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })

# 发布信息
@product_bp.route('/api/v1/product/add', methods=['POST'])
def add_product():
    if not current_user.is_authenticated:
        return jsonify({
            'success' : False,
            'id': -1,
            'Info': "Not login!"
        })
    try:
        new_content = request.form.get('content')
        new_price = float(request.form.get('price'))
        # new_tags = pickle.dumps(list(request.form.get('tags')))
        new_tags = request.form.get('tags')
        new_seller = int(current_user.get_id())
        new_title = str(request.form.get('title'))
        new_commodity = Commodity(price = new_price, title = new_title, content = new_content,
                tag = new_tags, seller = new_seller)
        image_urls = request.form.get('images_urls').split(',')
        success = True
        db.session.add(new_commodity)
        db.session.flush()
        for url in image_urls:
            row = Image.query.filter(Image.id==int(url)).first()
            logger.debug("url: %d" % int(url))
            logger.debug(str(row))
            row.commodity = new_commodity.id
        db.session.commit()
    except Exception as e:
        logger.exception('Add commedity failed!')
        success = False
        db.session.rollback()

    return jsonify({
        'success' : success,
        'id': new_commodity.id
    })

