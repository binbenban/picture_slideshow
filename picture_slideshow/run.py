import os
import logging
import zipfile
from pcloud import PyCloud
from picture_slideshow.utils import load_params, pcloud, locate_image_in_folder, delete_files_in_folder
from picture_slideshow.my_pcloud import RemoteFile
from datetime import datetime
from typing import List


log = logging.getLogger(__name__)
params = load_params()
dl_path = params['download_folder']
dl_zip_filepath = f"{dl_path}/dl.zip"


def main():
    """
    entry point
    store the next 200 pictures
    """
    remotefiles = get_next_batch()
    log.warning(f"retrieved remote files, size {len(remotefiles)}")

    delete_files_in_folder(dl_path)
    download_batch_as_zip(remotefiles)
    extract_zip()


def download_batch_as_zip(remotefiles: List[RemoteFile]) -> None:
    kwargs = {
        'fileids': ','.join([str(x.fileid) for x in remotefiles]),
    }
    zip_stream = pcloud()._do_request('getzip', json=False, **kwargs)
    with open(dl_zip_filepath, 'wb') as dl:
        dl.write(zip_stream)


def extract_zip() -> None:
    zip_ref = zipfile.ZipFile(dl_zip_filepath, 'r')
    zip_ref.extractall(params['download_folder'])
    zip_ref.close()
    os.remove(dl_zip_filepath)


def get_next_batch():
    last_image = last_downloaded_image()
    log.warning(f'last image is {last_image}')
    year = last_image.split('-')[0]
    month = last_image.split('-')[1]

    cur_folder_path = f"{year}/{year}{month}"
    cur_folder_content = retrieve_remote_folder(cur_folder_path)
    cur_folder_position = locate_image_in_folder(cur_folder_content, last_image)
    log.warning(f"last image in its folder at position {cur_folder_position}")
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


def next_folder(folder_path: str):
    all_folders = build_all_possible_folders()
    index = all_folders.index(folder_path) + 1
    if index == len(all_folders):
        index = 0
    return all_folders[index]


def download_from_folder(folder_path: str, start: int, max: int):
    folder_list = retrieve_remote_folder(folder_path)
    return folder_list[start:start+max]


def last_downloaded_image() -> str:
    files = sorted([x for x in os.listdir(params['download_folder']) if '.jpg' in x or '.png' in x])
    print(files)
    if files:
        return files[-1]
    else:
        # very first image
        return params['default_first_image']


def retrieve_remote_folder(folder_path='') -> List[RemoteFile]:
    root = params['pic_root_folderid']   #  "/pCloud Sync/pictures"
    root_subfolders = pcloud().listfolder(folderid=root)['metadata']['contents']
    files = []
    remote_files = []

    try:
        if folder_path:
            year = folder_path.split('/')[0]
            month = folder_path.split('/')[1]
            # go thru result to find folder with name = year
            folderid_of_year = [afolder['folderid'] for afolder in root_subfolders if afolder['name']==year][0]
            
            # go thru this subfolder again to find month
            year_subfolders = pcloud().listfolder(folderid=folderid_of_year)['metadata']['contents']
            folderid_of_month = [afolder['folderid'] for afolder in year_subfolders if afolder['name']==month][0]
            files = pcloud().listfolder(folderid=folderid_of_month)['metadata']['contents']
    except Exception as e:
        log.error(e)
    
    remote_files = [RemoteFile(x['fileid'], x['name']) for x in files if 'image' in x['contenttype']]
    return sorted(remote_files, key=lambda rf: rf.filename)


def build_all_possible_folders() -> List[str]:
    result = []
    cur_year = datetime.now().year
    for year in range(2002, cur_year+1):
        for month in range(1, 13):
            folder_path = f"{year}/" + f"{year}" + f"{month}".zfill(2)
            result.append(folder_path)
    return result


if __name__ == '__main__':
    main()