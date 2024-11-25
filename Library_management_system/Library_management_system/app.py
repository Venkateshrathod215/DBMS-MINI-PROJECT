import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models import db, Book, User, Borrow, Staff

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Boloram%40%402233@localhost/library_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True, port=7001)
