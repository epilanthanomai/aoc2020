import os

ROOT = os.path.dirname(__file__)


def open_data(filename):
    path = os.path.join(ROOT, "data", filename)
    return open(path)
