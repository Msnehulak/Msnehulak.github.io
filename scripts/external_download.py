if __name__ == '__main__': import sweb
else: from . import sweb
import requests
from pathlib import Path
import re
import logging
import sys
from tqdm import tqdm
import shutil

DOWNLOAD_TO_PATH = sweb.BASE_DIR / 'cache' / 'extra'
OUTPUT_PATH = sweb.BASE_DIR / 'output' / 'static' / 'extra'

def download_cdn(url, path):
    response = requests.get(url)
    response.raise_for_status()
    
    with open(path, "wb") as f:
        f.write(response.content)

def _validate_file_name(name: str) -> bool:
    check = re.sub(r'[^a-zA-Z0-9._-]', '', name)
    return name == check

def external_download():
    lib = sweb.data['exlib']

    dir_path = Path(DOWNLOAD_TO_PATH)
    dir_path.mkdir(parents=True, exist_ok=True)

    with tqdm(total=len(lib), desc="Downloaded form cnd", unit="download") as pbar:
        for i in lib:
            name = i['name']
            cdn = i['cdn']
            ftype = i['type']
            extra = i.get('extra', None)
            save_as = ''

            if not _validate_file_name(f'{name}{ftype}'):
                logging.error(f"'{name}.{ftype}' contains invalid characters, please fix it in data/external_download.yaml")
                sys.exit(1) 

            if extra is not None and extra['save_as']:
                save_as = extra['save_as']
                if '..' in save_as:
                    logging.error(f"'{name} save as' contains invalid characters, please fix it in data/external_download.yaml")
                    sys.exit(1)
           
            path = DOWNLOAD_TO_PATH / save_as 
            file_path = path / f'{name}.{ftype}'
            path.mkdir(parents=True, exist_ok=True)

            if file_path.exists():
                pbar.update(1)
                continue

            download_cdn(cdn, file_path)

            pbar.update(1)

def move_file():
    if not DOWNLOAD_TO_PATH.exists():
        logging.warning(f"Path {DOWNLOAD_TO_PATH} don't exist.  maybe for got download?")
        return

    if OUTPUT_PATH.exists():
        logging.debug(f'fle {DOWNLOAD_TO_PATH} alrady exists in {OUTPUT_PATH}')
        return

    shutil.copytree(DOWNLOAD_TO_PATH, OUTPUT_PATH)
    logging.debug(f'fle {DOWNLOAD_TO_PATH} is move to {OUTPUT_PATH}')

if __name__ == '__main__':
    external_download()
