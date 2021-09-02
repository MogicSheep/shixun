import os
from flask import Flask,jsonify,request,abort
from werkzeug.wrappers import PlainRequest
from flask_cors import CORS
from models import Address,User, setup_db, Commodity, Comment

import pymysql
pymysql.install_as_MySQLdb()


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

    #登录与注册
    @app.route('/api/v1/user/login/<user_phone>/<user_code>', methods = ['POST'])
    def get_phone(user_phone, user_code):
        message = User.query.get(user_phone)
        return jsonify({
            'Success' : True,
            'Message' : message.format()
        })

    #请求发送验证码
    @app.route('/api/v1/user/code/<user_phone>', methods = ['GET'])
    def get_code(user_phone):
        message = User.query.get(user_phone)
        return jsonify({
            'Success' : True,
            'Message' : message.format()
        })

    #修改个人信息
    @app.route('/api/v1/user/set_default_address/<user_id>', methods=['POST'])
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
    @app.route('/api/v1/user/get_profile/<user_id>',methods=['GET'])
    def get_profile(user_id):
        profile = User.query.get(user_id)
        return jsonify({
            'Success':True,
            'Profile': profile.format()
        })
    #修改收货地址
    @app.route('/api/v1/user/change_address/<address_id>',methods=['POST'])
    def change_address(address_id = 'null'):
        body = request.get_json()
        if(address_id != 'null'):
            address = Address.query.get(address_id)
            if(body.get("user")):
                address.name = body.get("user")
            if(body.get("name")):
                address.name = body.get("name")
            if(body.get("phone")):
                address.phone = body.get("phone")
            if(body.get("city")):
                address.city = body.get("city")
            if(body.get("content")):
                address.content = body.get("content")
        else:
            new_id = Address.query(func.max(Address.id)).first() + 1
            new_user = body.get("user",None)
            new_name = body.get("name",None)
            new_phone = body.get("phone",None)
            new_city = body.get("city",None)
            new_content = body.get("content",None)
            address = Address(id = new_id,user = new_user ,name=new_name, phone=new_phone,city = new_city,content=new_content)
        try:
            address.insert()
        except:
            print(" ")
        return jsonify({
            'Success':True,
            'Address': address.format()
        })
    #删除收货地址
    @app.route('/api/v1/user/delete_address/<address_id>',methods=['DELETE'])
    def delete_address(address_id):
        address = Address.query.get(address_id)
        address.delete()
        return jsonify({
            'success': True,
            'deleted': address.format()
        })


    #获取所有收货地址
    @app.route('/api/v1/user/set_default_address/<user_id>',methods=['GET'])
    def post_all_address(user_id):
        addresses = Address.query.filter(Address.user == user_id).all()
        formatted_address = [address.format() for address in addresses] 
        return jsonify({
            'Success':True,
            'marbres': formatted_address
        })
    #设置默认收货地址
    @app.route('/api/v1/user/set_default_address/<user_id>',methods=['POST'])
    def set_default_address(user_id):
        body = request.get_json()
        new_id = body.get("address_id",None)
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
    #查看单个商品信息
    @app.route('/api/v1/product/show/<commodity_id>',methods=['GET'])
    def show_commodity_info(commodity_id):
        info = Commodity.query.get(commodity_id)
        return jsonify({
            'Success':True,
            'Info': info.format()
        })
    
    #查看单个商品评论
    @app.route('/api/v1/product/comments/<commodity_id>',methods=['GET'])
    def show_commodity_comments(commodity_id):
        comments = Comment.query.filter(Comment.commodity == commodity_id).all()
        formatted_comments = [comment.format() for comment in comments] 
        return jsonify({
            'Success':True,
            'comments': formatted_comments
        })
    #评论商品信息
    @app.route('/api/v1/product/add_comment',methods=['POST'])
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

    @app.route('/marbres',methods=['POST'])
    def post_marbre():
        body = request.get_json()
        new_title = body.get("title",None)
        new_image = body.get("image",None)
        new_price = body.get("price",None)
        new_seller = body.get("seller",None)
        new_content = body.get("content",None)

        try:
            marbre = Commodity(title = new_title, price=new_price, seller=new_origin, content=new_content)
            marbre.insert()
        except:
            print(" ")
        return jsonify({
            'Success':True,
            'Marbre': marbre.format()
        })

    @app.route('/marbres',methods=['GET'])
    def get_marbre():
        marbres = Commodity.query.all()
        formatted_marbres = [marbre.format() for marbre in marbres] 
        return jsonify({
            'Success':True,
            'marbres': formatted_marbres
        })

    @app.route('/marbres/<marbre_id>',methods=['PATCH'])
    def patch_marbre(marbre_id):
        body = request.get_json()
        marbre = Commodity.query.get(marbre_id)
        if(body.get("title")):
            marbre.title = body.get("title")
        # if(body.get("image")):
        #     marbre.image = body.get("image")
        if(body.get("price")):
            marbre.price = body.get("price")
        if(body.get("seller")):
            marbre.origin = body.get("seller")
        if(body.get("content")):
            marbre.description = body.get("content")
        try:
            marbre.insert()
        except:
            print(" ")
        return jsonify({
            'Success':True,
            'Marbre': marbre.format()
        })
    
    @app.route('/marbres/<marbre_id>',methods=['DELETE'])
    def delete_marbre(marbre_id):
        marbre = Commodity.query.get(marbre_id)
        marbre.delete()
        return jsonify({
            'success': True,
            'deleted': marbre.format()
        })

    # # 发布信息
    # @app.route('/api/v1/product/add/<user_id>', methods=['POST'])
    # def add_product(user_id):
    #     body = request.get_json()

    #     return 
    return app


app = create_app()

from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    #nonlocal app
    app.run()
