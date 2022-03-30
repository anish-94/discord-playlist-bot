import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
playlist_modify_auth_manager = SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope="playlist-modify-private",
    # scope="playlist-modify-public"
)

BOT_PLAYLIST_ID = '0grsGacOeqZBdtJQU0KXJD'

class SpotifyController:
    def __init__(self, auth_manager=playlist_modify_auth_manager):
        self.auth_manager = auth_manager
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
        self.sp.trace = False

    def get_track_data(self, track_uri):
        track_data = self.sp.track(track_uri)
        return '{} - {}'.format(track_data['name'], ', '.join([ x['name'] for x in track_data['artists'] ]))

    def get_playlist_external_url(self, playlist_id=BOT_PLAYLIST_ID):
        return self.sp.playlist(playlist_id)['external_urls']['spotify']

    def get_tracks_from_playlist(self, id=BOT_PLAYLIST_ID, offset=0, limit=None):
        return self.sp.playlist_items(
            playlist_id=id,
            offset=offset,
            limit=limit
        )

    def add_track_to_playlist(self, track_uri, playlist_id=BOT_PLAYLIST_ID):
        playlist_tracks = self.get_tracks_from_playlist(playlist_id)
        track_uris = [ x['track']['uri'] for x in playlist_tracks['items'] ]
        if f'spotify:track:{track_uri}' not in track_uris:
            self.sp.playlist_add_items(
                playlist_id,
                [track_uri]
            )
            return True
        else:
            return False
