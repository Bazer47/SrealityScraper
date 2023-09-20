import os

from flask import Flask
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

from database import db
from fill_database import fill_db
from web_scrape import SrealitySpider2

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:secret@db:5432/postgres"
db.init_app(app)

from views import *

def run_spider(spider):
    def f(q):
        try:
            runner = crawler.CrawlerRunner(settings={
                "FEEDS": {
                    "web_scrape.json": {"format": "json", 'encoding': 'utf8', 'indent': 4},
                }})
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

if os.path.exists("web_scrape.json"):
    os.remove("web_scrape.json")
run_spider(SrealitySpider2)


with app.app_context():
    db.create_all()
    # Fill the DB from JSON
    fill_db()

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
