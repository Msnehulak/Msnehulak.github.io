from datetime import datetime
from pathlib import Path
from scripts.api import APIs
from scripts.builder import Builder

builder = Builder()

def get_web_data():
    app_apis = APIs()
    
    # -- YT Frame --
    yt_data = app_apis.get_data('yt')
    yt_vid_id = yt_data['newest_vid']['id']
    yt_vid_name = yt_data['newest_vid']['title']
    yt_frame = builder.yt_frame(yt_vid_id, yt_vid_name)
    
    index_links = builder.index_links()

    # -- OSU --
    osu_data = app_apis.get_data('osu')
    if osu_data is None:
        osu_data = {
            "rank": '-1',
            "pp": 42069,
            "acc": 101,
            "play_time": '365 dayS',
            "play_count": 0,
        }

    return {
        'YT_FRAME': yt_frame,
        'OSU_DATA': osu_data,
        'INDEX_LINKS_DIV': index_links, 
    }

if __name__ == "__main__":
    data = get_web_data()
    print(data)
