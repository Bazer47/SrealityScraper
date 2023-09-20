from itertools import groupby
from operator import attrgetter

from flask import render_template
from sqlalchemy import select

from app import app
from database import db
from models import Property, Image

@app.route("/")
def index():
    properties = db.session.execute(select(Property).order_by(Property.id)).all()
    properties = [prop[0] for prop in properties]
    images = db.session.execute(select(Image).order_by(Image.id)).all()
    images = [img[0] for img in images]
    images_groupby = {k: list(g) for k, g in groupby(images, attrgetter('property_id'))}
    # print(images_groupby)
    return render_template("index.html", properties=properties, images=images_groupby)