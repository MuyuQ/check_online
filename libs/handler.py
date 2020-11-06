import requests

def http_handler(ip_address, **kwargs):
    try:
        r = requests.get(ip_address, timeout=(2,4))
    except requests.exceptions.RequestException as e:
        return '异常'

    return '在线'
