import json
import database
import logging
import multiprocessing as mp
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.signals import item_passed
from scrapy.utils.project import get_project_settings
from pydispatch import dispatcher


class CrawlerWorker(mp.Process):
    name = "crawlerworker"

    def __init__(self, spider, result_queue):
        mp.Process.__init__(self)
        self.result_queue = result_queue
        self.items = list()
        self.spider = spider
        self.logger = logging.getLogger(self.name)

        self.settings = get_project_settings()
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Create CrawlerProcess with settings {}".format(self.settings))
        self.crawler = CrawlerProcess(self.settings)

        dispatcher.connect(self._item_passed, item_passed)

    def _item_passed(self, item):
        self.logger.debug("Adding Item {} to {}".format(item, self.items))
        self.items.append(item)

    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        self.crawler.stop()
        self.result_queue.put(self.items)


class DomRiaSpider(scrapy.Spider):
    name = 'dom_ria'
    start_urls = [
        'https://dom.ria.com/uk/search/#category=1&realty_type=2&operation_type=1&city_id=20&state_id=20'
        '&limit=0&ch=234_t_25000,242_239,247_252,265_0&wo_dupl=1&page=0']
    headers = {
        "accept": "* / *",
        "accept - encoding": "gzip, deflate, br",
        "accept - language": "ru - RU, ru;q = 0.9, en - US;q = 0.8, en;q = 0.7",
        "referer": "https: // dom.ria.com / uk / search /",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome /"
                      " 88.0.4324.192 Safari / 537.36 OPR / 74.0.3911.218",
        "x-requested-with": "XMLHttpRequest"
    }

    def parse(self, response):
        for page in range(0, 1): # Указать количество страниц для поиска
            url = f"https://dom.ria.com/searchEngine/?links-under-filter=on&category=1&realty_type=2&operation_type=1&" \
                  f"fullCategoryOperation=1_2_1&wo_dupl=1&page={page}&state_id=20&city_id=20&limit=20&sort" \
                  f"=inspected_sort&characteristic%5B234%5D%5Bto%5D=25000&characteristic%5B242%5D=239&characteristic" \
                  f"%5B247%5D=252&characteristic%5B265%5D=0 "
            yield scrapy.Request(url=url,
                                 callback=self.parse_page,
                                 headers=self.headers)

    def parse_page(self, response):
        page_data = response.body
        data = json.loads(page_data)
        for apartment in data["items"]:
            link = "https://dom.ria.com/uk/" + apartment['beautiful_url']
            description = apartment['description']
            try:
                district = apartment['district_name']
            except KeyError:
                district = "Не указан"
            try:
                latitude = apartment['latitude']
                longitude = apartment["longitude"]
            except KeyError:
                longitude = None
                latitude = None
            price_USD = int(apartment["priceArr"]["1"].replace(" ", ""))
            price_EUR = int(apartment["priceArr"]["2"].replace(" ", ""))
            price_UAH = int(apartment["priceArr"]["3"].replace(" ", ""))
            try:
                street_name = apartment["street_name"]
            except:
                street_name = "не указан("
            building_number = apartment["building_number_str"]
            publishing_date = apartment["publishing_date"][0:10]
            photo_link = [
                ("https://cdn.riastatic.com/photos/" + (apartment["photos"][photo]["file"]).replace('.jpg', 'b.webp'))
                for photo in apartment["photos"]]
            database.add_data_to_table_domria(link, description, latitude, longitude, price_USD, price_EUR, price_UAH,
                                              street_name, building_number, publishing_date, str(photo_link))


def start_domria():
    result_queue1 = mp.Queue()
    crawler = CrawlerWorker(DomRiaSpider, result_queue1)
    crawler.start()
    crawler.join()


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218'
    })
    process.crawl(DomRiaSpider)
    process.start()  # the script will block here until the crawling is finished
