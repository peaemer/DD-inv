import base64
from io import BytesIO

import requests
from PIL import Image, ImageTk

import cache


def load_image_from_url(url):
    """Lädt ein Bild von einer URL."""
    response = requests.get(url)
    response.raise_for_status()  # Überprüft, ob die Anfrage erfolgreich war
    img_data = BytesIO(response.content)  # Bilddaten in einen BytesIO-Stream laden
    return Image.open(img_data)


def load_image_from_base64(base64_string):
    """Lädt ein Bild aus einem Base64-String."""
    img_data = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_data))
    return img

def loadImage(parent, img=None, width:int=128, height:int=128):
    if img is None:
        img = cache.user_avatar
    if img.startswith("http"):
        img = load_image_from_url(img)

        img = img.resize((width, height))

        parent.img_tk = ImageTk.PhotoImage(img)
        return parent.img_tk
    else:
        # Bild aus Base64-String laden und anzeigen
        img = load_image_from_base64(img)

        # Bild skalieren (z. B. auf 100x100 Pixel)
        img = img.resize((width, height))

        parent.img_tk = ImageTk.PhotoImage(img)
        return parent.img_tk