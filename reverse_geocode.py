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
    Thread fetching zipcodes, given dict of lat/long values.
    Returns a dict of zipcode values.
    """

    def __init__(self, in_dict, out_dict, tLock):
        threading.Thread.__init__(self)
        self.in_dict = in_dict
        self.gmaps = googlemaps.Client(gmaps_api_key)     
        self.out_dict = out_dict   
        self.lock = tLock

    def run(self):
        for key, val in self.in_dict.items():
            result = None
            zipcode = '00000'
            if val[0] != 0 and val[1] != 0:
                try:
                    result = self.gmaps.reverse_geocode((str(val[0]), str(val[1])))
                except Exception as e:
                    print(e)
                    pass
        
            if result != None:
                for item in result[0]['address_components']:
                    if 'postal_code' in item['types']:
                        zipcode = str(item['long_name'])
                        break

                with self.lock:
                    self.out_dict[key] = zipcode

if __name__ == "__main__":
    
    in_dict = {'abc':['40.711303', '-74.016048'], 
                '123':['40.76127', '-73.982738'], 
                'xyz':['35.89250', '-86.31699'], 
                '901':['40.733873', '-73.980658']}
    out_dict = {}

    tLock = threading.Lock()
    t = FetchZipCodes(in_dict, out_dict, tLock)
    t.start()
    t.join()

    for k,v in out_dict.items():
        print(k,v)
