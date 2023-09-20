import json

from sqlalchemy import select
from tqdm import tqdm

from database import db
from models import Property, Image


def read_json(path: str) -> list:
    with open(path, "r") as f:
        json_lst = json.load(f)
    return json_lst


def fill_db():

    # Read webscraped JSON
    PATH_JSON = "web_scrape.json"
    json_lst = read_json(PATH_JSON)

    if len(json_lst) < 19:
        raise ValueError(f"Only {len(json_lst)} properties are scraped.")

    # Needs to be inside Flask app context
    TOTAL_COUNT = 500
    pbar = tqdm(total=TOTAL_COUNT)
    for json_prop in json_lst:
        if len(db.session.execute(select(Property).order_by(Property.id)).all()) >= TOTAL_COUNT:
            break
        prop_tmp = Property(
            title=json_prop["title"],
            title_url=json_prop["title_url"],
            price=json_prop["price"],
            description=json_prop["description"]
        )
        db.session.add(prop_tmp)
        db.session.commit()
        prop_id_tmp = prop_tmp.id
        pbar.update(1)
        db.session.add(Image(property_id=prop_id_tmp, url=json_prop["imgs_urls"][0]))
        db.session.add(Image(property_id=prop_id_tmp, url=json_prop["imgs_urls"][1]))
        db.session.add(Image(property_id=prop_id_tmp, url=json_prop["imgs_urls"][2]))
        db.session.commit()
    props = db.session.execute(select(Property).order_by(Property.id))
    imgs = db.session.execute(select(Image).order_by(Image.id))
    # print(props.all())
    # print(imgs.all())
    print(f"Database filled. Total count: {len(db.session.execute(select(Property).order_by(Property.id)).all())}\n")