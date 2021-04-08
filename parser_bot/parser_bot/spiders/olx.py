import scrapy
from scrapy.crawler import CrawlerProcess


class OlxSpider(scrapy.Spider):
    name = 'olx'
    start_urls = [
        'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/poltava/?search'
        '%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_float_price%3Ato%5D=680000']

    def parse(self, response, **kwargs):
        last_page = response.xpath('//*[@data-cy = "page-link-last"]/span/text()').extract()
        for page in range(1, int(last_page[0])+1):
            url = f'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/poltava/?search' \
                  f'%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_float_price%3Ato%5D=680000&page={page}'
            yield scrapy.Request(url, callback=self.parse_big_page)

    def parse_big_page(self, response, **kwargs):
        link = response.xpath('//*[@class="lheight22 margintop5"]/a/@href').extract()
        for href in link:
            url = response.urljoin(href.extract())
            yield scrapy.Request(url=url,
                                 callback=self.parse_page)

    def parse_page(self, response, **kwargs):
        title = response.xpath('//*[@data-cy="ad_title"]/text()').extract()
        yield {"title": title}

        # title = response.xpath('//*[@id="root"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/h1').extract()
        # print(title)
        # title = response.xpath('//*[@class="lheight22 margintop5"]/a/@href').extract()
        # count = 0
        # for href in title:
        #     count += 1
        #     print(count, "-",href)

        # yield {"title": title}


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218 '
    })
    process.crawl(OlxSpider)
    process.start()  # the script will block here until the crawling is finished
