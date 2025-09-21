# The most basic spider to get started with Scrapy
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/page/1/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('--' * 20)
        print(response.css('div.quote'))
        # The response.css('div.quote') returns a list of Selector objects with all the divs that have the class 'quote'
        print('--' * 20)