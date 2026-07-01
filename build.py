from datetime import datetime
import subprocess
from pathlib import Path
from code.osu import Osu

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

    def osu(self):
        osu_app = Osu()
        osu_app.load_data()
        data = osu_app.data

        if data is None:
            data = {
                "rank": '-1',
                "pp": 42069,
                "acc": 101,
                "play_time": 365,
                "play_count": 0,
                # "avatar": user.avatar_url
                "status": 'API is down, here are some funny numbers'
            }
        else:
            msg = f'update at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

            data['status'] = msg 

        self.content_build(data, 'osu')

    def build_website(self):
        self.osu()

        print("Spouštím Pelican build...")
        subprocess.run(["pelican", "content", "-s", "pelicanconf.py"])

if __name__ == "__main__":
    app = BuildWebsite()
    app.build_website()
