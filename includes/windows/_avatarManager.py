import base64
import os
import sys
import requests

from includes.util.Logging import Logger
from io import BytesIO
from PIL import Image, ImageTk, ImageDraw

import cache

logger:Logger = Logger('AvatarManager')


def check_internet_connection():
    """
    Checks if there is an internet connection by attempting to make a request to a reliable URL.

    :return: True if there is an internet connection, otherwise False.
    :rtype: bool
    """
    try:
        # Try making a simple GET request to a known reliable URL (e.g., Google's homepage).
        response = requests.get("http://www.google.com", timeout=3)
        cache.internet = True
        return response.status_code == 200
    except requests.RequestException:
        cache.internet = False
        return False

def load_image_from_url(url, default=None):
    """
    Lädt ein Bild von einer angegebenen URL herunter und gibt das Bildobjekt zurück.

    Das Bild wird von der angegebenen URL abgerufen, erforderliche Daten werden im
    Speicher verarbeitet, und das Bild wird mithilfe von `Pillow` geöffnet und
    zurückgegeben.

    :param url: Die URL, von der das Bild heruntergeladen werden soll.
    :type url: str
    :return: Ein Bildobjekt, das die heruntergeladene Bilddatei repräsentiert.
    :rtype: PIL.Image.Image
    :raises requests.HTTPError: Wird ausgelöst, wenn die HTTP-Anfrage fehlschlägt, z.B. bei 404 oder 500.
    """
    logger.debug(f"load_image_from_url:{url}")
    if not cache.internet:
        if not default.endswith(".png") or not default.endswith(".jpg") or not default.endswith(".jpeg"):
            img_data = base64.b64decode(cache.user_default_avatar)
            img = Image.open(BytesIO(img_data))
        else:
            img = Image.open(default)
        logger.debug(f"img:{img}")
        return img

    try:
        response = requests.get(url)
        response.raise_for_status()  # Überprüft, ob die Anfrage erfolgreich war
        img_data = BytesIO(response.content)  # Bilddaten in einen BytesIO-Stream laden
        logger.debug(f"img_data:{img_data}")
        return Image.open(img_data)
    except requests.exceptions.RequestException as e:
        if default.endswith(".png") or default.endswith(".jpg") or default.endswith(".jpeg"):
            img = Image.open(default)
        else:
            img_data = base64.b64decode(cache.user_default_avatar)
            img = Image.open(BytesIO(img_data))
        logger.debug(f"img:{img}")
        return img

def load_image_from_base64(base64_string):
    """
    Decodiert einen Base64-kodierten Bild-String und lädt das Bild-Objekt.

    Diese Funktion nimmt einen Base64-kodierten Bild-String, dekodiert ihn und
    erzeugt ein Bild-Objekt, das weiterverwendet werden kann.

    :param base64_string: Der Base64-kodierte Bild-String.
    :type base64_string: str
    :return: Ein Bild-Objekt, das aus dem dekodierten Bild-String erstellt wurde.
    :rtype: Image
    """
    logger.debug(f"load_image_from_base64: {base64_string}")
    img_data = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_data))
    logger.debug(f"img:{img}")
    return img

def loadImage(parent, image: str = None, defult_image=None, width: int = 48, height: int = 48):
    if image is None:
        image = cache.user_default_avatar  # Assuming 'cache' is predefined

    # Load image (from URL or base64)
    if image.startswith("http"):
        img = load_image_from_url(image, defult_image)
    else:
        img = load_image_from_base64(image)

    # Resize Image
    img = img.resize((width, height), Image.LANCZOS)

    # Make Image Rounded
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)

    rounded_img = Image.new("RGBA", (width, height))
    rounded_img.paste(img, (0, 0), mask)

    # Convert to Tkinter Image
    parent.img_tk = ImageTk.PhotoImage(rounded_img)
    return parent.img_tk

def resource_path(relative_path):
    """ Get the absolute path to resource files (supports PyInstaller and development). """
    try:
        # PyInstaller places files in a temporary folder (_MEIPASS)
        base_path = sys._MEIPASS
    except AttributeError:
        # Development mode
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)