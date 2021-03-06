import re
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


class NovobudSpider(scrapy.Spider):
    name = 'novobud'
    allowed_domains = ['novobud.pl.ua']
    start_urls = ['http://novobud.pl.ua/']

    def parse(self, response):
        for href in response.css('.portfolio-card a::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        status = response.xpath('//*[@id="content-page"]/div[1]/div/div[1]/div[1]/div/div[1]/span').extract()
        price = response.xpath('//*[@class="price-count"]/text()').extract()
        district = response.xpath('//*[@class="one-product__region"]/span/text()').extract()
        address = response.xpath('//*[@class="one-product__street"]/text()').extract()
        image = response.xpath('//*[@id="swiper-wrapper-7e6eba31691cc5c10"]/div[1]/a/@href').extract()
        map_ = response.xpath('//*[@class="zoommaps"]/@href').extract()
        construction_end = response.xpath('//*[@id="content-page"]/div[1]/div/div[2]'
                                          '/div/div[3]/span[2]/text()').extract()
        description = response.xpath('//*[@id="content-page"]/div[1]/div/div[2]/div/div[4]/p[2]/text()').extract()
        for item in zip(status, price, district, address, image, map_, construction_end, description):
            if item[0] != '<span>Все продано</span>' and item[0] != "<span>Всё продано</span>" \
                    and item[0] != "<span>Все проодано</span>":
                scraped_data = {
                    "Статус": str(item[0]).replace("<span>", "").replace("</span>", ""),
                    "Цена": item[1],
                    "link": response.url,
                    "Район": item[2],
                    "Адресс": str(item[3]).replace('\n', "").replace("  ", ""),
                    "Картинка": "https://novobud.pl.ua" + str(item[4]),
                    "Карта долгота": re.findall(r"\d{2}.\d+", item[5])[0],
                    "Карта широта": re.findall(r"\d{2}.\d+", item[5])[1],
                    "Окончание постройки": item[6],
                    "Описание": str(item[7]).replace("\\xa", " ")
                }
                # запись получених данных в базу даных
                database.add_data_to_table_novobud(scraped_data["Статус"],
                                                   scraped_data["Район"],
                                                   scraped_data["Адресс"],
                                                   scraped_data["Описание"],
                                                   scraped_data["Окончание постройки"],
                                                   scraped_data["link"],
                                                   scraped_data["Картинка"],
                                                   scraped_data["Цена"],
                                                   scraped_data["Карта долгота"],
                                                   scraped_data["Карта широта"]
                                                   )
            else:
                continue
            yield scraped_data


def start_novobud():
    result_queue1 = mp.Queue()
    crawler = CrawlerWorker(NovobudSpider, result_queue1)
    crawler.start()
    crawler.join()


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(NovobudSpider)
    process.start()  # the script will block here until the crawling is finished
