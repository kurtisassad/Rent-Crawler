def _sortByKey(data,key):
    if key in data:
        return data[key]
    else:
        return 1000000
listings = json.load(open(fileName))
print(sorted(listings,key=lambda listing: _sortByKeySpecial(listing,'travelTime')))
