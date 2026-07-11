from datetime import datetime
from pathlib import Path
from scripts.api import Osu, YouTube
from scripts.build_index import get_links_html

api_yt = YouTube()
osu_app = Osu()

def get_web_data(): 
    yt_frame = api_yt.get_frame()

    osu_data = osu_app.get_data()
    if osu_data is None:
        osu_data = {
            "rank": '-1',
            "pp": 42069,
            "acc": 101,
            "play_time": '365 dayS',
            "play_count": 0,
            "status": 'API is down, here are some funny numbers'
        }
        
    return {
        'YT_FRAME': yt_frame,
        'OSU_DATA': osu_data,
        'LINKS_CS': get_links_html(lan="cs"),
        'LINKS_EN': get_links_html(lan="en")
    }

if __name__ == "__main__":
    data = get_web_data()
    print(data)
