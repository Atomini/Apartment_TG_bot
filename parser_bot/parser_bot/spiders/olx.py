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


class OlxSpider(scrapy.Spider):
    name = 'olx'
    start_urls = [
        'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/poltava/?search'
        '%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_float_price%3Ato%5D=680000']

    def parse(self, response, **kwargs):
        last_page = response.xpath('//*[@data-cy = "page-link-last"]/span/text()').extract()
        for page in range(1, int(last_page[0]) + 1):
            url = f'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/poltava/?search' \
                  f'%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_float_price%3Ato%5D=680000&page={page}'
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response, **kwargs):
        title = response.xpath('//*[@data-cy = "listing-ad-title"]/strong/text()').extract()
        price = response.xpath('//*[@class = "price"]/strong/text()').extract()
        link = response.xpath('//*[@class = "lheight22 margintop5"]/a/@href').extract()
        # add_date = response.xpath('//*[@class = "breadcrumb x-normal"]/span[1]/text()').extract()
        image = response.xpath('//*[@class = "fleft"]/@src').extract()
        add_date = []
        for date in response.xpath('//*[@class = "breadcrumb x-normal"]/span[1]/text()').extract():
            if date != 'Полтава':
                add_date.append(date)
        for items in zip(title, price, link, image, add_date):
            database.add_data_to_table_olx(items[0], items[1], items[2], items[3], items[4])

    # ------------------------------для роботы нужно реализовать чтение динамической страницы в parse_page ----------
    # start_urls = [
    #     'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/poltava/?search'
    #     '%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_float_price%3Ato%5D=680000page=1']
    #
    # def parse(self, response):
    #     last_page = response.xpath('//*[@data-cy = "page-link-last"]/span/text()').extract()
    #     for page in range(2, int(last_page[0])+1):
    #         url = f'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/poltava/?search' \
    #               f'%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_float_price%3Ato%5D=680000&page={page}'
    #         yield scrapy.Request(url, callback=self.parse_big_page)
    #
    # def parse_big_page(self, response):
    #     link = response.xpath('//*[@class="lheight22 margintop5"]/a/@href').extract()
    #     for href in link:
    #         url = response.urljoin(href)
    #         yield scrapy.Request(url=url,
    #                              callback=self.parse_page)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #  не работает так как страныца генерируется динамически
    # def parse_page(self, response):
    #     print(response.url)
    #     title = response.xpath('/html/head').extract()
    #     yield {"title": title}


# ---------------------или---------------------------------------------
#  Работает но медленно на обработку одной ссылки уходит ~ 24 сек -> на 160 ссылок (4 страницы) ~ 66 минут
#     def parse_page(self, response):
#         from requests_html import HTMLSession
#         url = response.url
#         s = HTMLSession()
#         r = s.get(url)
#         r.html.render(sleep=1)
#         title = r.html.xpath('//*[@class="css-g5mtbi-Text"]/text()', first=True)
#         print(title)
#         print(url)

def start_olx():
    result_queue1 = mp.Queue()
    crawler = CrawlerWorker(OlxSpider, result_queue1)
    crawler.start()
    crawler.join()


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 OPR/75.0.3969.149'
    })
    process.crawl(OlxSpider)
    process.start()  # the script will block here until the crawling is finished
