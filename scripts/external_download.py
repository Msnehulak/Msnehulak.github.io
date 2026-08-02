if __name__ == '__main__': import sweb
else: from . import sweb
import requests
from pathlib import Path

EXTRA_PATH = sweb.BASE_DIR / 'theme' / 'static' / 'extra'

def download_cnd(url, path):
    response = requests.get(url)
    response.raise_for_status()
    
    with open(path, "wb") as f:
        f.write(response.content)

def external_download():
    lib = sweb.data['exlib']

    dir_path = Path(EXTRA_PATH)
    dir_path.mkdir(parents=True, exist_ok=True)

    for i in lib:
        name = i['name']
        cnd = i['cdn']
        ftype = i['type']

        path = EXTRA_PATH / f'{name}.{ftype}'

        with sweb.timer('name'):
            download_cnd(cnd, path)
        print(f'>>> Download {name} form {cnd}')

if __name__ == '__main__':
    external_download()


