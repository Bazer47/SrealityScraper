from pathlib import Path

# from app import app
import scrapy
from scrapy.crawler import CrawlerProcess


class SrealitySpider(scrapy.Spider):
    name = 'sreality_spider'
    N_OF_PAGES = 26
    urls = ["https://www.sreality.cz/hledani/prodej/byty"]
    urls_pages = ["https://www.sreality.cz/hledani/prodej/byty?strana=" + str(i) for i in range(N_OF_PAGES)]
    urls = urls + urls_pages

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set(
            "DOWNLOAD_HANDLERS",
            {
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            priority="spider"
        )
        settings.set(
            "TWISTED_REACTOR",
            "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            priority="spider"
        )

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        N_OF_IMAGES = 3
        PAGE_RANGE = 20
        BASE_URL = "https://www.sreality.cz"
        for i_property in range(PAGE_RANGE):
            prop = response.css('div.property')[i_property]
            title = prop.css('span.name::text').get()
            title_url = prop.css('a.title::attr(href)').get()
            title_url = BASE_URL + title_url
            price = prop.css('span.norm-price::text').get()
            description = prop.css('span.locality::text').get()
            imgs_urls = []
            for i_img in range(N_OF_IMAGES):
                imgs_urls.append(prop.css('img::attr(src)')[i_img].get())
            yield {
                "title": title,
                "title_url": title_url,
                "description": description,
                "price": price,
                "imgs_urls": imgs_urls
            }
    
    # def make_request(self):
    #     return scrapy.Request(url=self.start_url)

crawler_process = CrawlerProcess(
    settings={
        "FEEDS": {
            "web_scrape.json": {"format": "json", 'encoding': 'utf8', 'indent': 4},
        },
    }
)


if __name__ == "__main__":
    crawler_process.crawl(SrealitySpider)
    crawler_process.start()  # the script will block here until the crawling is finished
    # scrp = SrealitySpider()
    # resp = scrp.start_requests()
    # next(resp)