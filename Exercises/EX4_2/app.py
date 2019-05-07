import requests
import json
from dataclasses import dataclass

SERVER_URL = "https://pwpcourse.eu.pythonanywhere.com"
visited = []

@dataclass
class room:
    handle: str
    content: str

def find_room_href(handle,collection):
    pass

def check_room(s,room_href):
    resp = s.get(SERVER_URL + room_href)
    body = resp.json()

    if body["content"]:
        print(body["content"], " found in ", body["handle"])
        exit()
    else:
        rooms = body["@controls"]

        for room in rooms:
            print("checking room: ", room)
            if room == "maze:south" and body["@controls"]["maze:south"]["href"] not in visited:
                room_href = body["@controls"]["maze:south"]["href"]
                print("Going south ", body["handle"])
                visited.append(room_href)
                check_room(s, room_href)
            if room == "maze:east" and body["@controls"]["maze:east"]["href"] not in visited:
                room_href = body["@controls"]["maze:east"]["href"]
                print("Going east", body["handle"])
                visited.append(room_href)
                check_room(s, room_href)
            if room == "maze:north" and body["@controls"]["maze:north"]["href"] not in visited:
                room_href = body["@controls"]["maze:north"]["href"]
                print("Going north", body["handle"])
                visited.append(room_href)
                check_room(s, room_href)
            if room == "maze:west" and body["@controls"]["maze:west"]["href"] not in visited:
                room_href = body["@controls"]["maze:west"]["href"]
                visited.append(room_href)
                check_room(s, room_href)

with requests.Session() as s:
    s.headers.update({"Accept": "application/vnd.mason+json"})
    resp = s.get(SERVER_URL + "/api/")
    if resp.status_code != 200:
        print("Unable to access API.")
    else:
        body = resp.json()
        room_href = body["@controls"]["maze:entrance"]["href"]
        check_room(s, room_href)
