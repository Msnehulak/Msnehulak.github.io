import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeAPIWrapper:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("Chybí YOUTUBE_API_KEY v proměnných prostředí (.env).")

        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def get_channel_by_id(self, channel_id: str) -> dict | None:
        """Získá základní informace o kanálu podle jeho ID."""
        try:
            response = (
                self.youtube.channels()
                .list(part="snippet,statistics,brandingSettings", id=channel_id)
                .execute()
            )

            items = response.get("items", [])
            if not items:
                return None

            channel = items[0]
            snippet = channel.get("snippet", {})
            statistics = channel.get("statistics", {})

            return {
                "channel_id": channel_id,
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "custom_url": snippet.get("customUrl"),
                "published_at": snippet.get("publishedAt"),
                "thumbnails": snippet.get("thumbnails", {}),
                "subscriber_count": statistics.get("subscriberCount"),
                "video_count": statistics.get("videoCount"),
            }
        except HttpError as e:
            print(f"Chyba při komunikaci s YouTube API (Channel): {e}")
            return None

    def get_video_by_id(self, video_id: str) -> dict | None:
        """Získá informace o videu podle jeho ID."""
        try:
            response = (
                self.youtube.videos()
                .list(part="snippet,statistics,contentDetails", id=video_id)
                .execute()
            )

            items = response.get("items", [])
            if not items:
                return None

            video = items[0]
            snippet = video.get("snippet", {})
            statistics = video.get("statistics", {})

            return {
                "video_id": video_id,
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "channel_id": snippet.get("channelId"),
                "channel_title": snippet.get("channelTitle"),
                "published_at": snippet.get("publishedAt"),
                "thumbnails": snippet.get("thumbnails", {}),
                "view_count": statistics.get("viewCount"),
                "like_count": statistics.get("likeCount"),
                "comment_count": statistics.get("commentCount"),
            }
        except HttpError as e:
            print(f"Chyba při komunikaci s YouTube API (Video): {e}")
            return None

    def get_video_with_creator(self, video_id: str) -> dict | None:
        """Z വർce z ID videa vrátí jak informace o videu, tak detailní informace o tvůrci (kanálu)."""
        video_info = self.get_video_by_id(video_id)
        if not video_info:
            return None

        channel_id = video_info.get("channel_id")
        creator_info = None
        if channel_id:
            creator_info = self.get_channel_by_id(channel_id)

        return {"video": video_info, "creator": creator_info}


# Pomocná instance nebo funkce pro zpětnou kompatibilitu s tvým kódem v yt_iframe.py
_client = None


def get_client() -> YouTubeAPIWrapper:
    global _client
    if _client is None:
        _client = YouTubeAPIWrapper()
    return _client


def get_video_with_creator(video_id: str) -> dict | None:
    return get_client().get_video_with_creator(video_id)
