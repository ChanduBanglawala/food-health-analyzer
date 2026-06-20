from pyzbar.pyzbar import decode
import cv2


def scan_barcode(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return None

    barcodes = decode(image)

    for barcode in barcodes:
        return barcode.data.decode("utf-8")

    return None