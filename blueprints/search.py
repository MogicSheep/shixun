import os
import sys
sys.path.append("..")
from flask import Flask,jsonify,request,abort, redirect, render_template, url_for, flash, Blueprint
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import db, Address,User, setup_db, Commodity, Image
from flask_login import current_user, login_user, logout_user, login_required
from search_image import search_img
import logging

search_bp = Blueprint('search', __name__)
logger = logging.getLogger(__name__)

@search_bp.route('/api/v1/search/', methods = ['GET'])
def search():
    content = request.form.get("content",None)
    if content is None:
        content = " "
    items = Commodity.query.filter(Commodity.content.like("%"+content+"%"))
    formatted_items = [item.format() for item in items] 
    return jsonify({
        'Success':True,
        'items': formatted_items
    })

@search_bp.route('/api/v1/search/image/<image_url>', methods = ['GET'])
def image(image_url):
    try:
        img_file = Image.query.filter(Image.id == image_url).first()
        res = search_img(img_file.content, 1000)
        reslis = []
        tmp = set()
        for row in res:
            row = int(row[2:-1])
            tar = Image.query.filter(Image.id == row).first()
            if tar.commodity not in tmp:
                reslis.append(tar.commodity)
                tmp.add(tar.commodity)

        return jsonify({
            'Success': True,
            'items': reslis
        })
    except Exception as e:
        logger.exception('image search!')
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })
