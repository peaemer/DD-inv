import base64
from io import BytesIO

import PIL.Image
import requests
from PIL import Image, ImageTk

import cache


def load_image_from_url(url):
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
    response = requests.get(url)
    response.raise_for_status()  # Überprüft, ob die Anfrage erfolgreich war
    img_data = BytesIO(response.content)  # Bilddaten in einen BytesIO-Stream laden
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
    img_data = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_data))
    return img


def loadImage(parent, image: str = None, width: int = 48, height: int = 48):
    if image is None:
        image = cache.user_avatar
    if image.startswith("http"):
        img = load_image_from_url(image)

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