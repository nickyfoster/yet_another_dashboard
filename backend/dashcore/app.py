import flask
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/users', methods=["GET", "POST"])
def users():
    if request.method == "GET":
        data = {"status": "OK"}
        return flask.jsonify(data)
    if request.method == "POST":
        received_data = request.get_json()
        return flask.Response(response="", status=201)


if __name__ == "__main__":
    app.run("localhost", port=6969)
