import json

import scrapy


class SrealitySpider(scrapy.Spider):
    name = 'sreality_spider'
    N_OF_PAGES = 1
    urls = ["https://www.sreality.cz/hledani/prodej/byty"]
    # urls_pages = ["https://www.sreality.cz/hledani/prodej/byty?strana=" + str(i) for i in range(N_OF_PAGES)]
    # urls = urls + urls_pages

    # @classmethod
    # def update_settings(cls, settings):
    #     super().update_settings(settings)
    #     settings.set(
    #         "DOWNLOAD_HANDLERS",
    #         {
    #             "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    #             "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    #         },
    #         priority="spider"
    #     )
    #     # settings.set(
    #     #     "TWISTED_REACTOR",
    #     #     # "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    #     #     "twisted.internet.epollreactor.EPollReactor",
    #     #     priority="spider"
    #     # )

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        with open('page.html', 'wb') as html_file:
            html_file.write(response.body)
        N_OF_IMAGES = 3
        PAGE_RANGE = 3
        BASE_URL = "https://www.sreality.cz"
        props = response.css('div.property')
        for i_property in range(PAGE_RANGE):
            prop = props[i_property]
            print(f"{prop = }")
            title = prop.css('span.name').get()
            print(f"{title = }")
            title_url = prop.css('a.title::attr(href)').get()
            title_url = BASE_URL + title_url
            price = prop.css('span.norm-price').get()
            print(f"{price = }")
            description = prop.css('span.locality::text').get()
            print(f"{description = }")
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

class SrealitySpider2(scrapy.Spider):
    name = 'sreality_spider_2'
    BASE_URL = "https://www.sreality.cz"
    N_OF_IMGS = 3
    N_OF_ITEMS = 500
    url = f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page={N_OF_ITEMS}&tms=0"

    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            method="GET",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Host": "www.sreality.cz",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
                "TE": "trailers",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Dest": "cors",
                "Sec-Fetch-Dest": "same-origin",
                "Referer": "https://www.sreality.cz/hledani/prodej/byty"
            },
            callback=self.parse,
        )

    def parse(self, response):
        parsed_response = json.loads(response.body.decode("utf-8"))
        properties = parsed_response["_embedded"]["estates"]
        for prop in properties:
            name = prop["name"]
            prop_url_endp = prop["_links"]["self"]["href"]
            prop_url_endp = self.BASE_URL + "/api" + prop_url_endp
            locality = prop["locality"]
            price = prop["price"]
            # Get images
            imgs_urls = []
            for i_img, img in enumerate(prop["_links"]["images"]):
                if i_img == self.N_OF_IMGS:
                    break
                imgs_urls.append(img["href"])
            yield {
                "name": name,
                "prop_url_endp": prop_url_endp,
                "locality": locality,
                "price": price,
                "imgs_urls": imgs_urls
            }


# crawler_process = CrawlerProcess(
#     settings={
#         "FEEDS": {
#             "web_scrape.json": {"format": "json", 'encoding': 'utf8', 'indent': 4},
#         },
#         # "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
#         # "DOWNLOAD_HANDLERS": {
#         #     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#         #     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#         # },
#         # "CONCURRENT_REQUESTS": 32
#     }
# )


# if __name__ == "__main__":
#     crawler_process.crawl(SrealitySpider2)
#     crawler_process.start()  # the script will block here until the crawling is finished
#     # scrp = SrealitySpider()
#     # resp = scrp.start_requests()
#     # next(resp)