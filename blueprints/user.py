import os
import sys
sys.path.append("..")
from flask import Flask,jsonify,request,abort, redirect, render_template, url_for, flash, Blueprint
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import db, Address,User, setup_db, Commodity, Image
from flask_login import current_user, login_user, logout_user, login_required
import logging
from sqlalchemy import func

user_bp = Blueprint('user', __name__)
logger = logging.getLogger(__name__)

#用户注册
@user_bp.route('/api/v1/user/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('get_test')) #已登录用户重定向到主页 /
    else:
        if request.method == 'POST':
            user_phone = request.form.get("phone")
            user_pwd = request.form.get("pwd")

            user = User.query.filter(User.phone == user_phone).first()
            if user is not None:
                flash('The phone number is currently registered')
                return redirect(url_for('login')) #已注册用户重定向到登录页面 /api/v1/user/login
            else:
                new_user = User(phone = user_phone)
                new_user.set_pwd(user_pwd)
                new_user.insert()
                login_user(user)
                return redirect(url_for('login')) #已注册用户重定向到登录页面 /api/v1/user/login
    return render_template('register.html') #填register页面

#用户登录
@user_bp.route('/api/v1/user/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('get_test')) #已登录用户重定向到主页 /
    else:
        if request.method == 'POST':
            user_phone = request.form.get("phone")
            user_pwd = request.form.get("pwd")

            user = User.query.filter(User.phone == user_phone).first()
            if user is not None:
                if user.pwd is None:
                    flash('Register your account')
                    return redirect(url_for('register')) #未注册用户重定向到注册页面 /api/v1/user/register
                else:
                    if user.check(user_pwd):
                        login_user(user)
                        return redirect(url_for('get_test')) #登录用户重定向到主页 /
            flash('Username or password is incorrect')
            return redirect(url_for('login')) #密码或账户错误用户重定向到登录页面 /api/v1/user/login
    return render_template('login.html') #填login页面

#用户登出
@user_bp.route('/api/v1/user/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_test')) #登出用户重定向到主页 /

# @user_bp.route('/api/v1/user/login/<user_phone>/<user_code>', methods = ['POST'])
# def get_phone(user_phone, user_code):
#     message = User.query.get(user_phone)
#     return jsonify({
#         'Success' : True,
#         'Message' : message.format()
#     })

#请求发送验证码
# @user_bp.route('/api/v1/user/code/<user_phone>', methods = ['GET'])
# def get_code(user_phone):
#     message = User.query.get(user_phone)
#     return jsonify({
#         'Success' : True,
#         'Message' : message.format()
#     })

#修改个人信息
@user_bp.route('/api/v1/user/change_profile/<user_id>', methods = ['POST'])
def change_profile(user_id):
    body = request.get_json()

    new_name = body.get("name", None)
    new_position = body.get("position", None)
    new_sex = body.get("sex", None)
    new_signature = body.get("signature", None)

    user = User.query.get(user_id)
    try:
        user.name = new_name
        user.region = new_position
        user.sex = new_sex
        user.signature = new_signature
        user.insert()
    except:
        print(" ")
    return jsonify({
        'Success': True,
        'user': user.format()
    })


#获取个人信息
@user_bp.route('/api/v1/user/get_profile/<user_id>',methods=['GET'])
def get_profile(user_id):
    profile = User.query.get(user_id)
    return jsonify({
        'Success':True,
        'Profile': profile.format()
    })
#修改收货地址
@user_bp.route('/api/v1/user/change_address/<address_id>',methods=['POST'])
def change_address(address_id = 'null'):
    logger.debug("In to the address change %s" % str(address_id))
    if(address_id != 'null'):
        address = Address.query.get(address_id)
        if(request.form.get("user")):
            address.name = request.form.get("user")
        if(request.form.get("name")):
            address.name = request.form.get("name")
        if(request.form.get("phone")):
            address.phone = request.form.get("phone_number")
        if(request.form.get("city")):
            address.city = request.form.get("city")
        if(request.form.get("content")):
            address.content = request.form.get("detailed_address")
    else:
        # new_id = Address.session.query(func.max(Address.id)).first()
        new_user = request.form.get("user",None)
        new_name = request.form.get("name",None)
        new_phone = request.form.get("phone_number",None)
        new_city = request.form.get("city",None)
        new_content = request.form.get("detailed_address",None)
        address = Address(user = new_user ,name=new_name, phone=new_phone,city = new_city,content=new_content)
    try:
        db.session.add(address)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.exception('Add address failed!')
        success = False
        db.session.rollback()
    return jsonify({
        'Success':True,
        'Address': address.format()
    })


#删除收货地址
@user_bp.route('/api/v1/user/delete_address/<address_id>',methods=['DELETE'])
def delete_address(address_id):
    address = Address.query.get(address_id)
    address.delete()
    return jsonify({
        'success': True,
        'deleted': address.format()
    })


#获取所有收货地址
@user_bp.route('/api/v1/user/get_all_address/<user_id>',methods=['GET'])
def get_all_address(user_id):
    addresses = Address.query.filter(Address.user == user_id).all()
    formatted_address = [address.format() for address in addresses] 
    return jsonify({
        'Success':True,
        'marbres': formatted_address
    })


#设置默认收货地址
@user_bp.route('/api/v1/user/set_default_address/<user_id>',methods=['POST'])
def set_default_address(user_id):
    new_id = request.form.get("id",None)
    user = User.query.get(user_id)
    try:
        user.default_address = new_id
        user.insert()
    except:
        print("something go wrong")
    return jsonify({
        'Success':True,
        'user': user.format()
    })
