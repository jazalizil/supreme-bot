# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
from supreme.items import ProductItem
from scrapy.loader.processors import TakeFirst
from supreme.settings import SUPREME_BASE_URL


class ProductSpider(Spider):
    name = 'products'

    allowed_product_types = [
        'new', 'jackets', 'shirts', 'tops_sweaters', 'sweatshirts', 'pants', 'hats', 'bags', 'accessories', 'skate'
    ]

    def start_requests(self):
        for product_type in self.allowed_product_types:
            url = SUPREME_BASE_URL + 'shop/all/' + product_type
            if product_type is 'new':
                url = SUPREME_BASE_URL + 'shop/' + product_type
            yield Request(url, self.parse)

    @staticmethod
    def parse_product(response):
        splitted_url = response.url.split(SUPREME_BASE_URL)[1].split('/')
        selector = response.css('div#container')
        referer = response.request.headers.get('Referer', None)
        is_new = referer and 'new' in referer.split(SUPREME_BASE_URL)[1]

        loader = ItemLoader(item=ProductItem(), response=response, selector=selector)
        loader.default_output_processor = TakeFirst()

        loader.add_value('id', splitted_url[3])
        loader.add_value('collection_id', splitted_url[2])
        loader.add_value('type', splitted_url[1])
        loader.add_value('is_new', is_new)
        loader.add_value('url', response.url)
        loader.add_css('picture_url', 'img#img-main::attr(src)')
        loader.add_css('name', 'h1[itemprop="name"]::text')
        loader.add_css('description', 'p[itemprop="description"]::text')
        loader.add_css('model', 'p[itemprop="model"]::text')
        loader.add_css('price', 'span[itemprop="price"]::text')

        yield loader.load_item()

    def parse(self, response):
        product_urls = response.css('div.inner-article')

        for product_url in product_urls:
            is_sold_out = product_url.css('div.sold_out_tag').extract_first() is not None
            if is_sold_out is not True:
                yield response.follow(product_url.css('a::attr(href)').extract_first(), self.parse_product)

