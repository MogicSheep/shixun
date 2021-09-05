import os
from flask import Flask,jsonify,request,abort, redirect, render_template, url_for, flash
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import db, Address,User, setup_db, Commodity, Image
from flask_login import current_user, login_user, logout_user, login_required


from blueprints.user import user_bp
from blueprints.product import product_bp
from blueprints.order import order_bp
from blueprints.search import search_bp
from blueprints.media import media_bp
from blueprints.recommend import recommend_bp 

import pymysql
pymysql.install_as_MySQLdb()

import pickle

from module.product import product_add
from module.media import media_upload_image
def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_test():
        return jsonify({
            'success':True,
            'marbre': 'welcome'
        })
    
    register_blueprints(app)

    return app

def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(recommend_bp)



app = create_app()
app.debug = True
app.config['DEBUG'] = True
from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    app.run(debug=True)
