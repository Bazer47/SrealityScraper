import os

from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import select

from database import db
from fill_database import fill_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

from views import *

with app.app_context():
    db.create_all()
    fill_db()

if __name__ == "__main__":
    app.run(debug=False)
