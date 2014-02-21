# mad_bot scrapper | version 0.1
# DO NOT ABUSE THIS AND SPAM
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from mad_bot.items import CL
from pprint import pprint
import ast
import re

class MAD(Spider):
    name = "maderbot"

    def __init__(self, name=None, *args, **kwargs):

        self.allowed_domains = ['%s' % kwargs.get('url')]
        self.start_urls = ['http://%s.%s/%s/' % (kwargs.get('city'), kwargs.get('url'), kwargs.get('sec'))]
        self.city = kwargs.get('city')
        self.url = kwargs.get('url')
        self.sec = kwargs.get('sec')
    
        #self.rules = (
            #Rule(SgmlLinkExtractor(allow=(r'/%s/index\100\.html' % kwargs.get('sec')))),
        #    Rule(SgmlLinkExtractor(allow=(r'/%s/\d+\.html' % kwargs.get('sec'))), callback='parse_links', follow=True),
            #Rule(SgmlLinkExtractor(allow=(r'/%s/\d+\.html' % kwargs.get('sec'))), callback='parse_page_data', follow=True),
            #Rule(SgmlLinkExtractor(allow=(r'/reply/\d+'))),   
        #)
        super(MAD, self).__init__(name, *args, **kwargs)

    #def parse_start_url(self, response):
    #    list(self.parse_links(response))

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//*[@class="row"]/a/@href').extract()
        for i in links:
            goto = "http://"+self.city+"."+self.url+i.encode('utf-8')
            yield Request(goto, callback = self.parse_page_data)
        #for l in links:
        #comp = re.compile(r'/%s/\d+\.html' % self.sec)
        #print comp.findall(links)
            #link = l.xpath('//*[@class="row"]/a/@href').extract()
            #for i in link:
            #    print i.encode('utf-8')
            #yield Request(link, callback = self.parse_page_data)

    def parse_page_data(self, response):
        sel = Selector(response)
        #replyButton = sel.xpath('//div[@class="reply_options"]')
        page = sel.xpath('//*[@id="pagecontainer"]')
        for i in page:
            #ad = CL()
            #res = response.request.headers.get('Referer')
            #ad['referer'] = res
            #ad['id'] = re.sub(r'\D', "", res) 
            title = i.xpath('//*[@class="postingtitle"]/text()').extract()
            #description = i.xpath('//*[@id="postingbody"]/text()').extract()
            replyUrl = i.xpath('//*[@class="replylink"]/a/@href').extract()
            if len(replyUrl) > 0:
                goto = "http://"+self.city+"."+self.url+replyUrl[0].encode('utf-8')
                yield Request(goto, meta={'title': title}, callback = self.parse_reply_data)
            else:
                print "NO EMAIL"

    def parse_reply_data(self, response):
        hxs = Selector(response)
        posts = hxs.xpath('//div[@class="reply_options"]')
        for post in posts:
            ad = CL()
            res = response.request.headers.get('Referer')
            ad['referer'] = res
            ad['id'] = re.sub(r'\D', "", res)
            ad['title'] = response.meta['title']
            #ad['description'] = response.meta['description']
            if len(post.xpath('//ul/li/a[@class="mailto"]/text()').extract()) > 0:
                ad['email'] = post.xpath('//ul/li/a[@class="mailto"]/text()').extract()[0]
            else:
                ad['email'] = 'no email'  
            yield ad