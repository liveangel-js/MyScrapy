# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Base(scrapy.Item):
    last_updated = scrapy.Field()
    spider = scrapy.Field()
    url = scrapy.Field()
    crawled_time = scrapy.Field()

class HouseDeal(Base):
    agent = scrapy.Field()
    # location
    city_name = scrapy.Field()
    district_name = scrapy.Field()
    section_name = scrapy.Field()
    community_name = scrapy.Field()
    community_link = scrapy.Field()
    address = scrapy.Field()

    # House info
    house_no = scrapy.Field()
    room_type = scrapy.Field()
    area = scrapy.Field()
    floor = scrapy.Field()
    construction_year = scrapy.Field()
    building_orientation = scrapy.Field()
    decoration_level = scrapy.Field()
    tags = scrapy.Field()

    unit_price = scrapy.Field()
    list_price = scrapy.Field()

    deal_date = scrapy.Field()

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)


if __name__ == '__main__':

    product = Product(name='Desktop PC', price=1000)
    product.get('name')