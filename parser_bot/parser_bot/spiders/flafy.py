import logging
import multiprocessing as mp
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.signals import item_passed
from scrapy.utils.project import get_project_settings
from pydispatch import dispatcher
import database


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


class FlafySpider(scrapy.Spider):
    name = 'flafy'
    start_urls = ['https://flatfy.ua/search?currency=UAH&geo_id=27&price_max=650000&section_id=1']

    def parse(self, response):
        last_page = response.xpath('//*[@class="paging-button"]/text()').extract()
        # сделанно для проработки только трех первых странци для полой пророботки заменить на pages = last_page
        if int(last_page[-1]) > 3:
            pages: int = 3          # значение на сколько страниц в глубину прорабатывать
        else:
            pages: int = int(last_page)

        for page in range(0, pages):
            url = f'https://flatfy.ua/search?currency=UAH&geo_id=27&page={page}&price_max=650000&section_id=1'
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response, **kwargs):
        link = response.xpath('//*[@class="realty-preview"]/@id').extract()
        title = response.xpath('//*[@rel="nofollow noopener"]/text()').extract()
        district = response.xpath('//*[@class="realty-content-layout__sub-title-row"]/a[1]/text()').extract()
        price = response.xpath('//*[@class="realty-preview__price"]/text()').extract()
        print(title)
        for items in zip(title, price, link, district):
            database.add_data_to_table_flafy(items[0], items[1], f"https://flatfy.ua/redirect/{items[2]}", items[3])


def start_flafy():
    result_queue1 = mp.Queue()
    crawler = CrawlerWorker(FlafySpider, result_queue1)
    crawler.start()
    crawler.join()


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(FlafySpider)
    process.start()  # the script will block here until the crawling is finished
