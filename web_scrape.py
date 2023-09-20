import json

import scrapy

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

# if __name__ == "__main__":
#     crawler_process.crawl(SrealitySpider2)
#     crawler_process.start()  # the script will block here until the crawling is finished
#     # scrp = SrealitySpider()
#     # resp = scrp.start_requests()
#     # next(resp)