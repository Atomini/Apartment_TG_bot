import scrapy
from scrapy.crawler import CrawlerProcess



class FlafySpider(scrapy.Spider):
    name = 'flafy'
    start_urls = ['https://flatfy.ua/search?currency=UAH&geo_id=27&price_max=650000&section_id=1']

    def parse(self, response):
        last_page = response.xpath('//*[@class="paging-button"]/text()').extract()
        if int(last_page[-1]) > 3:
            pages: int = 3
        else:
            pages: int = int(last_page)

        for page in range(0, pages):
            url = f'https://flatfy.ua/search?currency=UAH&geo_id=27&page={page}&price_max=650000&section_id=1'
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response, **kwargs):
        link = response.xpath('//*[@rel="nofollow noopener"]/@href').extract()
        title = response.xpath('//*[@rel="nofollow noopener"]/text()').extract()
        district = response.xpath('//*[@class="realty-preview__sub-title"]/a[1]/text()').extract()
        # '//*[@id="380231826"]/div[1]/div[1]/div/div[1]/div[1]/div[2]/a[1]/text()'
        print(link)
        print(title)
        print(district)
        print(len(link), "-",len(title), "-",len(district))

if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(FlafySpider)
    process.start()  # the script will block here until the crawling is finished
