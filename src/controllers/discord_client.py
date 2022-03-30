import re
import discord
from pprint import pprint
from controllers.spotify_controller import SpotifyController

class DiscordClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.spotify_controller = SpotifyController()
    
    async def on_message(self, message):
        track_uri = self.try_get_track_uri(message)
        if track_uri:
            await self.add_track_to_playlist(track_uri, message)
        elif '!playlist' in message.content:
            playlist_url = self.spotify_controller.get_playlist_external_url()
            await message.channel.send('Playlist: {}'.format(playlist_url))

    def try_get_track_uri(self, message):
        regex_match = re.search(r'(https?://open.spotify.com/track\S+)', message.content)
        if regex_match:
            return regex_match.group().split('/')[-1].split('?')[0]
        else:
            return None

    async def add_track_to_playlist(self, track_uri, message):
        add_result = self.spotify_controller.add_track_to_playlist(track_uri)
        if add_result:
            track_data = self.spotify_controller.get_track_data(track_uri)
            await message.channel.send('Added: {}'.format(track_data))
        else:
            await message.channel.send('Nice try. That is a duplicate.')