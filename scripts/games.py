from scripts import sweb, api

APP_API = api.APIs()
GAME_DATA = sweb.data['games']

class Games:
    def __init__(self):
        self.games = []
        self.add_steam_games()
        self.add_osu()
    
    def get_games(self):
        return self.games
        
    def add_steam_games(self):
        steam_api = APP_API.get_data('steam')
        games = steam_api['games']
        for game in games:
            appid = game["appid"]
            self.games.append({
                'type': 'steam',
                'name': game["name"],
                'play_time': game['playtime_forever']*60,
                'link': f'https://store.steampowered.com/app/{appid}',
                'art': f'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/header.jpg',
            })
    
    def add_osu(self):
        osu_api = APP_API.get_data('osu')
        play_time = osu_api['play_time']
        osu_data = GAME_DATA['osu']
        self.games.append({
            'type': 'custom',
            'name': 'OSU!',
            'play_time': play_time,
            'link': osu_data['link'],
            'art': osu_data['art'],
            'more': {
                'new_tab': False,
            },
        })


if __name__ == '__main__':
    app = Games()
    print(app.get_games())
