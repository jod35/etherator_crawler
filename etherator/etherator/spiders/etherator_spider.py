import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from datetime import datetime as dt
from datetime import timedelta as td
from scrapy.spiders import CrawlSpider, Rule, Spider
from itemloaders.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags, replace_escape_chars
# from nltk.tokenize import sent_tokenize, word_tokenize

from ..models import HostnameClass, session, engine

with engine.connect():
    result = session.query(HostnameClass.hostname).all()
    start_urls_list = []
    allowed_domains_list = []
    for i in result:
        url = "http://" + i[0]
        start_urls_list.append(url)
        allowed_domains_list.append(i[0])
    print(start_urls_list[1:5])
    print(allowed_domains_list[1:5])


class PageItem(scrapy.Item):
    hostname = scrapy.Field(input_processor=MapCompose(),
                            output_processor=TakeFirst())
    human_text = scrapy.Field(input_processor=MapCompose(
        replace_escape_chars), output_processor=TakeFirst())
    title = scrapy.Field(input_processor=MapCompose(),
                         output_processor=TakeFirst())
    h1 = scrapy.Field(input_processor=MapCompose(),
                      output_processor=TakeFirst())
    urls = scrapy.Field(input_processor=Join(
        ','), output_processor=TakeFirst())
    scheme = scrapy.Field(input_processor=MapCompose(),
                          output_processor=TakeFirst())
    image_urls = scrapy.Field()


class EtheratorSpiderSpider(scrapy.Spider):
    name = 'etherator_spider'
    allowed_domains = allowed_domains_list
    start_urls = start_urls_list

    def parse(self, response):

        l = ItemLoader(item=PageItem(), selector=response)
        l.add_value('human_text', BeautifulSoup(
            response.body.decode(response.encoding)).text)
        l.add_css('title', 'title::text')
        l.add_value('title', 'none')
        l.add_css('h1', 'h1::text')
        l.add_value('h1', 'none')
        l.add_value('scheme', urlparse(response.url).scheme)
        l.add_value('hostname', urlparse(response.url).hostname)
        print(f'in {repr(response)}')

        #image_urls = []

        for link in response.css('a::attr(href)').getall():
            #print(f'Link is {repr(link)}')
            hostname_to_follow = "https://" + str(urlparse(link).hostname)
            yield response.follow(hostname_to_follow, callback=self.parse)
        # get image urls
        # for path in response.css('img::attr(src)').getall():
        #     if path is not None and 'http' in path:
        #         image_urls.append(path)
        #     else:
        #         image_urls.append(response.url + path)

        # l.add_value('urls', links)
        # l.add_value('urls', 'none')
        # l.add_value('image_urls', image_urls)
        # l.add_value('tokenized_words', BeautifulSoup(
        #     response.body.decode(response.encoding)).text)
        yield l.load_item()

    def on_error(self, failure):
        print(f'error {failure}, {failure.value}')
