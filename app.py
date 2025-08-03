from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hệ thống bán giày đang hoạt động!"

if __name__ == '__main__':
    app.run(debug=True)