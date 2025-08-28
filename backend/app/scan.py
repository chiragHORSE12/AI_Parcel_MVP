from pyzbar.pyzbar import decode
from PIL import Image
import os, json

def decode_image(path):
    img = Image.open(path).convert('RGB')
    decoded = decode(img)
    results = []
    for d in decoded:
        res = {
            "data": d.data.decode('utf-8', errors='ignore'),
            "type": d.type,
            "rect": {"left": d.rect.left, "top": d.rect.top, "width": d.rect.width, "height": d.rect.height}
        }
        results.append(res)
    # If nothing decoded, return empty list and a message
    if not results:
        return {"decoded": [], "message": "no barcodes/QR detected (this is normal for demo images)"}
    return {"decoded": results}
