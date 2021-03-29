import scrapy
from scrapy.crawler import CrawlerProcess


class DomRiaSpider(scrapy.Spider):
    name = 'dom_ria'
    allowed_domains = ['https://dom.ria.com']
    start_urls = ['https://dom.ria.com/uk/search/#category=1&realty_type=2&operation_type=1&state_id=20&city_id=20'
                  '&inspected=0&period=0&notFirstFloor=0&notLastFloor=0&with_photo=1&links-under-filter=on'
                  '&fullCategoryOperation=1_2_1&wo_dupl=1&page=0&limit=20&sort=inspected_sort&csrf=R2loNU6v-o3qvHdZR'
                  '-qCxHhoTmEM0sl5-Q8Y&ch=234_t_25000,242_239,247_252,'
                  '265_0&d_id=9718:15291:15362:15363:15971:16093:16958:17017:17018:17019:17216:17217:17284:17467'
                  ':17468:17469:17471:17472:17473:17475:17476:17477:17478:17479:17480:17481:17484:17487:17488:17489'
                  ':17492:17494:17495:17524:17611:17616:17617:17935:17936:17937:17938:17939:17940:17941:17943:17944'
                  ':17945:17946:17947']

    def parse(self, response):
        for href in response.css('.search-realty-19436948 > a.all-clickable::attr(href)'):
            # search-realty-19436948 > a.all-clickable.unlink
            url = response.urljoin(href.extract())
            print(href)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        name = response.xpath('/html/body/div[2]/form/section/div[4]/div[6]/div[3]/a[2]')
        print(name)
        yield name


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(DomRiaSpider)
    process.start()  # the script will block here until the crawling is finished
