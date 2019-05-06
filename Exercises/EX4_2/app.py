from flask import json
from dataclasses import dataclass

SERVER_URL = "https://pwpcourse.eu.pythonanywhere.com"

@dataclass
class room:
    handle: str
    content: str

with requests.Session() as s:
    s.headers.update({"Accept": "application/vnd.mason+json"})
    resp = s.get(SERVER_URL + "/api/")
    if resp.status_code != 200:
        print("Unable to access API.")
    else:
        body = resp.json()
        room_href = body["@controls"]["maze:entrance"]["href"]

def check_room(s,handle,room_href):
    pass

def find_room_href(handle,collection):
    pass


"""
def check_artist(s, name, artists_href):
    resp = s.get(API_URL + artists_href)
    body = resp.json()
    artist_href = find_artist_href(name, body["items"])
    if artist_href is None:
        artist_href = create_artist(s, name, body["@controls"]["mumeta:add-artist"])

    resp = s.get(API_URL + artist_href)
    body = resp.json()
    albums_href = body["@controls"]["mumeta:albums-by"]["href"]

def find_artist_href(name, collection):
    name = name.lower()
    hits = []
    for item in collection:
        if item["name"].lower() == name:
            hits.append(item)
    if len(hits) == 1:
        return hits[0]["@controls"]["self"]["href"]
    elif len(hits) >= 2:
        return prompt_artist_choice(hits)
    else:
        return None
"""
