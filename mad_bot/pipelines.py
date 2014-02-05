# mad_bot scrapper | version 0.1
# DO NOT ABUSE THIS AND SPAM
import json,httplib
from pprint import pprint
from scrapy import signals
#scrapy docs say use LinesExporter, but I want a JSON array
#from scrapy.contrib.exporter import JsonLinesItemExporter
from scrapy.contrib.exporter import JsonItemExporter
from scrapy.exceptions import DropItem
from mad_bot.settings import AppID
from mad_bot.settings import ApiKey

class CLPipe(object):
    """A pipeline for writing results to json"""
    def __init__(self):
        self.files = {}

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
        #for i in range(len(data)):
            #this is actually very bad to loop here
            #in one day I sent almost 500k requests.. thats bad
            #try sending one load and process on the other end. 


            #not sure if this is efficient, but it works
            #makes new api call for each loop
            #pushes single object for each call
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/functions/scrapeSaver', json.dumps({
            #"email":data[i]["email"], "referer":data[i]["referer"], "scrapeID":data[i]["id"]
            "data":data
        }), {
            "X-Parse-Application-Id": AppID,
            "X-Parse-REST-API-Key": ApiKey,
            "Content-Type": "application/json"
        })
        result = json.loads(connection.getresponse().read())
        print "Sending load ", result
        #done with the new file, close it
        new.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class Duplicates(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item
#writing Python is fun
class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    # can use any words here to check ads 
    words_to_filter = ['politics', 'religion']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            #need to fix scraper for this to work, but will work once fixed :)
            if word in unicode(item['description']).lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item