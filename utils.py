import requests

def access_nested_map(nested_map, path):
    """
    Access a nested map using the provided path.
    Raise KeyError if the key is not found.
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url):
    """
    Send a GET request to the given URL and return the JSON response.
    """
    response = requests.get(url)
    return response.json()
