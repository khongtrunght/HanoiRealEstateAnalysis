import googlemaps
from datetime import datetime
import json

gmaps = googlemaps.Client(key='AIzaSyA2ELpgpi-X9033DRRV5VaYNJtsxzKInBw')

# Geocoding an address
geocode_result = gmaps.geocode(
    " Phường Trung Liệt, Quận Đống Đa, Hà Nội")


with open('address.json', 'w', encoding='utf-8') as file:
    json.dump(geocode_result[0], file, ensure_ascii=False)

# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)

print(geocode_result[0]['geometry']['location'])
