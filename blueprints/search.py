import os
import sys
sys.path.append("..")
from flask import Flask,jsonify,request,abort, redirect, render_template, url_for, flash, Blueprint
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import db, Address,User, setup_db, Commodity, Image
from flask_login import current_user, login_user, logout_user, login_required


search_bp = Blueprint('search', __name__)


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
