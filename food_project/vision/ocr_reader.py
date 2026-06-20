"""
ocr_reader.py

Advanced OCR extraction for food packaging.
"""

import cv2
import easyocr
import numpy as np
import re


class OCRReader:

    def __init__(self):

        print("Loading EasyOCR...")

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

    # --------------------------------------------------
    # IMAGE PREPROCESSING
    # --------------------------------------------------

    def preprocess(self, image):

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        return [
            image,
            gray,
            thresh
        ]

    # --------------------------------------------------
    # ROTATION SUPPORT
    # --------------------------------------------------

    def rotate_image(
        self,
        image,
        angle
    ):

        if angle == 90:
            return cv2.rotate(
                image,
                cv2.ROTATE_90_CLOCKWISE
            )

        elif angle == 180:
            return cv2.rotate(
                image,
                cv2.ROTATE_180
            )

        elif angle == 270:
            return cv2.rotate(
                image,
                cv2.ROTATE_90_COUNTERCLOCKWISE
            )

        return image

    # --------------------------------------------------
    # TEXT CLEANING
    # --------------------------------------------------

    def clean_text(
        self,
        text
    ):

        text = text.lower()

        text = re.sub(
            r"[^a-zA-Z0-9\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # --------------------------------------------------
    # OCR EXTRACTION
    # --------------------------------------------------

    def extract_text(
        self,
        image_path
    ):

        try:

            image = cv2.imread(
                image_path
            )

            if image is None:
                print(
                    f"Could not load image: {image_path}"
                )
                return ""

            all_text = []

            for angle in [0, 90, 180, 270]:

                rotated = self.rotate_image(
                    image,
                    angle
                )

                versions = self.preprocess(
                    rotated
                )

                for img in versions:

                    results = self.reader.readtext(
                        img,
                        detail=1,
                        paragraph=False,
                        width_ths=0.7,
                        height_ths=0.7
                    )

                    for item in results:

                        bbox, text, conf = item

                        if conf < 0.30:
                            continue

                        all_text.append(
                            (
                                bbox,
                                text,
                                conf
                            )
                        )

            if not all_text:
                return ""

            # ----------------------------------------
            # PRIORITIZE LARGE TEXT
            # ----------------------------------------

            scored = []

            for bbox, text, conf in all_text:

                try:

                    width = abs(
                        bbox[1][0] - bbox[0][0]
                    )

                    height = abs(
                        bbox[2][1] - bbox[0][1]
                    )

                    area = width * height

                except:
                    area = 0

                score = area * conf

                scored.append(
                    (
                        score,
                        text
                    )
                )

            scored.sort(
                reverse=True,
                key=lambda x: x[0]
            )

            top_text = []

            seen = set()

            for score, text in scored:

                cleaned = self.clean_text(
                    text
                )

                if len(cleaned) < 2:
                    continue

                if cleaned in seen:
                    continue

                seen.add(cleaned)

                top_text.append(
                    cleaned
                )

            return " ".join(
                top_text[:50]
            )

        except Exception as e:

            print(
                f"OCR Error: {e}"
            )

            return ""

    # --------------------------------------------------
    # KEYWORD EXTRACTION
    # --------------------------------------------------

    def extract_keywords(
        self,
        image_path
    ):

        text = self.extract_text(
            image_path
        )

        words = text.split()

        stop_words = {

            "nutrition",
            "ingredients",
            "energy",
            "fat",
            "protein",
            "sugar",
            "salt",
            "carbohydrate",
            "serving",
            "values",
            "contains",
            "grams",
            "total",
            "daily",
            "value",
            "cholesterol",
            "sodium",
            "fiber",
            "vitamin",
            "calcium",
            "iron",
            "per",
            "food",
            "product"

        }

        keywords = []

        seen = set()

        for word in words:

            if len(word) <= 2:
                continue

            if word in stop_words:
                continue

            if word in seen:
                continue

            seen.add(word)

            keywords.append(
                word
            )

        return keywords[:20]


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    ocr = OCRReader()

    image_path = "sample.jpg"

    text = ocr.extract_text(
        image_path
    )

    print("\nDetected Text:")
    print(text)

    print("\nKeywords:")
    print(
        ocr.extract_keywords(
            image_path
        )
    )