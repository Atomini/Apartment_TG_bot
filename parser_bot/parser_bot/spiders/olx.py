import scrapy
from scrapy.crawler import CrawlerProcess



class OlxSpider(scrapy.Spider):
    name = 'olx'
    start_urls = ['https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/poltava/?search%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_float_price%3Ato%5D=680000&page=1']

    def parse(self, response, **kwargs):
        last_page = response.xpath('//*[@data-cy = "page-link-last"]/span/text()').extract()
        for page in range(1, int(last_page[0])+1):
            url = f'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/poltava/?search' \
                  f'%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_float_price%3Ato%5D=680000&page={page}'
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response, **kwargs):
        title = response.xpath('//*[@data-cy = "listing-ad-title"]/strong/text()').extract()
        price = response.xpath('//*[@class = "price"]/strong/text()').extract()
        print(title)
        print(price)


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
    #
    # def parse_page(self, response):
    #     print(response.url)
    #     title = response.xpath('/html/head').extract()
    #     yield {"title": title}


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 OPR/75.0.3969.149'
    })
    process.crawl(OlxSpider)
    process.start()  # the script will block here until the crawling is finished
