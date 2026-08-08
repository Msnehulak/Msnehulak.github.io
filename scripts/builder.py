from pathlib import Path
if __name__ == '__main__': import sweb
else: from . import sweb
import os

BASE_DIR = Path(__file__).resolve().parent.parent

class Builder:
    @staticmethod
    def yt_frame(video_id, title): 
        thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        return f'''<div class="yt-lazy-wrapper" data-video-id="{video_id}" data-title="{title}">
            <img src="{thumbnail_url}" alt="{title}" class="yt-lazy-thumbnail" fetchpriority=high>
            <button class="yt-lazy-play-btn" aria-label="Přehrát video">
            </button>
        </div>'''

    @staticmethod
    def index_links():
        data = sweb.data['links']
        links = ['<div class="links-index">']

        for link in data:
            # 1. Získání ID (odstraníme koncovku .svg z links.yaml, např. youtube.svg -> youtube)
            symbol_id = os.path.splitext(link['img'])[0]
            sprite_path = f"{sweb.site_url}/index/images/sprite.svg#{symbol_id}"
            
            # 2. Vykreslení pomocí <svg><use></use></svg> místo <img>
            template = f'''<a href="{link['link']}" target="_blank" rel="noopener noreferrer" title="{link['hover']}">
                <svg aria-hidden="true">
                    <use href="{sprite_path}"></use>
                </svg></a>'''
            links.append(template)

        links.append('</div>')
        return ''.join(links)

    @staticmethod
    def projects_cards(lan = 'en'):
        data = sweb.data['projects']

        slides = []
        for i in data:
            texts = i['content'][lan]
            
            if lan == sweb.site_lan:
                lan_url = '/'
            else:
                lan_url = f'/{lan}/'

            link = f'{sweb.site_url}{lan_url}projects/{i['content']['link']}'
            btn_html = ''
            if not i['content']['link'] == 'None':
                btn_html = f'<a href="{link}" class="card-btn btn">{texts["btn"]}</a>'

            slide_html = (
                f'<div class="swiper-slide">'
                f'<h2>{texts["head"]}</h2>'
                f'<p>{texts["desc"]}</p>' 
                f'{btn_html}'
                f'</div> \n'
            )
            slides.append(slide_html)
        
        all_slides = ''.join(slides)
        
        full_html = f'''<div class="swiper mySwiper">
<div class="swiper-wrapper">
{all_slides}
</div></div>'''

        return full_html
if __name__ == '__main__':
    builder = Builder()
    i = builder.projects_cards()
    print(i)
