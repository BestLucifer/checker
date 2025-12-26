import requests
from PIL import Image
from io import BytesIO

ACCEPTED_FILE_FORMATS = ("gif", "png", "jpeg")


def download_image_as(url, file_format, file_name=None):
    file_format = file_format.lower()
    if file_format.startswith("."):
        file_format = "".join(file_format.split(".")[1:])
    if file_format not in ACCEPTED_FILE_FORMATS:
        raise Exception("Dosyanın uzantısı doğru değil. ({})".format(file_format))
    if url.startswith('//'):
        url = 'http://' + url.split('//')[1]
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Urldeki image yüklenemedi {} , hata kodu: {}".format(url, response.status_code))
    infile = Image.open(BytesIO(response.content))
    if infile.mode != 'RGB':
        infile = infile.convert('RGB')
    infile.save(file_name)
    return file_name, response.status_code


def download_image_as_gif(url, file_name=None):
    return download_image_as(url, "GIF", file_name)


def download_image_as_jpeg(url, file_name=None):
    return download_image_as(url, "JPEG", file_name)


def download_image_as_png(url, file_name=None):
    return download_image_as(url, "PNG", file_name)
