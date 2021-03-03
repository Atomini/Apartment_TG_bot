import scrapy
from scrapy.crawler import CrawlerProcess
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
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(AlfaSpider)
    process.start()  # the script will block here until the crawling is finished
    process.stop()


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(AlfaSpider)
    process.start(stop_after_crawl=False)  # the script will block here until the crawling is finished
    process.stop()