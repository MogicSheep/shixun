import os
import sys
sys.path.append("..")
from flask import Flask,jsonify,request,abort, redirect, render_template, url_for, flash, Blueprint
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import db, Address,User, setup_db, Commodity, Image
from flask_login import current_user, login_user, logout_user, login_required


media_bp = Blueprint('media', __name__)

# 上传图片
@media_bp.route('/api/v1/media/upload_image', methods = ['POST'])
def upload_image():
    success, retid = media_upload_image(request)
    return jsonify({
        'success' : success,
        'id': retid
    })
    

# 购买物品
# @media_bp.route('/api/v1/order/buy', methods = ['POST'])
# def bug():
#     body = request.get_json()
#     com_id = body.get['id']
#     # TODO: user id!
#     user_id = 123