import subprocess
import yaml
from pathlib import Path
from datetime import datetime
from scripts.api import APIs
from scripts.builder import Builder
from pelicanconf import SITEURL
from scripts import sweb

BASE_DIR = Path(__file__).resolve().parent
builder = Builder()

def get_web_data():
    app_apis = APIs()
    
    # -- YT Frame --
    yt_data = app_apis.get_data('yt')
    yt_vid_id = yt_data['newest_vid']['id']
    yt_vid_name = yt_data['newest_vid']['title']
    yt_frame = builder.yt_frame(yt_vid_id, yt_vid_name)

    index_links = builder.index_links(site_url=SITEURL)

    # -- OSU --
    osu_row = sweb.data['osu']
    if not osu_row:
        osu_row = { "osu": {
            "offset": {
                "x": 75, "y": 50
            }, "area": {
                "w": 65, "h": 45
            }, "sr": 6.2}}

    osu_stats = osu_row['osu'] 
    osu_data = app_apis.get_data('osu')
    if osu_data is None:
        osu_data = {
            "rank": '-1',
            "pp": 42069,
            "acc": 101,
            "play_time": '365 dayS',
            "play_count": 0,
        }

    osu_data["offset"] = {
        "x": osu_stats['offset']['x'],
        "y": osu_stats['offset']['y'],
    }
    osu_data["area"] = {
        "h": osu_stats['area']['h'],
        "w": osu_stats['area']['w'],
    }

    # -- Projects Cards --
    projects = {
        'cs': builder.projects_cards(lan='cs'),
        'en': builder.projects_cards(lan='en')
    }

    return {
        'YT_FRAME': yt_frame,
        'OSU_DATA': osu_data,
        'INDEX_LINKS_DIV': index_links,
        'PROJECTS': projects,
    }

if __name__ == "__main__":
    data = get_web_data()
    print(data)
