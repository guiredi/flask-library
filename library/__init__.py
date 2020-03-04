from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api

#Model
from sqlalchemy.orm import relationship



app = Flask(__name__)
# api = Api(app)
app.secret_key = "super secret key"
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:546213gui@db-postgres.cihl3x37ztgu.us-east-2.rds.amazonaws.com:5432/RDS'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://USER:PASSWORD@db:5432/LIB'


db = SQLAlchemy(app)
ma = Marshmallow(app)

from library.api.views import views
app.register_blueprint(views)

db.create_all()


@app.route('/')
def home():
    return """
    <p>Author: <a href="http://0.0.0.0:8000/v1/author/">http://0.0.0.0:8000/v1/author/</a></p>
    <p>Book: <a href="http://0.0.0.0:8000/v1/book/">http://0.0.0.0:8000/v1/book/</a></p>
    """
