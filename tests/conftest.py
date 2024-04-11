import logging

import pytest

from api.core import DogAPI

def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help ="only 2 options: chrome;edge")
    parser.addini(name="logfile",help="path of logfile",type= "string", default= "..\\logfile.txt")
@pytest.fixture(scope="session")
def dog_api():
    """ create API object """
    dog_api = DogAPI()
    return dog_api
def pytest_configure(config):
    print("In pytest_configure")



@pytest.fixture(scope="session")
def log():
    logging.basicConfig(level=logging.INFO, filename="..\\logfile.log",
                        format="%(asctime)s :%(levelname)s : %(name)s :%(message)s")
    logger = logging.getLogger(__name__)
    return logger
