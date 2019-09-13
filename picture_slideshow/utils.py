import yaml
import os
import glob
from pcloud import PyCloud
from typing import List
from picture_slideshow.my_pcloud import RemoteFile


params = None
pc = None


def load_params() -> dict:
    global params
    if params is None:
        with open("conf/parameters.yml", "r") as stream:
            params = yaml.safe_load(stream)
        with open("conf/parameters_secure.yml", "r") as stream2:
            params.update(yaml.safe_load(stream2))
    return params


def pcloud() -> PyCloud:
    global pc

    load_params()
    if pc is None:
        pc = PyCloud(params["pcloud"]["user"], params["pcloud"]["password"])
    return pc


def locate_image_in_folder(folder_content: List[RemoteFile], image_name: str) -> int:
    result = 0
    for idx, x in enumerate(folder_content):
        if x.filename == image_name:
            result = idx
            break
    return result


def delete_files_in_folder(folderpath: str):
    files = glob.glob(f"{folderpath}/*")
    for f in files:
        os.remove(f)
