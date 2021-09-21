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
import base64


#用户注册
@user_bp.route('/api/v1/user/register', methods = ['POST'])
def register():
    try:
        if current_user.is_authenticated:
            return jsonify({
                    'Success': False,
                    'Info': 'current_user is authenticated'
                })
        user_phone = str(request.form.get("phone"))
        user_pwd = str(request.form.get("pwd"))
        if user_pwd is None or user_phone is None:
            return jsonify({
                'Success': False,
                'Info': 'phone or pwd is None'
            })
        user = User.query.filter(User.phone == user_phone).first()
        if user is not None:
            return jsonify({
                'Success': False,
                'Info': 'current user is registed, please login directly.',
                'user': user.format()
            })
        new_user = User(phone = user_phone,name = " ", region = " ", signature = " ", gravatar = "1")
        new_user.set_pwd(user_pwd)
        new_user.insert()
        db.session.commit()
        login_user(new_user, remember = False)
        return jsonify({
            'Success': True,
            'user': new_user.format()
        })
    except Exception as e:
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })
        db.session.rollback()

#用户登录
@user_bp.route('/api/v1/user/login', methods = ['POST'])
def login():
    #try:
        if current_user.is_authenticated:
            return jsonify({
                    'Success': False,
                    'Info': 'current user is authenticated'
                })

        user_phone = str(request.form.get("phone"))
        user_pwd = str(request.form.get("pwd"))
        remember_me = request.form.get('remember', False)
        if remember_me is True:
            remember_me = True
        if user_pwd is None or user_phone is None:
            return jsonify({
                'Success': False,
                'Info': 'phone or pwd is None'
            })
        user = User.query.filter(User.phone == user_phone).first()
        if user is not None:
            if user.check_pwd(user_pwd):
                login_user(user, remember_me)
                return jsonify({
                    'Success': True,
                    'user': user.format()
                })
        return jsonify({
            'Success': False,
            'Info':'user is not registed',
            'user': user.format()
        })
    # except Exception as e:
    #     return jsonify({
    #         'Success': False,
    #         'Info': repr(e)
    #     })
   

#用户登出
@user_bp.route('/api/v1/user/logout', methods = ["DELETE"])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({
            'Success': True,
            #'user': user.format()
        })
    except Exception as e:
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })
    # return redirect(url_for('get_test')) #登出用户重定向到主页 /

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
@user_bp.route('/api/v1/user/change_profile', methods = ['POST'])
def change_profile(user_id):
    try:
        new_name = str(request.form.get("name", None))
        new_position = str(request.form.get("position", None))
        new_sex = int(request.form.get("sex", None))
        new_signature = str(request.form.get("signature", None))
        new_gravatar = int(request.form.get("gravatar", None))

        user_id = int(current_user.get_id())
        user = User.query.get(user_id)
        user.name = new_name
        user.region = new_position
        user.sex = new_sex
        user.signature = new_signature
        user.gravatar = new_gravatar
        user.insert()
        db.session.commit()
        return jsonify({
            'Success': True,
            'user': user.format()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })


#获取个人信息
@user_bp.route('/api/v1/user/get_profile/<user_id>',methods=['GET'])
def get_profile(user_id):
    try:
        if user_id is None:
            user_id = int(current_user.get_id())
        profile = User.query.get(user_id)
        ret = profile.format()
        if profile.gravatar is not None:
            photo = Image.query.filter(Image.id == profile.gravatar).first()
            ret["gravatar"] = str(base64.b64encode(photo.content))
        return jsonify({
            'Success':True,
            'Profile': ret
        })
    except Exception as e:
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })


#修改收货地址
@user_bp.route('/api/v1/user/change_address/<address_id>',methods=['POST'])
def change_address(address_id = 'null'):
    try:
        logger.debug("In to the address change %s" % str(address_id))
        if(address_id != 'null'):
            address = Address.query.get(address_id)
            if(request.form.get("user")):
                address.name = str(request.form.get("user"))
            if(request.form.get("name")):
                address.name = str(request.form.get("name"))
            if(request.form.get("phone")):
                address.phone = str(request.form.get("phone_number"))
            if(request.form.get("city")):
                address.city = str(request.form.get("city"))
            if(request.form.get("content")):
                address.content = str(request.form.get("detailed_address"))
        else:
            # new_id = Address.session.query(func.max(Address.id)).first()
            new_user = str(request.form.get("user",None))
            new_name = str(request.form.get("name",None))
            new_phone = str(request.form.get("phone_number",None))
            new_city = str(request.form.get("city",None))
            new_content = str(request.form.get("detailed_address",None))
            address = Address(user = new_user ,name=new_name, phone=new_phone,city = new_city,content=new_content)
        try:
            db.session.add(address)
            db.session.flush()
            db.session.commit()
            return jsonify({
                'Success':True,
                'Address': address.format()
            })
        except Exception as e:
            logger.exception('Add address failed!')
            db.session.rollback()
            raise e
    except Exception as ee:
        return jsonify({
            'Success': False,
            'Info': repr(ee)
        })


#删除收货地址
@user_bp.route('/api/v1/user/delete_address/<address_id>',methods=['DELETE'])
def delete_address(address_id):
    try:
        address = Address.query.get(address_id)
        address.delete()
        return jsonify({
            'success': True,
            'deleted': address.format()
        })
    except Exception as e:
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })


#获取所有收货地址
@user_bp.route('/api/v1/user/get_all_address',methods=['GET'])
def get_all_address(user_id):
    try:
        user_id = int(current_user.get_id())
        addresses = Address.query.filter(Address.user == user_id).all()
        formatted_address = [address.format() for address in addresses] 
        return jsonify({
            'Success':True,
            'marbres': formatted_address
        })
    except Exception as e:
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })


#设置默认收货地址
@user_bp.route('/api/v1/user/set_default_address',methods=['POST'])
def set_default_address(user_id):
    try:
        user_id = int(current_user.get_id())
        new_id = int(request.form.get("id",None))
        user = User.query.get(user_id)
        user.default_address = new_id
        user.insert()
        db.session.commit()
        return jsonify({
            'Success':True,
            'user': user.format()
        })
    except Exception as e:
        return jsonify({
            'Success': False,
            'Info': repr(e)
        })
