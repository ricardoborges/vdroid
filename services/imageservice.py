import os, scope
from pprint import pprint
from PIL import Image
from py_linq import Enumerable

def is_vertical(image_path):
    with Image.open(image_path) as im:
        width, height = im.size
        aspect_ratio = width / height
        return aspect_ratio < 1

def imageResolution(image_path):
    with Image.open(image_path) as im:
        width, height = im.size
        return width, height

def get_file_length(file_path):
    with open(file_path, 'rb') as file:
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
    return file_length


def imagesInDisc():
    list = []
    for root, dirs, files in os.walk(scope.basedir):
        for file in files:
            if file.endswith(".jpg"):
                path = os.path.join(root, file)
                try:
                    w,h  = imageResolution(path)
                    length = get_file_length(path)
                    list.append({'path':path, 'filename': file, 'isvertical': is_vertical(path), 'width':w, 'height':h, 'length': length})
                except:
                    w,h = 0,0

    return list

def select_images():
    all = Enumerable(imagesInDisc())

    if (scope.options['short'] == 'True'):
        list =  all.where(lambda x: x['isvertical']).distinct(lambda x:x['length']).order_by_descending(lambda x:x['length']).to_list()
    else:
        list = all.distinct(lambda x:x['length']).order_by_descending(lambda x:x['length']).to_list()

    if (scope.posterFound):
        try:
            path = f"{scope.basedir}/poster.jpg"
            w,h  = imageResolution(path)
            length = get_file_length(path)
            result = [{'path':path, 'filename': "poster.jpg", 'isvertical': is_vertical(path), 'width':w, 'height':h, 'length': length}] + list
        except:
            w,h = 0,0
    else:
        result = list

    return result[:scope.totalScenes]



