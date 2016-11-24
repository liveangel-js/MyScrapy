#-*- coding: utf-8 -*-

__author__ = 'liveangel'
__project__ = 'MyScrapy'


import scrapy

class DoubanSpider(scrapy.Spider):
    name = "douban_group"

    def start_requests(self):
        urls = [
            'https://www.douban.com/group/531651/',
            # 'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        for topic in response.css('div table.olt tr'):
            yield {
                'topic_title': topic.css('td.title a::text').extract_first(),
                'topic_url': topic.css('td.title a::attr(href)').extract_first(),
                'author': topic.css('td')[1].css('a::text').extract_first(),
                'author_url': topic.css('td')[1].css('a::attr(href)').extract_first(),
                'response_count': topic.css('td')[2].css("::text").extract_first() if topic.css('td')[2].css("::text").extract_first()!='' else 0,
                'last_response_time': topic.css('td')[3].css("::text").extract_first(),
            }