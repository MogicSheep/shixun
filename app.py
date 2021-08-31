import os
from flask import Flask,jsonify,request,abort
from werkzeug.wrappers import PlainRequest
from models import Address,User, setup_db, Commodity
from flask_cors import CORS

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
        addresses = Address.query.filter(user = user_id).all()
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

    # @app.route('/product/add', methods=['POST'])
    # def add_product
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
