import scrapy


class SpiderBookStore(scrapy.Spider):
    name = 'bookstore'
    start_urls = [
        'https://books.toscrape.com/catalogue/page-1.html',
    ]
    custom_settings = {
        'FEEDS': {
            'books.json': {
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
        'MEMUSAGE_NOTIFY_MAIL': ['vijoin@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Whatever',
    }

    def parse_book(self, response):
        title = response.xpath('//h1/text()').get()
        price = response.xpath('//th[contains(text(), "Price (incl. tax)")]/following-sibling::td/text()').get()
        stock_available = response.xpath('//th[contains(text(), "Availability")]/following-sibling::td/text()').get()

        yield {
            'title': title,
            'price': float(price.replace('£', '')), #Improve with a regex
            'stock_available': int(stock_available.replace('In stock (', '').replace(' available)', '')) #Improve with a regex
        }

    def parse(self, response, **kwargs):

        # Parse all book links first
        book_links = kwargs.get('book_links')
        if book_links:
            book_links.extend(response.xpath('//ol[@class="row"]/li//h3/a/@href').getall())
        else:
            book_links = response.xpath('//ol[@class="row"]/li//h3/a/@href').getall()

        next_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_link:
            yield response.follow(next_link, callback=self.parse, cb_kwargs={'book_links': book_links})
        else:
            # Parse all books
            for book_link in book_links:
                yield response.follow(book_link, callback=self.parse_book)
