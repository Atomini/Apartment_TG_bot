from database.table_function import add_to_course
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


class AlfaSpider(scrapy.Spider):
    name = 'alfa'
    start_urls = ['https://alfabank.ua/ru/']

    def parse(self, response):
        dollar_sales = response.xpath('//*[@id="new-layout"]/main/section[3]/div/div[4]'
                                      '/div[1]/div[2]/span[2]/text()').extract()
        euro_sales = response.xpath('//*[@id="new-layout"]/main/section[3]/div/div[4]'
                                    '/div[2]/div[2]/span[2]/text()').extract()
        euro_dollar_sales = response.xpath('//*[@id="new-layout"]/main/section[3]/div/div[4]'
                                           '/div[3]/div[2]/span[2]/span/text()').extract()
        print(euro_sales[0].strip(), dollar_sales[0].strip(), euro_dollar_sales[0])
        add_to_course(euro_sales[0].strip(), dollar_sales[0].strip(), euro_dollar_sales[0])
        yield euro_sales[0].strip(), dollar_sales[0].strip(), euro_dollar_sales[0]


def start_alfa():
    result_queue1 = mp.Queue()
    crawler = CrawlerWorker((AlfaSpider), result_queue1)
    crawler.start()
    crawler.join()


if __name__ == "__main__":
    import time
    start_alfa()

    time.sleep(5)
    start_alfa()


