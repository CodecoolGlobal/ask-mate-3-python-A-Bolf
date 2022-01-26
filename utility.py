import data_manager

def get_headers(table_name):
    header_dicts = data_manager.get_headers_from_table(table = table_name)
    return [header['json_object_keys'] for header in header_dicts]