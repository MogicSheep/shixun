import os
import sys
sys.path.append("..")
from flask import Flask,jsonify,request,abort, redirect, render_template, url_for, flash, Blueprint
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import db, Address,User, setup_db, Commodity, Image
from flask_login import current_user, login_user, logout_user, login_required
import logging


media_bp = Blueprint('media', __name__)
logger = logging.getLogger(__name__)

# 上传图片
@media_bp.route('/api/v1/media/upload_image', methods = ['POST'])
def upload_image():
    imgfile = request.files['image'].read()
    new_img = Image(content = imgfile)
    success = True
    try:
        db.session.add(new_img)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.exception('Uploading image failed!')
        success = False
        db.session.rollback()
    
    return jsonify({
        'success' : success,
        'id': new_img.id
    })
    

# 购买物品
# @media_bp.route('/api/v1/order/buy', methods = ['POST'])
# def bug():
#     body = request.get_json()
#     com_id = body.get['id']
#     # TODO: user id!
#     user_id = 123