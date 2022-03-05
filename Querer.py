import requests
from requests.exceptions import HTTPError


class Querer:
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url

    def get_name(self):
        return self.name

    def get_with_params(self, params, path=None):
        if path:
            url = self.base_url + '/' + path

        if params:
            for key in params.keys():
                url += "?" + key + "=" + str(params[key])
        try:
            response = requests.get(url)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(params)
        except Exception as err:
            print(f'Other error occurred: {err}')
            print(params)
        else:
            print(f'Params: {params} - Response Length: {len(response.content)}')
            return response.content
