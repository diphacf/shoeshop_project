from flask import Flask
from db import mysql, init_app

app = Flask(__name__)
init_app(app)

@app.route('/')
def home():
    return "Hệ thống bán giày đang hoạt động!"

if __name__ == '__main__':
    app.run(debug=True)