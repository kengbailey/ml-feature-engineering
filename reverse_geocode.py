# Kenneth Bailey
# 2018-12-17
# 
# Threaded class for translating lat/long values to zipcode. 
# AKA reverse geocode lookup using the Gmaps API.

import googlemaps
import threading
import os

gmaps_api_key = os.environ['GMAPS_API_KEY']


class FetchZipCodes(threading.Thread):
    """
    Thread fetching zipcodes, given dict of lat/long values
    """

    def __init__(self, zipDict, outDict, tLock):
        threading.Thread.__init__(self)
        self.zipDict = zipDict
        self.gmaps = googlemaps.Client(gmaps_api_key)     
        self.outDict = outDict   
        self.lock = tLock

    def run(self):
        for key, val in self.zipDict.items():
            if val[0] != 0 and val[1] != 0:
                try:
                    result = self.gmaps.reverse_geocode((str(val[0]), str(val[1])))
                except Exception as e:
                    print(e)
                    pass
        
            if result:
                for item in result[0]['address_components']:
                    if 'postal_code' in item['types']:
                        zipcode = str(item['long_name'])
                        break

            with self.lock:
                self.outDict[key] = zipcode

            zipcode = '00000'

if __name__ == "__main__":
    
    inList = {'abc':['40.711303', '-74.016048'], 
                '123':['40.76127', '-73.982738'], 
                'xyz':['35.89250', '-86.31699'], 
                '901':['40.733873', '-73.980658']}
    outDict = {}

    tLock = threading.Lock()
    t = FetchZipCodes(inList, outDict, tLock)
    t.start()
    t.join()

    for k,v in outDict.items():
        print(k,v)
