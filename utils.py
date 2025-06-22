def access_nested_map(nested_map, path):
    for key in path:
        try:
            nested_map = nested_map[key]
        except (TypeError, KeyError):
            raise KeyError(key)
    return nested_map
