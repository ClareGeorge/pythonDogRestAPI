import json
import logging
import os
from enum import Enum

import requests

logging.basicConfig(level=logging.INFO, filename= "..\\logfile.log",format= "%(asctime)s :%(levelname)s : %(name)s :%(message)s")
logger = logging.getLogger(__name__)
class RequestType(Enum):
    """
    Enum class for RequestType containing 4 values - GET, POST, PUT, PATCH, DELETE
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
class DogAPI:
    def __init__(self):
        """
        function to initialise API class
        """
        api_key = os.environ.get("API_KEY")
        self.headers = {"Content-Type": "application/json",
        "x-api-key": api_key}
        self.base_url = "https://api.thedogapi.com/v1"


    def call_api(self,request_type: str, endpoint: str, payload: dict |str = None)-> str:
        try:
            response = ""
            if request_type == "GET":
                response = requests.get(endpoint, timeout=30, headers= self.headers,
                params=payload)
            elif request_type == "POST":
                response = requests.post(endpoint, headers=self.headers,
                timeout=30, json=payload)
            elif request_type == "DELETE":
                response = requests.delete(f'{endpoint}/{payload}', timeout=30, headers=self.headers)
            if response.status_code in (200, 201):
                return response.json()
            elif response.status_code == 401:
                return json.dumps({"ERROR": "Authorization Error. "
            "Please check API Key"})
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logger.error(errh)
        except requests.exceptions.ConnectionError as errc:
            logger.error(errc)
        except requests.exceptions.Timeout as errt:
            logger.error(errt)
        except requests.exceptions.RequestException as err:
            logger.error(err)


    def search_breeds(self, query_str: str):
        """
        Function to Search Dog Breeds
        - https://docs.thedogapi.com/api-reference/breeds/breeds-search
        :param query_str: Query String. Type - String
        :return: Response. Type - JSON Formatted String
        """
        try:
            search_breeds_url = f"{self.base_url}/breeds/search"
            if isinstance(query_str, str):
                response = self.call_api(request_type=RequestType.GET.value,
                endpoint=search_breeds_url,
                payload={"q": query_str})
            else:
                raise ValueError("ERROR - Parameter 'query_str' should be of Type Str")
            return response
        except ValueError as valerr:
            raise ValueError("ERROR - Parameter 'query_str' should be of Type Str")

    def create_favourite(self,payload:dict):
        create_favourite_url =f'{self.base_url}/favourites'
        return self.call_api( request_type= RequestType.POST.value,
                              endpoint= create_favourite_url,
                              payload= payload
                              )
    def get_favourites(self):
        get_favourites_url = f'{self.base_url}/favourites'
        return  self.call_api(request_type=RequestType.GET.value,
                              endpoint= get_favourites_url,
                              payload="")
    def del_favourite(self,favourite_id: str):
        del_favourites_url = f'{self.base_url}/favourites'
        return self.call_api(request_type=RequestType.DELETE.value,
                             endpoint=del_favourites_url,
                             payload=favourite_id)
