import scrapy
from spiders.zolo import ZoloSpider
from spiders.kijiji import KijijiSpider
from scrapy.crawler import CrawlerProcess
from jsonlToJson import transfer
from gmaps import distance
import json
import sys
import os

'''This function parses the jsonl file and returns a list of all extracted
houses listings that have been scraped. This is so we dont rescrape those listings.'''
def _makeVisitedHousesList(file_name):
    retList = []
    with open(file_name,'r') as fp:
        results = json.load(fp)['results']
        for entry in results:
            retList.append(entry['location'])
    return retList

def _returnJsonlList(file_name):
    retList = []
    with open(file_name) as fp:
        for entry in fp.readlines():
            retList.append(json.loads(entry))
    return retList

'''the meat of the program'''
def main(destination,type,stop_after,maps_key,max_days_listed):
    if maps_key == '':
        sys.exit('you need a google developer key to run this program')
    results = []
    fileName = 'results.json'
    intermediateFile = 'results.jsonl'
    if fileName not in os.listdir():
        writeTo = {'results':[]}
        with open(fileName,'w') as fp:
            json.dump(writeTo,fp)
    #handles crawler
    visited_houses = _makeVisitedHousesList(fileName)
    # print(visited_houses)
    # return 0
    spiderList = [ZoloSpider]
    open(intermediateFile, 'w').close()#empties file because scrapy appends
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': intermediateFile,
        'LOG_ENABLED' : True,
    })
    for i in range(len(spiderList)):
        process.crawl(spiderList[i],stop_after = stop_after//len(spiderList),list=visited_houses,days_old_less_than=max_days_listed)
    process.start()# the script will block here until the crawling is finished

    listings = _returnJsonlList(intermediateFile)

    #google maps stuff, updates travel time and distance for each listing to destination
    locations = []
    for i in range(len(listings)):
        locations.append(listings[i]['location'])
    # print('\n\n\n\n\n\n',locations,'\n\n\n\n\n\n\n')
    info = distance(locations,destination,type,maps_key)
    for i in range(len(info)):
        listings[i]['travelTime'] = info[i]['duration']
        listings[i]['distance'] = info[i]['distance']
    open("results.jsonl",'w').close()
    with open("results.jsonl",'r+') as fp:
        for listing in listings:
            # print(listing)
            json.dump(listing,fp)
            fp.write('\n')
    #transfers from jsonl to json
    transfer(intermediateFile,fileName)


if __name__ == "__main__":
    type = 'transit'
    destination = ["College St at St George St"]
    num_of_pages = 200
    max_days_listed = 14
    with open('api_key.txt','r') as f:
        main(destination,type,50 ,f.read().strip(),max_days_listed)
