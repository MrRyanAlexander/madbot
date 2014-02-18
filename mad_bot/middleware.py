# mad_bot scrapper | version 0.1
# DO NOT ABUSE THIS AND SPAM
import re
import random
import base64
from scrapy import log
from scrapy.exceptions import IgnoreRequest


class RandomProxy(object):
    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        f = open(self.proxy_list)

        self.proxies = []
        for l in f.readlines():
            ##below will enable AUTH, refer to github.com/aivarsk/scrapy-proxies
            #parts = re.match('(\w+://)(\w+:)?(.+)', l)
            # Cut trailing @
            #if parts[1]:
            #    parts[1] = parts[1][:-1]

            self.proxies.append("http://"+l.strip())
        f.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        proxy_address = random.choice(self.proxies)
        log.msg('Trying ip :%s' % proxy_address)
        #proxy_user_pass = self.proxies[proxy_address]

        request.meta['proxy'] = proxy_address
        #if proxy_user_pass:
        #    request.headers['Proxy-Authorization'] = 'Basic ' + base64.encodestring(proxy_user_pass)

    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        log.msg('Dropping ip: <%s>. There are %d ips left' % (proxy, len(self.proxies)))
        try: self.proxies.remove(proxy)
        except ValueError: pass

class RandomUserAgent(object):
    """Randomly rotate user agents"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class ErrorMonkeyMiddleware(object):

    def process_request(self, request, spider):
        if 'x-ignore-request' in request.url:
            raise IgnoreRequest()
        elif 'x-error-request' in request.url:
            _ = 1 / 0

    def process_response(self, request, response, spider):
        if 'x-ignore-response' in request.url:
            raise IgnoreRequest()
        elif 'x-error-response' in request.url:
            _ = 1 / 0
        else:
            return response

