import os

from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import select

from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

from models import Property, Image
from views import *

with app.app_context():
    db.create_all()

    if len(db.session.execute(select(Property).order_by(Property.id)).all()) < 12:
        prop_tmp = Property(title="Byt", title_url="Byt_url", description="Byt_descr")
        db.session.add(prop_tmp)
        db.session.flush()
        prop_id_tmp = prop_tmp.id
        print(f"{prop_id_tmp = }")
        db.session.add(Image(property_id=prop_id_tmp, url="https://d18-a.sdn.cz/d_18/c_img_QJ_Jo/6e0BFt5.jpeg?fl=res,400,300,3|shr,,20|jpg,90"))
        db.session.add(Image(property_id=prop_id_tmp, url="https://d18-a.sdn.cz/d_18/c_img_QJ_Jo/6e0BFt5.jpeg?fl=res,400,300,3|shr,,20|jpg,90"))
        db.session.add(Image(property_id=prop_id_tmp, url="https://d18-a.sdn.cz/d_18/c_img_QJ_Jo/6e0BFt5.jpeg?fl=res,400,300,3|shr,,20|jpg,90"))
        db.session.commit()
    props = db.session.execute(select(Property).order_by(Property.id))
    imgs = db.session.execute(select(Image).order_by(Image.id))
    print(props.all())
    print(imgs.all())
    # db.drop_all()
    # db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
