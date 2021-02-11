import logging
import os
from argparse import ArgumentParser

from dotenv import load_dotenv
from flask import request, jsonify, Flask, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

load_dotenv()

app = Flask("sqlalchemy-example")
app.logger.setLevel(logging.INFO)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)


db.metadata.create_all(db.engine)


@app.route("/")
def index():
    return jsonify({"status": "ok"})


@app.route("/adduser", methods=["POST"])
def add_user():
    request_data = request.json
    users = []
    for row in request_data:
        users.append(User(name=row['name'], email=row['email']))

    try:
        db.session.add_all(users)
        db.session.commit()
        return jsonify({"message": f"{len(users)} users added."})
    except (DBAPIError, SQLAlchemyError):
        db.session.rollback()
        abort(500)


@app.route("/users", methods=["GET"])
def get_users():
    user_list = db.session.query(User).all()
    return jsonify(user_list)


if __name__ == '__main__':
    parser = ArgumentParser(description="Simple Flask-Sqlalchemy example.")
    parser.add_argument("-h", "--host", required=False, default="localhost", help="Webserver Host")
    parser.add_argument("-h", "--port", required=False, default=8080, help="Webserver Port")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
