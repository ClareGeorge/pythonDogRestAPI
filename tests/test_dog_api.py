import os

import pytest

from utilities.ReadExcel import ReadExcel

dict_favourite ={}
def test_search_breeds(dog_api, pytestconfig, getExcelData) -> None:
    """
    Unit Test to Search Dog Breeds
    :param dog_api: Class Object Parameter from conftest.
            Type - DogAPI
    :return: None
    """
    expected_response = [
        {
            "weight": {
                "imperial": "45 - 65",
                "metric": "20 - 29"
            },
            "height": {
                "imperial": "21.5 - 25",
                "metric": "55 - 64"
            },
            "id": 261,
            "name": "Wirehaired Vizsla",
            "breed_group": "Sporting",
            "life_span": "12 - 14 years",
            "reference_image_id": "r1I4hl5Em",
            "image": {
                "id": "r1I4hl5Em",
                "width": 1024,
                "height": 770,
                "url": "https://cdn2.thedogapi.com/images/r1I4hl5Em.jpg"
            }
        }
    ]
    actual_response = dog_api.search_breeds(query_str=getExcelData["param1"])
    assert actual_response == expected_response

def test_search_breeds_invalid_criteria(dog_api ,) -> None:
    with pytest.raises(ValueError):
        actual_response = dog_api.search_breeds(query_str=1)

def test_search_breeds_zero_records(dog_api, log ,getdata_search_breeds_zero_records) -> None:
        actual_response = dog_api.search_breeds(query_str=getdata_search_breeds_zero_records["param1"])
        assert actual_response.__len__() == 0
        log.info( f'{os.environ.get('PYTEST_CURRENT_TEST')} Passed')

def test_get_favourites(dog_api) ->None:
    global dict_favourite
    actual_response = dog_api.get_favourites()
    assert  len(actual_response) > 0
    dict_favourite = actual_response[0]

def test_del_favourite(dog_api,) ->None:

    actual_response = dog_api.del_favourite(dict_favourite["id"])
    assert actual_response["message"] == "SUCCESS"



def test_create_favourite(dog_api, log):
    global dict_favourite
    actual_response = dog_api.create_favourite({
                            "image_id": f'{dict_favourite["image_id"]}',
                            "sub_id": f'{dict_favourite["sub_id"]}'
                        })
    assert  actual_response["message"] == "SUCCESS"
    log.info(f'{os.environ.get('PYTEST_CURRENT_TEST')} Passed')


@pytest.fixture(params=ReadExcel.getTestDataFromExcel("test_search_breeds"))
def getExcelData(request):
    return request.param

@pytest.fixture(params=ReadExcel.getTestDataFromExcel("test_search_breeds_zero_records"))
def getdata_search_breeds_zero_records(request):
    return request.param

