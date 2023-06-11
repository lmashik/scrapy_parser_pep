import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        numerical_index = response.xpath('//section[@id="numerical-index"]')
        peps = numerical_index.css('tbody tr a::attr(href)').getall()
        for pep_link in peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = ' '.join(
            t.strip() for t in response.css('article h1::text').getall()
        ).strip()
        number, name = (item.strip() for item in title.split('–'))
        number = number.replace('PEP ', '')
        status = response.xpath(
            '//*[contains(., "Status")]/following-sibling::*/child::*/text()'
        ).get()
        data = {
            'number': number,
            'name': name,
            'status': status,
        }
        yield PepParseItem(data)
