# msnehulak.github.io
This is my static website built with Pelican.
**Site:** [msnehulak.github.io](https://msnehulak.github.io)

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
example
```
OSU_CLIENT_ID= # ID
OSU_CLIENT_SECRET= # SECRET
GIT_HUB_TOKEN= # GitHub Token
YOUTUBE_API_KEY= # YouTube API key
```

### 3. Build Web Site
```
pelican
```
#### 3.1 Local testing
```
pelican -r -l
```
