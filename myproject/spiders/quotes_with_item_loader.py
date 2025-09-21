import scrapy
from scrapy.loader import ItemLoader
from myproject.items import QuoteItem  

class QuotesSpider(scrapy.Spider):
    name = "quotes_with_item_loader"

    def start_requests(self):
        url = "http://quotes.toscrape.com/page/1"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quotes = response.css('div.quote')

        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_css('quote', 'span.text::text')
            loader.add_css('author', 'small.author::text')
            loader.add_xpath('tags', './/div[@class="tags"]/a[@class="tag"]/text()')

            yield loader.load_item()

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)