import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Join, MapCompose, Identity
from myproject.items import QuoteItem

def clean_quote(text):
    return text.replace('“', '').replace('”', '').strip()

def make_tags_in_string(tags):
    return ", ".join(tags)


class QuoteLoader(ItemLoader):
    default_output_processor = TakeFirst()
    tags_in = MapCompose(str.strip)
    tags_out = Identity()


class QuotesSpider(scrapy.Spider):
    name = "quotes_with_item_loader_and_processors"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/page/1/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quotes = response.css('div.quote')

        for quote in quotes:
            loader = QuoteLoader(item=QuoteItem(), selector=quote)

            loader.add_css('quote', 'span.text::text', MapCompose(clean_quote))
            loader.add_css('author', 'small.author::text')
            loader.add_xpath('tags', './/div[@class="tags"]/a[@class="tag"]/text()')
            yield loader.load_item()

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)