# get all links with articles
# response.xpath('//a[starts-with(@href, "collection/") and (parent::h2|parent::h3)]/@href').getall()

import scrapy
from scrapy.http import Response


class CiaSpider(scrapy.Spider):
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections',
        ]
    custom_settings = {
        'FEEDS' : {
            'cia.json' : {
                'format': 'json',
                'encoding': 'utf-8',
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
        links_declassified = response.xpath('//a[starts-with(@href, "collection/") and (parent::h2|parent::h3)]/@href').getall()
        for link in links_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})
        

    def parse_link(self, response, **kwargs):
        link = kwargs.get('url')
        title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
        body = "".join(response.xpath('//div[@class="field-item even"]//p[3]/text()').getall())

        yield {
            'url': link,
            'title': title,
            'body': body,
        }
