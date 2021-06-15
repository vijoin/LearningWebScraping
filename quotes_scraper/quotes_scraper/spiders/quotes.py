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

    def parse(self, response):

        next_link = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(next_link, callback=self.parse)

        yield {
            'title': response.xpath("//h1/a/text()").get(),
            'quotes': response.xpath("//div[@class='quote']/span[@class='text' and @itemprop='text']/text()").getall(),
            'top_ten_tags': response.xpath("//div[contains(@class, 'tags-box')]/span[@class='tag-item']/a/text()").getall(),
        }
