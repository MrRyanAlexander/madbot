# mad_bot scrapper | version 0.1
# DO NOT ABUSE THIS AND SPAM
from scrapy.item import Item, Field

class CL(Item):
    referer = Field()
    email = Field()
    id = Field()
