"""
Module with all backend for twitter_map.
"""
import requests
import pprint
import json
from typing import Union, List, Dict
# geopy and folium
from geopy.extra.rate_limiter import RateLimiter
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from geopy import distance
geolocator = Nominatim(user_agent="name")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)


def twitter_friends(nickname: str, access_token: str):
    """
    Function which return twitter information about given user.
    """
    base_url = "https://api.twitter.com/"

    search_headers = {
        'Authorization': f'Bearer {access_token}'
    }

    search_params = {
        'screen_name': f'@{nickname}',
        'count': 12
    }

    search_url = f'{base_url}1.1/friends/list.json'

    response = requests.get(
        search_url, headers=search_headers, params=search_params)

    # RESPONSE STATUS
    # return response.status_code

    json_response = response.json()

    return json_response


def name_location(data: Union[Dict, List]) -> List:
    """
    Function return users`s name and location from json file.
    """
    if "users" not in list(data.keys()):
        return tuple()
    decoded_json = json.dumps(data, indent=4, ensure_ascii=False)
    encoded_json = json.loads(decoded_json)
    users_name_location = []
    for user in encoded_json["users"]:
        temporary_tuple = (user["name"], user["location"])
        users_name_location.append(temporary_tuple)
    return users_name_location


def generate_map(users_location: List) -> List:
    """
    Function generates longitude and latitude depending on users` location.
    """
    markers = []

    for point in users_location:
        try:
            location = geolocator.geocode(point[1])
            film_location = (location.latitude, location.longitude)
            user = (point[0], film_location)
            markers.append(user)
        except AttributeError:
            continue
        except GeocoderUnavailable:
            continue

    return markers


def main(nickname: str, access_token: str) -> List:
    """
    Main function which return list of view (username, location) from given twitter nickname
    and bearer token.
    """
    return generate_map(name_location(twitter_friends(nickname, access_token)))
