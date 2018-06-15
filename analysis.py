import json
'''this sort function will be based on the following assumptions:
minimum wage, which as of the time of writing is $14.00/hr in ontario
each person commutes 8 times a week (to school and back 4 times a week), so travelling time opportunity cost is around 14($/hr)*8(travelAmount/week)*TravelTime(hr)*4(weeks/month) =TravelTime*448/month
This means for example a 30 minute commute will cost $224 per month
so in total the
cost per person = (price/number of beds) + ((TravelTime/60)*448)
Note that this cost does not take utilities into account or room furnishings (or people with active social lives :P ).
'''
def _sortBySpecial(data):
    if 'beds' in data and 'price' in data and data['beds'] is not None and 'travelTime' in data:
        return data['price']/data['beds'] + data['travelTime']*448/60
    else:
        return 1000000


'''these are just misc sorting functions that i like to play around with for fun'''

def _sortByKey(data,key):
    if key in data:
        return data[key]
    else:
        return 1000000
def _sortByPricePerBed(data):
    if 'price' in data and 'beds' in data:
        return data['price']/data['bed']
    else:
        return 1000000

#prints list based on special sorting
def analysis():
    with open("results.json",'r') as fp:
        listings = json.load(fp)['results']
    for item in sorted(listings,key=lambda listing: _sortBySpecial(listing)):
        print(item)

if __name__ == "__main__":
    analysis()
