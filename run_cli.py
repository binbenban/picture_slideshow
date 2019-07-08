import subprocess
import sys
from pathlib import Path
import os
import click


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

# get our package onto the python path
PROJ_PATH = Path(__file__).resolve().parent
sys.path.append(str(PROJ_PATH / "src"))
os.environ["PYTHONPATH"] = (
    os.environ.get("PYTHONPATH", "") + os.pathsep + str(PROJ_PATH / "src")
)
os.environ["IPYTHONDIR"] = str(PROJ_PATH / ".ipython")



@click.command()
def run():
    from picture_slideshow.run import main
    main()


if __name__ == '__main__':
    run()