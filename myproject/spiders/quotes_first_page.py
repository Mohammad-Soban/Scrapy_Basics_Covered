import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes_first_page"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/page/1/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quotes = response.css('div.quote')

        for quote in quotes:
            quote_text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').getall()

            yield {
                'quote': quote_text,
                'author': author,
                'tags': tags
            }