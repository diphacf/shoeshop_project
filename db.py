from flask_mysqldb import MySQL

mysql = MySQL()

def init_app(app):
    app.config.from_object('config.Config')
    mysql.init_app(app)