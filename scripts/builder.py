from pathlib import Path
from scripts import sweb, api
import os

APP_API = api.APIs()
TRANSLATE = sweb.data['tran']

class Builder:
    def new_card_r(self, link):
        return f'href="{link}" target="_blank" rel="noopener noreferrer"'
 
    def yt_frame(self, video_id, title): 
        thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        return f'''<div class="yt-lazy-wrapper" data-video-id="{video_id}" data-title="{title}">
            <img src="{thumbnail_url}" alt="{title}" class="yt-lazy-thumbnail" fetchpriority=high>
            <button class="yt-lazy-play-btn" aria-label="Přehrát video">
            </button>
        </div>'''

    def index_links(self):
        data = sweb.data['links']
        links = ['<div class="links-index">']

        for link in data:
            symbol_id = os.path.splitext(link['img'])[0]
            sprite_path = f"{sweb.site_url}/index/images/sprite.svg#{symbol_id}"
            
            template = f'''<a href="{link['link']}" target="_blank" rel="noopener noreferrer" title="{link['hover']}">
                <svg aria-hidden="true">
                    <use href="{sprite_path}"></use>
                </svg></a>'''
            links.append(template)

        links.append('</div>')
        return ''.join(links)

    def steam_games(self, lan='en'):
        tr = {key: value[lan] for key, value in TRANSLATE['steam_games_list'].items()}
        html = []
        html.append(f'''<section class="games-section"><header class="controls-bar">
        <div class="search-box"><input type="text" id="game-search" placeholder="{tr['find_game']}" /></div>

        <div class="sort-box"><label for="sort-select">{tr['sort_by']}</label>
        <select id="sort-select">
        <option value="playtime-desc">{tr['most_played']}</option>
        <option value="playtime-asc">{tr['least_played']}</option>
        <option value="name-asc">{tr['a-z']}</option>
        <option value="name-desc">{tr['z-a']}</option>
        </select></div></header>
        <div class="games-grid" id="games-container">
        ''')
        steam_api = APP_API.get_data('steam')
        games = steam_api['games']
        for game in games:
            appid = game['appid']
            name = game['name']
            playtime_s = game['playtime_forever']
            playtime = sweb.s_to_time(m=playtime_s, lan=lan)
            steam_page = f'https://store.steampowered.com/app/{appid}'
            cover_art = f'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg' 
            card = f'''
            <article class="game-card" data-name="{name}" data-playtime="{playtime_s}" data-appid="{appid}"><div class="card-media">
            <img src="{cover_art}" alt="{name} Cover art" loading="lazy" /></div><div class="card-content">
            <h3 class="game-title">{name}</h3>
            <p class="game-playtime">{tr['play_time']} <span>{playtime}</span></p>
            <a class="steam-btn btn" {self.new_card_r(steam_page)}>{tr['steam_btn']}</a>
            </div></article>
            '''
            html.append(card)

        html.append('</div></section>')

        return ''.join(html)

    def projects_cards(self, lan = 'en'):
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
    i = builder.steam_games()
    print(i)
