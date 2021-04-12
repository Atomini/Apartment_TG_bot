import scrapy


class FlafySpider(scrapy.Spider):
    name = 'flafy'
    start_urls = ['https://flatfy.ua/search?currency=UAH&geo_id=27&price_max=650000&section_id=1']

    def parse(self, response):
        last_page = response.xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div[3]/div[1]/a[4]').extract()

        if int(last_page) > 3:
            pages: int = 3
        else:
            pages: int = int(last_page)

        for page in range(0, pages):
            url = f'https://flatfy.ua/search?currency=UAH&geo_id=27&page={page}&price_max=650000&section_id=1'
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response, **kwargs):
        link = response.xpath('//*[@rel="nofollow noopener"]/@href').extract()
        title = response.xpath('//*[@rel="nofollow noopener"]/text()').extract()
        district = response.xpath('//*[@class="realty-preview__sub-title"]/text()').extract()

        'realty-preview__sub-title'
