# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AccuracyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    provider = scrapy.Field()
    hi = scrapy.Field()
    low = scrapy.Field()
    icon = scrapy.Field()
    text = scrapy.Field()
    overall = scrapy.Field()
    sort_zip = scrapy.Field()
    sort_city  = scrapy.Field()
    sort_state = scrapy.Field()

    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({'sort_zip': self['sort_zip']
                      , 'sort_city': self['sort_city']
                      , 'sort_state': self['sort_state']
                    }
                )
