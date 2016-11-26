#-*- coding: utf-8 -*-

__author__ = 'liveangel'
__project__ = 'MyScrapy'

class HouseDeal(object):
    agent = None
    # page info
    page_url = None
    page_title = None


    # location info
    city_name = None
    district_name = None
    section_name = None
    community_name = None
    community_link = None
    address = None

    # House info
    house_no = None
    room_type = None
    area = None
    floor = None
    construction_year = None
    building_orientation = None
    decoration_level = None
    tags=None

    unit_price = None
    list_price = None

    deal_date = None

    def __init__(self, url, agent=u'链家', **kwargs):
        self.agent = agent
        self.page_url = url
        # print kwargs
        # print dict(kwargs)
        for key in kwargs:
            # print kwargs[key]
            setattr(self, key, kwargs[key])


    def __str__(self):
        # return str(vars(self))
        return str(self.__dict__)


if __name__ == '__main__':

    housedeal = HouseDeal("3123", a="f",b="c")
    print str(housedeal)
    print housedeal
    print housedeal.agent
    print u'链家'
