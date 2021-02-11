import logging
import os
from argparse import ArgumentParser

from dotenv import load_dotenv
from flask import request, jsonify, Flask, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

load_dotenv()


app = Flask("sqlalchemy-example")
app.logger.setLevel(logging.INFO)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
db = SQLAlchemy(app)


class Group(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    group_id = db.Column(db.INTEGER, ForeignKey('group.id'), nullable=False)
    email = db.Column(db.String(20), nullable=False)


db.metadata.create_all(db.engine)


@app.route("/")
def index():
    return jsonify({"status": "ok"})


@app.route("/addgroup", methods=["POST"])
def add_group():
    request_data = request.json
    group = Group(name=request_data["name"])
    try:
        db.session.add(group)
        db.session.commit()
        return jsonify({"group_id": group.id})
    except (DBAPIError, SQLAlchemyError):
        db.session.rollback()
        abort(500)


@app.route("/adduser", methods=["POST"])
def add_user():
    request_data = request.json
    user = User(
        name=request_data['name'],
        email=request_data['email'],
        group_id=request_data['group_id']
    )

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"user_id": user.id})
    except (DBAPIError, SQLAlchemyError):
        db.session.rollback()
        abort(500)


@app.route("/users", methods=["GET"])
def get_users():
    user_list = db.session.query(User).all()
    return jsonify(user_list)


@app.route("/groups", methods=["GET"])
def get_group():
    group_list = db.session.query(Group).all()
    return jsonify(group_list)


if __name__ == '__main__':
    parser = ArgumentParser(description="Simple Flask-Sqlalchemy example.")
    parser.add_argument("-h", "--host", required=False, default="localhost", help="Webserver Host")
    parser.add_argument("-h", "--port", required=False, default=8080, help="Webserver Port")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
