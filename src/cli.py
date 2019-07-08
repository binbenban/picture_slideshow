import subprocess
import sys
from pathlib import Path
import os
import fire
from picture_slideshow.run import main


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

# get our package onto the python path
PROJ_PATH = Path(__file__).resolve().parent
sys.path.append(str(PROJ_PATH / "src"))
os.environ["PYTHONPATH"] = (
    os.environ.get("PYTHONPATH", "") + os.pathsep + str(PROJ_PATH / "src")
)
os.environ["IPYTHONDIR"] = str(PROJ_PATH / ".ipython")

def run():
    main()


def test():
    from tests.test_connection import test_pcloud
    test_pcloud()


def entry_point():
    fire.Fire()

if __name__ == '__main__':
    entry_point()

