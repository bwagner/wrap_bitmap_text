#!/usr/bin/env python

import pathlib
from enum import Enum
from typing import Optional

import cv2
import pytesseract
from pytesseract import Output

if __name__ == "__main__":
    import os
    import sys

HeightType = Enum("HeightType", "MAX_HEIGHT MIN_HEIGHT MAX_ENCLOSING_HEIGHT".split())


def get_bbs(
    filename: str,
    create_visualization: bool = False,
    height_type: HeightType = HeightType.MAX_ENCLOSING_HEIGHT,
) -> tuple[Optional[str], list[(int, int, int, int)]]:
    """
    Finds the bounding boxes of words in an image. Optionally copies the image
    and superimposes the found bounding boxes.
    Returns a tuple of:
    1. The filename of the generated superimposition image, or None if none requested.
    2. A list of x, y, w, h- tuples for the found bounding boxes.
    height_type lets you choose between 3 strategies for determining the height of the generated lines:
    1. MAX_HEIGHT: equals the height of the original image
    2. MIN_HEIGHT: each bounding box defines its own hight.
    3. MAX_ENCLOSING_HEIGHT: The tallest bounding box determines the height for all
    """
    img = cv2.imread(filename)
    height, width, channel = img.shape

    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    text = " ".join(d["text"]).strip()
    n_boxes: int = len(d["level"])
    bbs: list[(int, int, int, int)] = []
    min_y = 10_000
    max_h = -10_000
    for i in range(n_boxes):
        (x, y, w, h, t) = (
            d["left"][i],
            d["top"][i],
            d["width"][i],
            d["height"][i],
            d["text"][i],
        )
        if w < width / 3:
            if y < min_y:
                min_y = y
            if h > max_h:
                max_h = h
            if height_type == HeightType.MAX_HEIGHT:
                y = 0
                h = height
            bbs.append((x, y, w, h, t))

    if height_type == HeightType.MAX_ENCLOSING_HEIGHT:
        bbs2 = []
        for b in bbs:
            b2 = list(b)
            b2[1] = min_y
            b2[3] = max_h
            bbs2.append(b2)
        bbs = bbs2

    if create_visualization:
        for x, y, w, h, _ in bbs:
            cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

    if create_visualization:
        orig = pathlib.Path(filename)
        bb = f"{orig.stem}_bb{orig.suffix}"
        cv2.imwrite(bb, img)
    else:
        bb = None
    return bb, bbs, text


def main():
    filename = sys.argv[1]
    bb, bbs, text = get_bbs(filename, True, HeightType.MAX_ENCLOSING_HEIGHT)
    print(f"created {bb}")
    print(f"bounding boxes: {bbs}")
    print(f"found text: {text}")
    os.system(f"open {bb}")


if __name__ == "__main__":
    main()
