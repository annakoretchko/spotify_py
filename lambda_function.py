from __future__ import print_function
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import time    
import datetime
import warnings
import json
import boto3
import os
# headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}

ssm = boto3.client('ssm', 'us-east-2')

def lambda_handler(event, context):
    value = get_parameters()
    print("value1 = " + value)
    return value  # Echo back the first key value
    
def get_parameters():
    response = ssm.get_parameters(
        Names=['client_id_anna'],
        WithDecryption=True
    )
    for parameter in response['Parameters']:
        return parameter['Value']
        
