## 运行：

* flask run

## 基于数据库创建orm：

* flask-sqlacodegen 'mysql+pymysql://yxn:bilibili@118.195.233.143:3306/db_v1' --outfile "models_new.py"  --flask

## 数据库迁移：

* python manage.py db init

* python manage.py db migrate

* python manage.py db upgrade


## 部署

* cd shixun
* . venv/bin/activate
* gunicorn -w 4 -b 127.0.0.1:5500 app:app
echo "server {
    listen 8080; 
    server_name 118.195.233.143; 
 
    location / {
        proxy_pass http://127.0.0.1:5500; 
        access_log /root/flaskweb/access.log;
        error_log  /root/flaskweb/error.log;
                 add_header Access-Control-Allow-Methods 'GET,POST,DELETE';
        add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization'; 
    }

  }" > /etc/nginx/conf.d/default.conf

* 启动后 开启另一个服务器链接，输入：
* sudo service nginx start
