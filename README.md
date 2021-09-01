运行：
flask run

基于数据库创建orm：
flask-sqlacodegen 'mysql+pymysql://yxn:bilibili@118.195.233.143:3306/db_v1' --outfile "models_new.py"  --flask

数据库迁移：
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
