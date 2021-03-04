import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue

import twisted
from twisted.internet import reactor
from database.table_function import add_to_course


class AlfaSpider(scrapy.Spider):
    name = 'alfa'
    allowed_domains = ['https://alfabank.ua/ru']
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
    process = crawler.CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    try:
        process.crawl(AlfaSpider)
        process.start()  # the script will block here until the crawling is finished
        process.stop()
    except twisted.internet.error.ReactorNotRestartable:
        process.crawl(AlfaSpider)
        process.stop()


# def start_alfa(spider=AlfaSpider):
#     def f(q):
#         try:
#             runner = crawler.CrawlerRunner()
#             deferred = runner.crawl(spider)
#             deferred.addBoth(lambda _: reactor.stop())
#             reactor.run()
#             q.put(None)
#         except Exception as e:
#             q.put(e)
#
#     q = Queue()
#     p = Process(target=f, args=(q,))
#     p.start()
#     result = q.get()
#     p.join()
#
#     if result is not None:
#         raise result


if __name__ == "__main__":
    process = crawler.CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(AlfaSpider)
    process.start(stop_after_crawl=False)  # the script will block here until the crawling is finished
    process.stop()
