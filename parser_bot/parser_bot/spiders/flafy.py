import scrapy
from scrapy.crawler import CrawlerProcess


class FlafySpider(scrapy.Spider):
    name = 'flafy'
    start_urls = ['https://flatfy.ua/search?currency=UAH&geo_id=27&price_max=650000&section_id=1']

    def parse(self, response):
        last_page = response.xpath('//*[@class="paging-button"]/text()').extract()
        if int(last_page[-1]) > 3:
            pages: int = 1
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
        image = response.xpath('//*[@class="realty-preview__image-holder"]/picture/img').extract()

        print(link)
        print(title)
        print(district)
        print(price)
        print(image)
        print(len(link), "-", len(title), "-", len(district), "-", len(price))


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(FlafySpider)
    process.start()  # the script will block here until the crawling is finished


