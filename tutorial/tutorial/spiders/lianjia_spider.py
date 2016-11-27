#-*- coding: utf-8 -*-

__author__ = 'liveangel'
__project__ = 'MyScrapy'
import scrapy
# from HouseDeal import HouseDeal

import simplejson as json
import re
from tutorial.items import HouseDeal

class HouseSpider(scrapy.Spider):
    name = "house"
    # cookies = {'select_city':'310000', 'cityCode':'sh', 'lianjia_uuid':'b31eff11-2b79-438f-8384-e8d1a23b93f6'}
    cookies = {'select_city':'310000', 'cityCode':'sh', 'lianjia_uuid':'b31eff11-2b79-438f-8384-e8d1a23b93f5'}

    def process_request(self, request, spider):
        print "*" *80 +"process_request"

    def start_requests(self):
        urls = ['http://sh.lianjia.com/chengjiao/sh1813297.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # yield scrapy.Request(url=url, meta={'dont_redirect': True,"handle_httpstatus_list": [302]}, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        print response
        filename = '%s' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        # house_deal = HouseDeal()
        title = response.css("h1::text").extract_first()
        tags = response.css("div.view-label span span")
        tag_list = []
        for tag in tags:
            tag_list.append(tag.css("::text").extract_first())
        album = response.css("div.album-box")
        content = response.css("div.content")

        deal_date = response.css("div.soldInfo div.cell.first p::text").extract_first().strip()
        list_price = response.css("div.soldInfo div.cell")[1].css(" p::text").extract_first().strip()

        around_info = response.css("table.aroundInfo")
        unit_price = around_info[0].css("tr td")[0].css("::text").extract()[2].strip()
        floor = around_info[0].css("tr td")[1].css("::text").extract()[2].strip()
        construction_year = around_info[0].css("tr td")[2].css("::text").extract()[2].strip()
        decoration_level = around_info[0].css("tr td")[3].css("::text").extract()[2].strip()
        building_orientation = around_info[0].css("tr td")[4].css("::text").extract()[2].strip()
        community_name = around_info[0].css("tr td")[5].css("a::text").extract_first().strip()

        community_link = around_info[0].css("tr td")[5].css("a::attr(href)").extract_first().strip()
        community_link = response.urljoin(community_link)
        address = around_info[0].css("tr td")[6].css("p::text").extract_first().strip()
        house_no = around_info[0].css("tr td")[7].css("::text").extract()[2].strip()
        room_type = title.split(u" ")[1]
        area = title.split(u" ")[2]

        breadcrumbs = response.css("div .fl.l-txt a")
        city_name = breadcrumbs[1].css("::text").extract_first()[:-7]
        district_name = breadcrumbs[1].css("::text").extract_first()[:-7]
        section_name = breadcrumbs[1].css("::text").extract_first()[:-7]
        house_deal = HouseDeal(url=response.url, community_name=community_name,
                              community_link=community_link, address=address, house_no=house_no,
                               deal_date=deal_date, list_price=list_price, unit_price=unit_price,
                               floor=floor, construction_year=construction_year,decoration_level=decoration_level,
                               building_orientation=building_orientation,tags=tag_list,
                               room_type=room_type, area=area,city_name=city_name,
                               district_name=district_name,section_name=section_name)
        # print house_deal
        yield house_deal
        yield scrapy.Request("http://sh.lianjia.com/chengjiao/sh4220677.html", callback=self.parse)



