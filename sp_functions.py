# Spotify API functions - calls to the API to collect track features

# IMPORTS
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np

# Spotify Credentials
import spot_creds

clid = spot_creds.client_id
secret = spot_creds.secret

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=clid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


def extract_track_feat(track_uri):
    this_track = {}
    # URI
    this_track['track_uri'] = track_uri

    track = sp.track(track_uri)

    # Track name
    this_track['track_name'] = track["name"]

    # Main Artist
    artist_uri = track["artists"][0]["uri"]
    this_track['artist_uri'] = artist_uri
    artist_info = sp.artist(artist_uri)

    # Name, popularity, genre
    this_track['artist_name'] = track["artists"][0]["name"]
    this_track['artist_pop'] = artist_info["popularity"]
    this_track['artist_genres'] = artist_info["genres"]

    # Album
    this_track['album'] = track["album"]["name"]

    # Track Metadata
    this_track['track_pop'] = track["popularity"]
    this_track['explicit'] = track['explicit']

    # Audio Features
    this_track = extract_audio_feat(track_uri, this_track)

    this_track_df = pd.json_normalize(this_track)

    return (this_track_df)

def extract_audio_feat(track_uri, track_dict):
    # Audio Features
    audio_feat_list = ['acousticness',
                       'danceability',
                       'energy',
                       'instrumentalness',
                       'key',
                       'liveness',
                       'loudness',
                       'mode',
                       'speechiness',
                       'tempo',
                       'time_signature',
                       'valence']

    audio_feat = sp.audio_features(track_uri)[0]

    audio_feat_list = ['acousticness',
                       'danceability',
                       'energy',
                       'instrumentalness',
                       'key',
                       'liveness',
                       'loudness',
                       'mode',
                       'speechiness',
                       'tempo',
                       'time_signature',
                       'valence']

    for feat in audio_feat_list:
        track_dict[feat] = audio_feat[feat]

    return track_dict


def get_audio_analysis(track_uri):
    audio_anal = sp.audio_analysis(track_uri)

    # delete the long track strings - until I figure out how to use them
    del audio_anal['track']['codestring']
    del audio_anal['track']['echoprintstring']
    del audio_anal['track']['synchstring']
    del audio_anal['track']['rhythmstring']

    return(audio_anal)


track_uri = '1kGQzSasZr4HY5CzjHqCPG'
track_details = extract_track_feat(track_uri)
len(track_details)
