import os
import sys
sys.path.append("..")
from flask import Flask,jsonify,request,abort, redirect, render_template, url_for, flash, Blueprint
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import db, Address,User, setup_db, Commodity, Image
from flask_login import current_user, login_user, logout_user, login_required
from re_algorithm import get_re_list

recommend_bp = Blueprint('recommend', __name__)

@recommend_bp.route("/api/v1/recommend/", methods=["GET"])
def recommend():
    try:
        Recommendations = get_re_list()
        recommend_id = []
        for item in Recommendations:
            recommend_id.append(item[0])
        return jsonify({
            "Success": True, 
            "commodity": recommend_id
            })
    except Exception as e:
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })
        