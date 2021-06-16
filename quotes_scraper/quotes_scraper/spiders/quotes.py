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
        'CONCURRENT_REQUESTS': 24,
        'MEM_USAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['test@example.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Whatever',
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
        top_tags = response.xpath("//div[contains(@class, 'tags-box')]/span[@class='tag-item']/a/text()").getall()

        yield {
            'title': title,
            'top_tags': top_tags,
        }

        next_link = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(next_link, callback=self.parse_quotes_only, cb_kwargs={'quotes': quotes})

        limit_tag = getattr(self, 'limit_tag', None)
        if limit_tag is not None:
            try:
                top_tags = top_tags[:int(limit_tag)]
            except ValueError as e:
                raise ValueError("Argument limit_tag must be an integer")
            
        