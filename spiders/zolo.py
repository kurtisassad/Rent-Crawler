import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from items import Listing, ListingLoader
import re
class ZoloSpider(scrapy.Spider):
    name = "zolo"
    start_urls = [
        'https://www.zolo.ca/toronto-real-estate/houses-for-rent',
    ]
    i = 0
    def __init__(self,stop_after,list,days_old_less_than):
        self.stop_after = stop_after
        self.list = list
        self.days_old_less_than = days_old_less_than

    def parse(self, response):
        if(self.i < self.stop_after):
            #we dont want to rescrape listings
            street_names = response.xpath('//span[contains(@class,"street")]/text()').extract()
            #we want to force stop once we start scraping old listings
            listing_times = response.xpath('//span[contains(@class,"xs-mr1")]/text()').extract()
            #this response just gives us all the listings urls on the page
            listings = response.xpath('//div[contains(@class,"card-listing--image")]/a/@href')
            for street_name,listing,listing_time in zip(street_names,listings,listing_times):
                #we dont want any old listings so we stop scraping altogether if the are more than a week old
                if 'day' in listing_time and float(re.search('\d+',listing_time).group()) > self.days_old_less_than:
                    self.i+=1
                elif not (street_name.strip() in self.list):
                    self.i +=1
                    yield response.follow(listing,callback=self.parseListing)
            nextPage = response.xpath('//i[contains(@class,"icon-keyboard-arrow-right")]/../@href').extract_first()
            if nextPage is not None:
                yield response.follow(nextPage, callback=self.parse)

    def parseListing(self,response):
         l = ListingLoader(item=Listing(),response=response)
         l.add_xpath("price",'//div[contains(@class,"listing-price-value")]/span/text()')
         l.add_xpath("beds",'//div[contains(@class,"listing-values-bedrooms")]//div[contains(@class,"listing-values-item")]/span/text()')
         l.add_xpath("location",'//h1[contains(@class,"address")]/text()')
         availableSince = response.xpath('//dd[contains(@class,"last-updated")]/text()')[-1].extract()
         l.add_value("availableSince",availableSince)
         l.add_xpath("type",'//dt[text()="Type"]/../dd/span/text()')
         l.add_value("url",response.url)
         l.add_xpath("leaseTerm",'//dt[text()="Lease Term"]/../dd/span/text()')
         # img = response.xpath('//img[contains(@class,"listing-slider-content-photo")]/@src')[0].extract()
         # l.add_value("imageUrl",img)
         return l.load_item()
