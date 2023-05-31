
#!/Users/anna/miniforge3/envs/spotify/bin/python3
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from secrets import *
import time    
import datetime
import warnings
from aws_helper_methods import SSM


def get_devices(auth_manager):
    access_token = auth_manager.get_access_token()["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url_devices = "https://api.spotify.com/v1/me/player/devices"
    try:
        response = requests.get(url_devices, headers=headers)
        response.raise_for_status()
    except HTTPError as e:
        print(response.status_code)
        print(e)

    response_object = response.json()

    device_data = ssm_client.read_dict_secret("devices_anna")
    # gets the playing device ID for that moment / morning 
    devices = response_object["devices"]
    playing_device_id = ""
    for device in devices:
        if device.get("is_active") is True:
            playing_device_id = device.get("id")
    if playing_device_id == "":
        playing_device_id = default_device # defaults to mac mini if not running

    playing_device_name = device_data.get(playing_device_id)

    return playing_device_id, playing_device_name


def get_uris(auth_manager):
    access_token = auth_manager.get_access_token(check_cache=True)["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    # gets uri for pods to queue up 
    daily_pods_dict = ssm_client.read_dict_secret("daily_pods_anna")

    today = datetime.date.today()
    today = (today.strftime("%Y-%m-%d"))
    daily_uri_list = []
    names = []
    for key, value in daily_pods_dict.items():
        # response = json.dumps(sp_reg.show_episodes(value["uri"], limit = 1), indent =2)
        id = str(value["other"])
        url_shows = "https://api.spotify.com/v1/shows/" + id + "/episodes?limit=1"
        try:
            response = requests.get(url_shows, headers=headers)
            response.raise_for_status()
        except HTTPError as e:
            print(response.status_code)
            print(e)
        response_object = response.json()
        items = response_object.get("items", None)
        if items is None:
            continue
        release_date = ((items[0])["release_date"])
        if release_date == today:
            daily_uri_list.append((response_object["items"][0])["uri"])
            names.append((response_object["items"][0])["name"])

    return daily_uri_list, names



def add_to_daily_queue(device, uris, auth_manager):
    access_token = (auth_manager.get_access_token(check_cache=True)["access_token"])

    headers = {
        "Authorization": "Bearer {token}".format(token=access_token),
    }


    for uri in uris:
        url_queue = "https://api.spotify.com/v1/me/player/queue/?uri="+str(uri)+"&device_id="+str(device)
        requests.post(url_queue, headers=headers)


    # sp_queue.add_to_queue(uri = daily_uri, device_id = playing_device_id)

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    ssm_client = SSM()
    auth_manager = SpotifyOAuth(
        client_id=ssm_client.read_str_secret("client_id_anna"),
        client_secret=ssm_client.read_str_secret("client_secret_anna"),
        redirect_uri=ssm_client.read_str_secret("SPOTIPY_REDIRECT_URI"),
        cache_path=ssm_client.read_str_secret("cache_device_anna"),
        scope=[
            ssm_client.read_str_secret("scope_devices_anna"),
            ssm_client.read_str_secret("scope_add_to_queue_anna"),
            ssm_client.read_str_secret("scope_reg_anna")
        ]
    )
    device_id , device_name = get_devices(auth_manager)
    print("Got device:", device_name)
    uris, names = get_uris(auth_manager)
    print("Got uris", uris)
    print("Got the following", names)
    add_to_daily_queue(device_id, uris, auth_manager)
    print("Sucessfully added to queue on", device_name)
