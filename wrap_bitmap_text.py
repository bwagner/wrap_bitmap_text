#!/usr/bin/env python

# TODO:
# - add help output to README.md

import os
import sys
from collections import Counter

import typer
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
    text_wrapped = ""
    for line in lines:
        x_offset = 0  # new line, start flush left
        for b in line:
            (x, y, w, h, t) = bbs[b]  # get bounding box of current word
            im = img.crop((x, y, x + w, y + h))
            new_im.paste(im, (x_offset, y_offset))
            x_offset += w + inter_word_space
            text_wrapped += f"{t} "
        y_offset += max_height + inter_line_space
        text_wrapped += "\n"

    base_name, ext = os.path.splitext(os.path.basename(img_path))

    target = f"{base_name}_stacked{ext}"
    new_im.save(target)
    return target, text, text_wrapped


def custom_help_check():
    if "-h" in sys.argv or "-?" in sys.argv:
        sys.argv[1] = "--help"


def main(
    file_path: str = typer.Argument(
        ..., help="Path to the image file", show_default=False
    ),
    width: int = typer.Argument(
        ..., help="Max width for the resulting lines in pixels", show_default=False
    ),
    open_img: bool = typer.Option(
        False, "--open-image", "-i", help="Open image after creation"
    ),
    output_txt: bool = typer.Option(
        False, "--output-txt", "-t", help="Output OCR'd text on stdout"
    ),
):
    target, text, text_wrapped = text_wrap(file_path, width)
    typer.echo(f"created: {target}.")
    if output_txt:
        typer.echo(f"found text: '{text}'.")
        typer.echo(f"wrapped:\n{text_wrapped}")
    if open_img:
        os.system(f"open {target}")


if __name__ == "__main__":
    custom_help_check()
    typer.run(main)
