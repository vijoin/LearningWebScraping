import scrapy
from scrapy.http.request import Request


# Get all links:
## response.xpath('//ol[@class="row"]/li//h3/a/@href').getall()
# Get Next page:
## response.xpath('//ol[@class="row"]/li//h3/a/@href').getall()
# and append page links to the list:
# scrape all of the links
class SpiderBookStore(scrapy.Spider):
    name = 'bookstore'
    start_urls = [
        'https://books.toscrape.com/catalogue/page-1.html',
    ]

    # Get all links:
    ## response.xpath('//ol[@class="row"]/li//h3/a/@href').getall()
    # Get Next page:
    ## response.xpath('//li[@class="next"]/a/@href').get()
    
    # and append page links to the list:
    ## logic

    # scrape all of the links
    ## title response.xpath('//h1/text()').get()
    ## price response.xpath('//th[contains(text(), "Price (incl. tax)")]/following-sibling::td/text()').get()
    ## stock_available response.xpath('//th[contains(text(), "Availability")]/following-sibling::td/text()').get()

    def start_requests(self):
        for
            yield Request()

    def get_book_links(self, url):
        response = 

    def parse_book(self, response):
        title = response.xpath('//h1/text()').get()
        price = response.xpath('//th[contains(text(), "Price (incl. tax)")]/following-sibling::td/text()').get()
        stock_available = response.xpath('//th[contains(text(), "Availability")]/following-sibling::td/text()').get()

        yield {
            'title': title,
            'price': float(price.replace('£', '')), #Improve with a regex
            'stock_available': int(stock_available.replace('In stock (', '').replace('In stock (', ''))
        }

    def parse(self, response):

         # Get all links:
    ## response.xpath('//ol[@class="row"]/li//h3/a/@href').getall()
    # Get Next page:
    ## response.xpath('//li[@class="next"]/a/@href').get()
        # Get all links


        book_links = response.xpath('//ol[@class="row"]/li//h3/a/@href').getall()
        next_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_link:
            book_links.extend(self.get_book_links(next_link))

        #parse all links
        for book in book_links:
            yield response.follow(book, callback=self.parse_book)