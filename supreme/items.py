# -*- coding: utf-8 -*-

from scrapy import Item, Field


def serialize_price(value):
    return int(value[1:])


def serialize_picture_url(value):
    return 'https:' + value


class ProductItem(Item):
    id = Field()
    name = Field()
    description = Field()
    model = Field()
    type = Field()
    price = Field(serializer=serialize_price)
    collection_id = Field()
    picture_url = Field(serializer=serialize_picture_url)
    is_new = Field()
    url = Field()
