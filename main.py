
#!/Users/anna/miniforge3/envs/spotify/bin/python3
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from secrets import *
import time    
import datetime
import warnings


def get_devices():
    auth_manager=SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        cache_path = cache_path_device,
                        scope=scope_devices)
    access_token = (auth_manager.get_access_token()['access_token'])
    # with open(cp1) as temp_tokens:
    #     data = json.load(temp_tokens)
    #     access_token = data['access_token']
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    url_devices = 'https://api.spotify.com/v1/me/player/devices'
    r = requests.get(url_devices, headers=headers)
    d = r.json()

    with open('devices.json') as json_file:
        data = json.load(json_file)
    # gets the playing device ID for that moment / morning 
    devices = d['devices']
    playing_device_id = ""
    for device in devices:
        if device.get('is_active') is True:
            playing_device_id = device.get('id')
    if playing_device_id == "":
        playing_device_id = default_device # defaults to mac mini if not running

    playing_device_name = data.get(playing_device_id)

    return playing_device_id, playing_device_name


def get_uris():
    auth_manager=SpotifyOAuth(client_id=client_id,
                                client_secret=client_secret,
                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                cache_path = cache_path_uri,
                                scope=scope_reg)

    access_token = (auth_manager.get_access_token(check_cache=True)['access_token'])
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token),
    }


    # gets uri for pods to queue up 
    with open('daily_pods.json') as json_file:
        data = json.load(json_file)

    today = datetime.date.today()
    today = (today.strftime("%Y-%m-%d"))
    daily_uri_list = []
    names = []
    for key, value in data.items():
        # response = json.dumps(sp_reg.show_episodes(value['uri'], limit = 1), indent =2)
        id = str(value['other'])
        url_shows = 'https://api.spotify.com/v1/shows/' + id + '/episodes?limit=1'
        r = requests.get(url_shows, headers=headers)
        d = r.json()
        res = json.loads(json.dumps(d))
        items = res.get("items", None)
        if items is None:
            continue
        release_date = ((items[0])['release_date'])
        if release_date == today:
            daily_uri_list.append((res['items'][0])['uri'])
            names.append((res['items'][0])['name'])

    return daily_uri_list, names



def add_to_daily_queue(device, uris):

    auth_manager=SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        cache_path = cache_path_queue,
                        scope=scope_add_to_queue)
    access_token = (auth_manager.get_access_token(check_cache=True)['access_token'])

    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token),
    }


    for uri in uris:
        url_queue = 'https://api.spotify.com/v1/me/player/queue/?uri='+str(uri)+"&device_id="+str(device)
        requests.post(url_queue, headers=headers)


    # sp_queue.add_to_queue(uri = daily_uri, device_id = playing_device_id)

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    device_id , device_name = get_devices()
    print("Got device:", device_name)
    uris, names = get_uris()
    print("Got uris", uris)
    print("Got the following", names)
    add_to_daily_queue(device_id, uris)
    print("Sucessfully added to queue on", device_name)
