import re
import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']
    custom_settings = {
        'FEED_EXPORT_FIELDS': ['Номер', 'Название', 'Статус'],
    }

    def parse(self, response):
        numerical_index = response.xpath('//section[@id="numerical-index"]')
        peps = numerical_index.css('tbody tr a::attr(href)').getall()
        for pep_link in peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        pattern = r'PEP (?P<number>\d+) – (?P<name>.*)'
        # title = response.css('article h1::text').get()
        title = ' '.join(
            t.strip() for t in response.css('article h1::text').getall()
        ).strip()
        number, name = (item.strip() for item in title.split('–'))
        # text_match = re.search(pattern, title)
        # number, name = text_match.groups()
        status = response.xpath(
            '//*[contains(., "Status")]/following-sibling::*/child::*/text()'
        ).get()
        data = {
            'number': number,
            'name': name,
            'status': status,
        }
        yield PepParseItem(data)
