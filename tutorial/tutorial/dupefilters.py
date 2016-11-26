#-*- coding: utf-8 -*-

__author__ = 'liveangel'
__project__ = 'MyScrapy'
import os

from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.request import request_fingerprint

class CustomFilter(RFPDupeFilter):

    def __init__(self, path=None, debug=False):
        super(CustomFilter, self).__init__(path, debug)

        self.twice_fingerprints = set()
        self.twice_file = None
        if path:
            self.twice_file = open(os.path.join(path, 'requests.twice_seen'), 'a+')
            self.twice_file.seek(0)
            self.twice_fingerprints.update(x.rstrip() for x in self.twice_file)

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints and fp in self.twice_fingerprints:
            return True
        if fp not in self.fingerprints:
            self.fingerprints.add(fp)
            if self.file:
                self.file.write(fp + os.linesep)
        else:
            self.twice_fingerprints.add(fp)
            if self.twice_file:
                self.twice_file.write(fp + os.linesep)

        #
        # fp = self.__getid(request.url)
        # if fp in self.fingerprints:
        #     return True
        # self.fingerprints.add(fp)
        # if self.file:
        #     self.file.write(fp + os.linesep)