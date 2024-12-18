import base64
import os
import sys
import requests
import socket
from io import BytesIO
from PIL import Image, ImageTk
from PIL._tkinter_finder import tk

import cache


def check_internet_connection():
    """
    Überprüft, ob eine Internetverbindung besteht, indem versucht wird, eine Verbindung zu einem öffentlichen DNS-Server herzustellen.

    :return: True, wenn eine Verbindung zum Internet besteht, andernfalls False.
    :rtype: bool
    """
    try:
        # Versuchen, eine Verbindung zu einem bekannten öffentlichen DNS-Server herzustellen (Google DNS).
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except (socket.timeout, socket.error):
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
    print("DEBUG: load_image_from_url: ", url, "")
    if not check_internet_connection():
        img_data = base64.b64decode(cache.user_default_avatar)
        img = Image.open(BytesIO(img_data))
        print("DEBUG: img: ", img, "")
        return Image.open(default) if default else img

    response = requests.get(url)
    response.raise_for_status()  # Überprüft, ob die Anfrage erfolgreich war
    img_data = BytesIO(response.content)  # Bilddaten in einen BytesIO-Stream laden
    print("DEBUG: img_data: ", img_data, "")
    return Image.open(img_data)


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
    print("DEBUG: load_image_from_base64: ", base64_string, "")
    img_data = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_data))
    print("DEBUG: img: ", img, "")
    return img


def loadImage(parent, image: str = None, defult_image = None, width: int = 48, height: int = 48):
    if image is None:
        image = cache.user_avatar
    if image.startswith("http"):
        try:
            img = load_image_from_url(image, defult_image)

            # Bild skalieren (z. B. auf 128x128 Pixel)
            img = img.resize((width, height))

            parent.img_tk = ImageTk.PhotoImage(img)
            return parent.img_tk
        except (requests.HTTPError, ConnectionError) as e:
            print(f"Fehler beim Laden des Bildes von der URL: {e}")
            # Hier können Sie eine Standardaktion oder ein Ersatzbild ausführen
            img = load_image_from_base64(cache.user_avatar)

            # Bild skalieren (z. B. auf 128x128 Pixel)
            img = img.resize((width, height))

            parent.img_tk = ImageTk.PhotoImage(img)
            return parent.img_tk
    else:
        img = load_image_from_base64(image)

        # Bild skalieren (z. B. auf 128x128 Pixel)
        img = img.resize((width, height))

        parent.img_tk = ImageTk.PhotoImage(img)
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