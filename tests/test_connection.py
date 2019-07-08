from picture_slideshow.utils import pcloud

def test_pcloud():
    pc = pcloud()
    assert pc is not None
    