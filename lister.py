import json
from flask import Flask,jsonify

with open("result.json",encoding='utf8') as fp:
    data=json.load(fp)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify(data)

if __name__ == '__main__':
    app.run()