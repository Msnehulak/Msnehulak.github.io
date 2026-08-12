# msnehulak.github.io
This is my static website built with Pelican.
**Site:** [snehulak.dev](https://snehulak.dev/)

## Start developing 
### 0. Create .venv (optional)
Create venv
```
python3 -m venv <env_name>
```
Activate
```
source .<env_name>/bin/activate
```

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Add ENV variables to .env 
Copy `.env.example` to `.env` (or create a new `.env` file) and fill in your tokens:

```env
# OSU API (get here: https://osu.ppy.sh/home/account/edit)
OSU_CLIENT_ID=
OSU_CLIENT_SECRET=

# YouTube API (get here: https://console.cloud.google.com/apis/api/youtube.googleapis.com)
YOUTUBE_API_KEY=

# Steam API (get here: https://steamcommunity.com/dev/apikey)
STEAM_API=

# Site URL (e.g. http://127.0.0.1:8000) for local testing)
SITEURL="http://127.0.0.1:8000"
```

##### Links
- [osu](https://osu.ppy.sh/home/account/edit)
- [YT](https://console.cloud.google.com/apis/api/youtube.googleapis.com)
- [steam](https://steamcommunity.com/dev/apikey)


### 3. Build Web Site
```
pelican
```
#### 3.1 Local testing
```
pelican -r -l
```


