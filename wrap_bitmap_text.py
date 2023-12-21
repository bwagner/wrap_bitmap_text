#!/usr/bin/env python

import os
import sys
from collections import Counter

from PIL import Image

import arrange_bb
import bb

"""
wrap_bitmap_text:

Crude implementation of text break for a text in a bitmap.

bb.get_bbs(filename)
-> gets list of bounding boxes of words in bitmap

arrange_bb.arrange_bounding_boxes(bounding_boxes: list[(int, int, int, int)], max_width: int) -> list[list[int]]:
-> takes a list of bounding boxes and a max_width and creates a list of list of indices. Every top-level-list
   is a line in the final output. The indices in a line point to that bounding_box in the input list.
"""


def get_bg_col(img):
    colors = img.getdata()
    color_counts = Counter(colors)
    background_color, _ = color_counts.most_common(1)[0]
    return background_color


def text_wrap(img_path, max_width):
    img = Image.open(img_path)
    width, height = img.size
    background_color = get_bg_col(img)

    _, bbs, text = bb.get_bbs(img_path)
    max_height = max(bbs, key=lambda x: x[3])[3]

    lines = arrange_bb.arrange_bounding_boxes(bbs, max_width)
    max_words = len(max(lines, key=len))

    inter_word_space = 10
    inter_line_space = 0

    new_im = Image.new(
        "RGB",
        (max_width + inter_word_space * max_words, max_height * len(lines)),
        background_color,
    )

    y_offset = 0
    for line in lines:
        x_offset = 0  # new line, start flush left
        for b in line:
            (x, y, w, h) = bbs[b]  # get bounding box of current word
            im = img.crop((x, y, x + w, y + h))  # crop word
            new_im.paste(im, (x_offset, y_offset))  # paste word
            x_offset += w + inter_word_space  # update x-offset
        y_offset += max_height + inter_line_space  # update y-offset

    base_name, ext = os.path.splitext(os.path.basename(img_path))

    target = f"{base_name}_stacked.jpg"
    new_im.save(target)
    return target, text


if __name__ == "__main__":
    target, text = text_wrap(sys.argv[1], int(sys.argv[2]))
    print(f"created: {target} .")
    print(f"found text: '{text}'.")
    os.system(f"open {target}")
