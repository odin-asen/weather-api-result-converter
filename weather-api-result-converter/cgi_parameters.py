import os


def get_cgi_url_path():
    if 'PATH_INFO' in os.environ:
        return os.environ['PATH_INFO']
    return ''


def get_cgi_url_query_string():
    if 'QUERY_STRING' in os.environ:
        return os.environ['QUERY_STRING']
    return ''
