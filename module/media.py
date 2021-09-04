from models import db, Address,User, setup_db, Commodity, Image

def media_upload_image(request):
    imgfile = request.files['image'].read()
    new_img = Image(content = imgfile)
    success = True
    try:
        db.session.add(new_img)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        print("--------------------------------------")
        print("[ERROR] at upload img: \n%s" % repr(e))
        print("--------------------------------------")
        success = False
    return success, new_img.id

