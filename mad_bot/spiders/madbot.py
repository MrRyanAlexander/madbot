# mad_bot scrapper | version 0.1
# DO NOT ABUSE THIS AND SPAM
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from mad_bot.items import CL
import re

class MySpider(CrawlSpider):
    name = "madbot"

    def __init__(self, name=None, *args, **kwargs):
        

        self.allowed_domains = ['%s' % kwargs.get('url')]
        self.start_urls = ['http://%s.%s/%s/' % (kwargs.get('city'), kwargs.get('url'), kwargs.get('sec'))]
    
        self.rules = (
            Rule(SgmlLinkExtractor(allow=(r'/%s/index\100\.html' % kwargs.get('sec')))),
            Rule(SgmlLinkExtractor(allow=(r'/%s/\d+\.html' % kwargs.get('sec')))),
            Rule(SgmlLinkExtractor(allow=(r'/reply/\d+')), callback='parse_reply_data', follow=True),   
        )
        super(MySpider, self).__init__(name, *args, **kwargs)

    def parse_reply_data(self, response):
        hxs = HtmlXPathSelector(response)
        posts = hxs.xpath('//div[@class="reply_options"]')
        ads = []
        for post in posts:
            ad = CL()
            #find the referering url
            res = response.request.headers.get('Referer')
            ad['referer'] = res
            ad['id'] = re.sub(r'\D', "", res)            
            #find the reply email
            if len(post.xpath('//ul/li/a[@class="mailto"]/text()').extract()) > 0:
                ad['email'] = post.xpath('//ul/li/a[@class="mailto"]/text()').extract()[0]
            else:
                ad['email'] = 'no email'          
            ads.append(ad)
            return ads

             