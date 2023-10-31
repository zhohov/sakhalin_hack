from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from GPSPhoto import gpsphoto


def image_coordinates(gps_coords, gps_coords_ref):
    d, m, s = gps_coords
    dd = d + m / 60 + s / 3600
    if gps_coords_ref.upper() in ('S', 'W'):
        return -dd
    elif gps_coords_ref.upper() in ('N', 'E'):
        return dd
    else:
        raise RuntimeError('Incorrect gps_coords_ref {}'.format(gps_coords_ref))
