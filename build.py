from datetime import datetime
import subprocess
from pathlib import Path
from code.api import Osu
from code.api import YouTube
from code.build_index import get_links_html

api_yt = YouTube()

class BuildWebsite:
    def __init__(self) -> None:
        pass

    def content_build(self, data: dict, file: str):
        template_path = Path(f"content/{file}.md.template")
        output_path = Path(f"content/{file}.md")

        if template_path.exists():
            text = template_path.read_text(encoding="utf-8")
            for key, value in data.items():
                text = text.replace(f'{{{{ {key} }}}}', f'{value}')
            output_path.write_text(text, encoding="utf-8")
            print(f"Page `{file}.md` is build.")

    def index(self):
            new_vid_frame = api_yt.get_frame()
            data_cs = {
                "links": get_links_html(lan = "cs"),
                'new_video': new_vid_frame,
            }
            self.content_build(data_cs, 'cs/index')

            data_en = {
                "links": get_links_html(lan = "en"),
                'new_video': new_vid_frame,
            }
            self.content_build(data_en, 'en/index')

    def osu(self):
        osu_app = Osu()
        data = osu_app.get_data()

        if data is None:
            print('I DONT HAVE DATA')
            data = {
                "rank": '-1',
                "pp": 42069,
                "acc": 101,
                "play_time": 365,
                "play_count": 0,
                # "avatar": user.avatar_url
                "status": 'API is down, here are some funny numbers'
            }

        self.content_build(data, 'en/osu')
        self.content_build(data, 'cs/osu')

    def build_website(self):
        self.osu()
        self.index()

        print("Spouštím Pelican build...")
        subprocess.run(["pelican", "content", "-s", "pelicanconf.py"])

if __name__ == "__main__":
    app = BuildWebsite()
    app.build_website()
