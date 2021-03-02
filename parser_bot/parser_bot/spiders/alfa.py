import scrapy
from scrapy.crawler import CrawlerProcess


class AlfaSpider(scrapy.Spider):
    name = 'alfa'
    allowed_domains = ['https://alfabank.ua/ru']
    start_urls = ['https://alfabank.ua/ru/']

    def parse(self, response):
        euro_sales = response.xpath('//*[@id="new-layout"]/main/section[3]/div/div[4]/div[1]/div[2]/span[2]/text()').extract()
        dollar_sales = response.xpath('//*[@id="new-layout"]/main/section[3]/div/div[4]/div[2]/div[2]/span[2]/text()').extract()
        print(euro_sales, dollar_sales)
        yield euro_sales, dollar_sales
        # for item in zip(euro_sales, dollar_sales):
        #     da = item[0]
        #     yield da

if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(AlfaSpider)
    process.start()  # the script will block here until the crawling is finished