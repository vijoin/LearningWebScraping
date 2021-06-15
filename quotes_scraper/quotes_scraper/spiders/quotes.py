import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):
        print("\n\n\n")
        title = response.xpath("//h1/a/text()").get()
        quotes = response.xpath("//div[@class='quote']/span[@class='text' and @itemprop='text']/text()").getall()
        top_ten_tags = response.xpath("//div[contains(@class, 'tags-box')]/span[@class='tag-item']/a/text()").getall()
        print(title,quotes,top_ten_tags)
        print("\n\n\n")
