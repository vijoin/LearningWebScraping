import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
    ]
    custom_settings = {
        'FEEDS': {
            'quotes.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            },
        },
    }

    def parse_quotes_only(self, response, **kwargs):
        quotes = kwargs.get('quotes')
        if quotes:
            quotes.extend(response.xpath("//span[@class='text' and @itemprop='text']/text()").getall())
        
        next_link = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(next_link, callback=self.parse_quotes_only, cb_kwargs={'quotes': quotes})  
        else:
            yield {
                'quotes': quotes
            }

    def parse(self, response):

        title = response.xpath("//h1/a/text()").get()
        quotes = response.xpath("//span[@class='text' and @itemprop='text']/text()").getall()
        top_ten_tags = response.xpath("//div[contains(@class, 'tags-box')]/span[@class='tag-item']/a/text()").getall()

        next_link = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(next_link, callback=self.parse_quotes_only, cb_kwargs={'quotes': quotes})

        yield {
            'title': title,
            'quotes': quotes,
            'top_ten_tags': top_ten_tags,
        }
