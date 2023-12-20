#!/usr/bin/env python

import pathlib
from typing import Optional

import cv2
import pytesseract
from pytesseract import Output

if __name__ == "__main__":
    import os
    import sys


def get_bbs(filename: str, create_visualization:bool=False) -> tuple[Optional[str], list[(int, int, int, int)]]:
    """
    Finds the bounding boxes of words in an image. Optionally copies the image
    and superimposes the found bounding boxes.
    Returns a tuple of:
    1. The filename of the generated superimposition image, or None if none requested.
    2. A list of x, y, w, h- tuples for the found bounding boxes.
    """
    img = cv2.imread(filename)
    width: int = img.shape[1]

    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes : int= len(d["level"])
    bbs: list[(int, int, int, int)] = []
    for i in range(n_boxes):
        (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
        if w < width / 3:
            bbs.append((x, y, w, h))
            if create_visualization:
                cv2.rectangle(
                    img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2
                )

    if create_visualization:
        orig = pathlib.Path(filename)
        bb = f"{orig.stem}_bb{orig.suffix}"
        cv2.imwrite(bb, img)
    else:
        bb = None
    return bb, bbs


def main():
    filename = sys.argv[1]
    bb, bbs = get_bbs(filename, True)
    print(f"created {bb}")
    print(f"bounding boxes: {bbs}")
    os.system(f"open {bb}")


if __name__ == "__main__":
    main()
