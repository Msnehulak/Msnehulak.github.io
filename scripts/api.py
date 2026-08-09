if __name__ == '__main__':
    import sweb
else:
    from . import sweb

import logging
import os
import sys
from datetime import timedelta
from pathlib import Path

from diskcache import Cache
from dotenv import load_dotenv
from googleapiclient.discovery import build
from ossapi import Ossapi

load_dotenv()

_NO_EXPIRE = '_no_expire'
BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache" / "diskcache"
YT_CHANNEL_ID = 'UC-SySQOnf_6WygeSQuLnCrQ'

ENV_VAL = {
    "osu_client_id": os.getenv("OSU_CLIENT_ID"),
    "osu_client_secret": os.getenv("OSU_CLIENT_SECRET"),
    "youtube_api_key": os.getenv("YOUTUBE_API_KEY"),
}

for name, key in ENV_VAL.items():
    if key is None:
        logging.error(f'missing env: {name}')
        sys.exit(1)

class APIs:
    def __init__(self) -> None:
        self.cache = Cache(str(CACHE_DIR))
        self.apis = {
            'yt': {
                'update': self.update_yt,
                'refresh': 1 * 60 * 60,
                'data': None
            },
            'osu': {
                'update': self.update_osu,
                'refresh': 1 * 60 * 60,
                'data': None
            }
        }
        self.update_data()

    def update_data(self):
        for name, content in self.apis.items():
            cached_data = self.cache.get(name)

            if cached_data is None:
                logging.debug(f"Cache pro '{name}' neexistuje nebo vypršela. Spouštím update...")
                
                try:
                    new_data = content['update']()
                    if not new_data:
                        raise ValueError(f"Funkce update pro {name} vrátila prázdná data.")
                except Exception as e:
                    logging.warning(f"Chyba při aktualizaci {name}: {e}. Zkouším načíst stará data...")
                    new_data = self.cache.get(f'{name}{_NO_EXPIRE}') 
                    
                    if new_data is None:
                        logging.error(f"Chybí stará data i v záložní cache pro {name}")
                        sys.exit(1)
                   
                self._update_cache(name, new_data)
            else:
                logging.info(f'for {name} is used cache')
                content['data'] = cached_data

    def get_data(self, api):
        if api in self.apis:
            return self.apis[api]['data']
        else:
            logging.error(f"API data '{api}' doesn't exist")
            sys.exit(1)

    def _update_cache(self, api, data):
        if data and api in self.apis:
            expire_seconds = self.apis[api]['refresh']
            self.cache.set(api, data, expire=expire_seconds)
            self.cache.set(f'{api}{_NO_EXPIRE}', data, expire=None)
            self.apis[api]['data'] = data
            logging.info(f"Update cache for '{api}' and '{api}{_NO_EXPIRE}'")

    def update_yt(self):
        youtube = build('youtube', 'v3', developerKey=ENV_VAL['youtube_api_key'])
        
        channel_request = youtube.channels().list(
            part='contentDetails,snippet',
            id=YT_CHANNEL_ID
        )
        channel_response = channel_request.execute()

        if not channel_response.get('items'):
            raise RuntimeError("Kanál s tímto ID nebyl nalezen.")

        channel_title = channel_response['items'][0]['snippet']['title']
        channel_tag = channel_response['items'][0]['snippet']['customUrl']
        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        playlist_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=1 
        )
        playlist_response = playlist_request.execute()

        if not playlist_response.get('items'):
            raise RuntimeError("V playlistu nahraných videí nebyla nalezena žádná videa.")

        latest_video = playlist_response['items'][0]
        video_title = latest_video['snippet']['title']
        video_id = latest_video['snippet']['resourceId']['videoId']
        published_at = latest_video['snippet']['publishedAt']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_url_embed = f"https://www.youtube-nocookie.com/embed/{video_id}"

        return {
            'profile': {
                'title': channel_title,
                'tag': channel_tag,
            },
            'newest_vid': {
                'title': video_title,
                'id': video_id,
                'released_date': published_at,
                'url': video_url,
                'embed': video_url_embed
            }
        }

    def update_osu(self):
        client_id = ENV_VAL['osu_client_id']
        client_secret = ENV_VAL['osu_client_secret']
        username = "SnehulakTV_"

        if not client_id or not client_secret:
            raise ValueError("Chybí OSU_CLIENT_ID nebo OSU_CLIENT_SECRET v .env.")

        api = Ossapi(int(client_id), client_secret)
        user = api.user(username)
        stats = user.statistics

        return {
            "rank": stats.global_rank,
            "pp": stats.pp,
            "acc": stats.hit_accuracy,
            "play_time_s": stats.play_time,
            "play_time": str(timedelta(seconds=stats.play_time)),
            "play_count": stats.play_count,
            "avatar": user.avatar_url,
        }
