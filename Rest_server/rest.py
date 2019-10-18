import sys
sys.path.append("..")
from myDes import *
from bottle import unicode
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)


@app.route('/des/encrypt', methods=['POST'])
def flask_encrypt():
    if not request.json or not 'key' in request.json or 'message' not in request.json:
        abort(400)
    try:
        # return jsonify({'encrypted': encrypt(request.json["message"],request.json["key"])}), 201
        return encrypt(request.json["message"], request.json["key"])
    except Exception as e:
        make_response(jsonify({'error': e.args[0]}), 400)


@app.route('/des/decrypt', methods=['POST'])
def flask_decrypt():
    if not request.json or not 'key' in request.json or 'message' not in request.json:
        abort(400)
    try:
        # return jsonify({'encrypted': encrypt(request.json["message"],request.json["key"])}), 201
        return decrypt(request.json["message"], request.json["key"])
    except Exception as e:
        make_response(jsonify({'error': e.args[0]}), 400)
        # return "Sth went wrong"

if __name__ == '__main__':
    app.run(debug=True, port=9541)
