from pcloud import PyCloud
import os
from picture_slideshow.utils import load_params, pcloud
from datetime import datetime
from typing import List


params = load_params()

def main():
    """
    entry point
    store the next 200 pictures
    """
    pass


def get_next_batch():
    last_image = last_downloaded_image()
    year = last_image.split('-')[0]
    month = last_image.split('-')[1]

    cur_folder_path = f"{year}/{year}{month}"
    cur_folder_content = retrieve_remote_folder(cur_folder_path)
    cur_folder_position = cur_folder_content.index(last_image)
    images_to_download = []

    while len(images_to_download) < params['batch_size']:
        images_to_download += download_from_folder(
            cur_folder_path, 
            cur_folder_position, 
            params['batch_size']-len(images_to_download)
        )
        cur_folder_path = next_folder(cur_folder_path)
        cur_folder_position = 0
    
    return images_to_download


def next_folder(folder_path):
    all_folders = build_all_possible_folders()
    index = all_folders.index(folder_path) + 1
    if index == len(all_folders):
        index = 0
    return all_folders[index]


def download_from_folder(folder_path: str, start: int, max: int):
    folder_list = retrieve_remote_folder(folder_path)
    return folder_list[start:start+max]


def last_downloaded_image() -> str:
    files = list(os.listdir('data/downloaded_images'))
    if files:
        return files[-1]
    else:
        # very first image
        return params['default_first_image']


def retrieve_remote_folder(folder_path='') -> List[str]:
    root = params['pic_root_folderid']   #  "/pCloud Sync/pictures"
    root_subfolders = pcloud().listfolder(folderid=root)['metadata']['contents']
    result = []

    try:
        if folder_path:
            year = folder_path.split('/')[0]
            month = folder_path.split('/')[1]
            # go thru result to find folder with name = year
            folderid_of_year = [afolder['folderid'] for afolder in root_subfolders if afolder['name']==year][0]
            
            # go thru this subfolder again to find month
            year_subfolders = pcloud().listfolder(folderid=folderid_of_year)['metadata']['contents']
            folderid_of_month = [afolder['folderid'] for afolder in year_subfolders if afolder['name']==month][0]
            result = pcloud().listfolder(folderid=folderid_of_month)['metadata']['contents']
    except Exception as e:
        print(e)
    print(result)
    return sorted([x['name'] for x in result if 'image' in x['contenttype']])


def build_all_possible_folders() -> List[str]:
    result = []
    cur_year = datetime.now().year
    for year in range(2002, cur_year+1):
        for month in range(1, 13):
            folder_path = f"{year}/" + f"{year}" + f"{month}".zfill(2)
            result.append(folder_path)
    return result


if __name__ == '__main__':
    # x = get_next_batch()
    # print(x)
    r = pcloud().downloadfile(
        url='2008-12-31 18.58.45.jpg', 
        folderid=params['pic_root_folderid'],
        links
    )
    print(r)