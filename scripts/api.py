import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from ossapi import Ossapi
from diskcache import Cache
from googleapiclient.discovery import build
from datetime import timedelta

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache" / "diskcache"
YT_CHANEL_ID = 'UC-SySQOnf_6WygeSQuLnCrQ'

ENV_VAL = {
    "osu_client_id": os.getenv("OSU_CLIENT_ID"),
    "osu_client_secret": os.getenv("OSU_CLIENT_SECRET"),
    "github_token": os.getenv("GIT_HUB_TOKEN"),
    "youtube_api_key": os.getenv("YOUTUBE_API_KEY"),
}

for i, x in ENV_VAL.items():
    if x is None:
        print(f'missing {i}')
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
        for api in self.apis.keys():
            cached_data = self.cache.get(api)

            if cached_data is None:
                print(f"Cache pro '{api}' neexistuje nebo vypršela. Spouštím update...")
                self.apis[api]['update']()
            else:
                self.apis[api]['data'] = cached_data

    def get_data(self, api):
        if api in self.apis:
            return self.apis[api]['data']
        else:
            print(f"API data '{api}' dont exist")

    def _update_cache(self, api, data):
        if data and api in self.apis:
            expire_seconds = self.apis[api]['refresh']
            self.cache.set(api, data, expire=expire_seconds)
            self.apis[api]['data'] = data
            print(f"Update cache for '{api}'")

    def update_yt(self):
        youtube = build('youtube', 'v3', developerKey=ENV_VAL['youtube_api_key'])
        try:
            channel_request = youtube.channels().list(
                part='contentDetails,snippet',
                id=YT_CHANEL_ID
            )
            channel_response = channel_request.execute()

            if not channel_response.get('items'):
                print("Kanál s tímto ID nebyl nalezen.")
                return

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
                print("V playlistu nahraných videí nebyla nalezena žádná videa. Přeskakuji uložení.")
                return

            latest_video = playlist_response['items'][0]
            video_title = latest_video['snippet']['title']
            video_id = latest_video['snippet']['resourceId']['videoId']
            published_at = latest_video['snippet']['publishedAt']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_url_embed = f"https://www.youtube-nocookie.com/embed/{video_id}"

            new_data = {
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
            self._update_cache('yt', new_data)
        except Exception as e:
            print(f"Došlo k chybě: {e}")

    def update_osu(self):
        client_id = ENV_VAL['osu_client_id']
        client_secret = ENV_VAL['osu_client_secret']
        username = "SnehulakTV_"

        if not client_id or not client_secret:
            print("Chyba: Chybí OSU_client_id nebo OSU_CLIENT_SECRET v .env. Přeskakuji.")
            return

        try:
            api = Ossapi(int(client_id), client_secret)
            user = api.user(username)
            stats = user.statistics

            new_data = {
                "rank": stats.global_rank,
                "pp": stats.pp,
                "acc": stats.hit_accuracy,
                "play_time_s": stats.play_time,
                "play_time": str(timedelta(seconds=stats.play_time)),
                "play_count": stats.play_count,
                "avatar": user.avatar_url
            } 
            
            self._update_cache('osu', new_data)
            
        except Exception as e:
            print(f"Chyba při komunikaci s osu! API: {e}")
