import requests
import os


def image_coordinates(gps_coords, gps_coords_ref):
    d, m, s = gps_coords
    dd = d + m / 60 + s / 3600
    if gps_coords_ref.upper() in ('S', 'W'):
        return -dd
    elif gps_coords_ref.upper() in ('N', 'E'):
        return dd
    else:
        raise RuntimeError('Incorrect gps_coords_ref {}'.format(gps_coords_ref))


def get_address(coord_1, coord_2) -> list:
    api_key = os.getenv('YAMAPS_API')
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={coord_1},{coord_2}&results=1&format=json'
    request = requests.get(url=url)
    response = request.json()
    address = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
    return address


def verified_address(address, task_address) -> bool:
    for i in task_address.__str__().split(', '):
        print(i)
        if i not in address:
            print(address)
            return False
    return True

