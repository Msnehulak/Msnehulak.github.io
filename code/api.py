import os
from pathlib import Path
from dotenv import load_dotenv
from ossapi import Ossapi
from diskcache import Cache
from googleapiclient.discovery import build

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

class Osu:
    def __init__(self) -> None:
        self.data = None 
        self.cache = Cache(str(CACHE_DIR))
        self.update_frequency_hours = 1

    def load_data(self):
        cached_data = self.cache.get("osu") 
        
        if cached_data is None:
            print("Cache pro 'osu' neexistuje nebo vypršela. Spouštím update...")
            self._update()
            cached_data = self.cache.get("osu")

        if cached_data:
            self.data = cached_data
        else:
            print("Chyba: Nepodařilo se získat data z API ani z cache.")

    def _update(self):
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

            novy_api_vystup = {
                "rank": stats.global_rank,
                "pp": stats.pp,
                "acc": stats.hit_accuracy,
                "play_time": stats.play_time,
                "play_count": stats.play_count,
                "avatar": user.avatar_url
            } 
            
            # Zápis do cache s nastavenou expirací (převod hodin na sekundy)
            expire_seconds = self.update_frequency_hours * 3600
            self.cache.set("osu", novy_api_vystup, expire=expire_seconds)
            
            print("osu! cache byla úspěšně aktualizována pomocí diskcache.")
            
        except Exception as e:
            print(f"Chyba při komunikaci s osu! API: {e}")

    def get_data(self):
        self.load_data()
        return self.data

class GitHub:
    def __init__(self) -> None:
        pass

class YouTube:
    def __init__(self) -> None:
        self.data = None 
        self.cache = Cache(str(CACHE_DIR))
        self.update_frequency_hours = 1

    def load_data(self):
        cached_data = self.cache.get("yt") 
        
        if cached_data is None:
            print("Cache pro 'yt' neexistuje nebo vypršela. Spouštím update...")
            self._update()
            cached_data = self.cache.get("yt")

        if cached_data:
            self.data = cached_data
        else:
            print("Chyba: Nepodařilo se získat data z API ani z cache.")

    def _update(self):
        self.youtube = build('youtube', 'v3', developerKey=ENV_VAL['youtube_api_key'])
        try:
            channel_request = self.youtube.channels().list(
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
            
            playlist_request = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=1 
            )
            playlist_response = playlist_request.execute()

            latest_video = playlist_response['items'][0]
            video_title = latest_video['snippet']['title']
            video_id = latest_video['snippet']['resourceId']['videoId']
            published_at = latest_video['snippet']['publishedAt']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_url_embed = f"https://www.youtube.com/embed/{video_id}"

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
            expire_seconds = self.update_frequency_hours * 3600
            self.cache.set("yt", new_data, expire=expire_seconds)
        except Exception as e:
            print(f"Došlo k chybě: {e}")

    def get_frame(self):
        self.load_data()

        size = 'width="100%" height="450"'
        src = self.data['newest_vid']['embed']
        video_title = self.data['newest_vid']['title']
        return f'''<iframe {size} src="{src}" title="{video_title}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen="" ></iframe>'''

if __name__ == "__main__":
#    app_osu = Osu()
#    app_osu.load_data()

    app_yt = YouTube()
    
