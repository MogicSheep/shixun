import os
from flask import Flask,jsonify,request,abort
from models import setup_db, Commodity
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

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
