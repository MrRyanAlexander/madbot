# mad_bot scrapper | version 0.1
# DO NOT ABUSE THIS AND SPAM
import re
import json,httplib
import string
from scrapy import signals
from scrapy import log
#scrapy docs say use LinesExporter, but I want a JSON array
#from scrapy.contrib.exporter import JsonLinesItemExporter
from scrapy.contrib.exporter import JsonItemExporter
from scrapy.exceptions import DropItem

class CLPipe(object):
    """A pipeline for writing results to json"""
    def __init__(self, **kwargs):
        self.files = {}
        self.AppID = kwargs.get('AppID')
        self.ApiKey = kwargs.get('ApiKey')
        super(CLPipe, self).__init__(**kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        #open a static/dynamic file to read and write to
        file = open('%s_items.json' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        #reopen new static/dynamic file to parse for sending
        new = open('%s_items.json' % spider.name)
        data = json.load(new)
        #reg = re.compile(r'[\n\r\t]')
        #for i in data:
        #    log.msg( i )
            #this is actually very bad to loop here
            #in one day I sent almost 500k requests.. thats bad
            #try sending one load and process on the other end. 


            #not sure if this is efficient, but it works
            #makes new api call for each loop
            #pushes single object for each call
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/functions/scrapeSaver', json.dumps({
        #    #"email":data[i]["email"], "referer":data[i]["referer"], "scrapeID":data[i]["id"]
            "data":data
        }), {
            "X-Parse-Application-Id": self.AppID,
            "X-Parse-REST-API-Key": self.ApiKey,
            "Content-Type": "application/json"
        })
        result = json.loads(connection.getresponse().read())
        print "Sending load ", result
        #done with the new file, close it
        new.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

#drop items without email adress


class Duplicates(object):

    def __init__(self):
        self.emails_seen = set()

    def process_item(self, item, spider):
        if item['email'] in self.emails_seen:
            raise DropItem("\n\n\n\n\n\n\n\n\n\n\n\nDuplicate email found: %s \n\n\n\n\n\n\n\n\n\n\n\n" % item)
        else:
            self.emails_seen.add(item['email'])
            return item

class DropAds(object):
    """A pipeline to restrict results to specific details"""

    # put all words in lowercase
    # can use any words here to check ads 
    words_to_filter = ['craigslist is hiring']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            #need to fix scraper for this to work, but will work once fixed :)
            if word in unicode(item['title']).lower():
                raise DropItem("Invalid Ad")
                #log.msg("\n\n\n\n\n\n\n\n\n\n\n\nFound the word '%s' in the description!!!!\n\n\n\n\n\n\n\n\n\n\n\n" % word)
                #return item
            else:
                return item