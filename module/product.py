import pickle
from models import db, Address,User, setup_db, Commodity, Image

def product_add(request):
    body = request.get_json()
    new_content = body.get('content')
    new_price = int(body.get('price'))
    new_tags = pickle.dumps(list(body.get('tags')))
    # TODO : user id!
    new_seller = 123
    new_title = str(body.get('title'))
    new_commodity = Commodity(price = new_price, title = new_title, content = new_content,
            tag = new_tags, seller = new_seller)
    image_urls = list(body.get('images_urls'))
    success = True
    try:
        db.session.add(new_commodity)
        db.session.flush()
        for url in image_urls:
            row = Image.query.filter(Image.id==url).first()
            row.commodity = new_commodity.id
        db.session.commit()
    except Exception as e:
        print("--------------------------------------")
        print("[ERROR] at upload img: \n%s" % repr(e))
        print("--------------------------------------")
        success = False

    return success, new_commodity.id