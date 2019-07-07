import yaml
from pcloud import PyCloud

params = None
pc = None

def load_params() -> dict:
    global params
    if params is None:
        with open('conf/parameters.yml', 'r') as stream:
            params = yaml.safe_load(stream)
    return params

def pcloud() -> PyCloud:
    global pc
    if pc is None:
        pc = PyCloud(
            params['pcloud']['user'],
            params['pcloud']['password'])
    return pc

