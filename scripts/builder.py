from pathlib import Path
from . import sweb

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
        data = sweb.data['links']


        links = ['<div class="links-index">']
        new_window = 'target="_blank" rel="noopener noreferrer"'

        for link in data:
            link_img = f'{site_url}/images/icon/{link['img']}'
            template =  f'''<a href="{link['link']}" class="index-a"
            target="_blank" rel="noopener noreferrer">
            <img src="{link_img}" 
            alt="{link['hover']}" title="{link['hover']}"
            class="index-img" loading="lazy"></a>'''
            links.append(template)

        links.append('</div>')

        return ''.join(links)

    @staticmethod
    def projects_cards(lan = 'en'):
        data = sweb.data['projects']

        slides = []
        for i in data:
            texts = i['content'][lan]

            link = f'{sweb.site_url}/projects/{i['content']['link']}'
            btn_html = ''
            if not i['content']['link'] == 'None':
                btn_html = f'<a href="{link}" class="card-btn">{texts["btn"]}</a>'

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
