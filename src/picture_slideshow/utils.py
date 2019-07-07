import yaml
from pcloud import PyCloud

params = None
pc = None

def load_params() -> dict:
    global params
    if params is None:
        with open('conf/parameters.yml', 'r') as stream:
            params = yaml.safe_load(stream)
        with open('conf/parameters_secure.yml', 'r') as stream2:
            params.update(yaml.safe_load(stream2))
    return params


def pcloud() -> PyCloud:
    global pc
    if pc is None:
        pc = PyCloud(
            params['pcloud']['user'],
            params['pcloud']['password'])
    return pc

