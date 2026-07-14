import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Builder:
    @staticmethod
    def yt_frame(video_id, title): 
        return f'''<iframe width="100%" height="450" 
        src="https://www.youtube-nocookie.com/embed/{video_id}" 
        title="{title}" frameborder="0" loading="lazy"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        referrerpolicy="strict-origin-when-cross-origin" 
        allowfullscreen=""></iframe>''' 

    @staticmethod
    def index_links(site_url=''):
        master_links = BASE_DIR / 'data' / 'links.yaml'
        with open(master_links, 'r') as f:
            data = yaml.safe_load(f)

        links = ['<div class="links-index">']
        new_window = 'target="_blank" rel="noopener noreferrer"'

        for link in data:
            template =  f'''<a href="{link['link']}" class="index-a"
            target="_blank" rel="noopener noreferrer">
            <img src="{site_url}/images/icon/btrace/{link['img']}" 
            alt="{link['hover']}" title="{link['hover']}"
            class="index-img" loading="lazy"></a>'''
            links.append(template)

        links.append('</div>')

        return ''.join(links)
