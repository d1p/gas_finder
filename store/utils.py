import re

import googlemaps

english_check = re.compile(r'[A-Za-z]')


def lat_lng_to_city(lat: float, lng: float, key=0):
    gmaps = googlemaps.Client(key="AIzaSyBRjp7TedIq1JMJcEZbKByBHF6PCJGMRGw")
    r_geocode = gmaps.reverse_geocode({"lat": lat, "lng": lng})
    for component in r_geocode[key]["address_components"]:
        try:
            if (
                    component["types"][1] == "locality"
                    or component["types"][0] == "locality"
            ):
                city = component["short_name"]
                if english_check.match(city):
                    return city
                else:
                    return lat_lng_to_city(lat, lng, key + 1)
        except IndexError:
            pass
