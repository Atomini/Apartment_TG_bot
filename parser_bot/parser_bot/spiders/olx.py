import scrapy
from scrapy.crawler import CrawlerProcess


class OlxSpider(scrapy.Spider):
    name = 'olx'
    start_urls = [
        'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/poltava/?search%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_float_price%3Ato%5D=680000']

    # def parse(self, response):
    #     for page in range(1, 2):
    #         url = f'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/poltava/?search' \
    #               f'%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_float_price%3Ato%5D=680000&page={page}'
    #         yield scrapy.Request(url=url,
    #                              callback=self.parse_page)
    #
    #
    #
    # def parse_page(self, response):
    #     title = response.xpath('//*[@id="body-container"]/div[3]/div/div[1]/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[2]/div/h3/a/@href')
    #     yield title
    def parse(self, response, **kwargs):
        # title = response.xpath('//*[@id="body-container"]/div[3]/div/div[1]/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[2]/div/h3/@href').extract()
        title = response.xpath('//*[@class="lheight22 margintop5"]/a/@href').extract()

        yield {"title": title}


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218'
    })
    process.crawl(OlxSpider)
    process.start()  # the script will block here until the crawling is finished
