from setuptools import find_packages, setup

entry_point = (
    "picture_slideshow = picture_slideshow.run:main"
)

# get the dependencies and installs
with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = [x.strip() for x in f if x.strip()]

setup(
    name="picture_slideshow",
    version="0.1",
    packages=find_packages(exclude=["tests"]),
    install_requires=requires,
    extras_require={},
    entry_points={
        'console_scripts': ['picshow = cli:entry_point']
    }
)
