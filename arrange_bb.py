#!/usr/bin/env python

import sys

import pytest

import bb


def arrange_bounding_boxes(
    bounding_boxes: list[(int, int, int, int)], max_width: int
) -> list[list[int]]:
    """
    Arrange bounding boxes into lines such that the total width of bounding boxes
    in each line does not exceed max_width.

    Parameters:
    bounding_boxes (list of tuples): List of bounding boxes in (x, y, w, h) format.
    max_width (int): Maximum allowed width for each line.

    Returns:
    list of lists: Each sublist contains indexes of bounding boxes in a line.
    """

    lines: list[list[int]] = []
    current_line = []
    current_width = 0

    for i, (_, _, w, *_) in enumerate(bounding_boxes):
        if current_width + w > max_width:
            # Start a new line
            if current_line:
                lines.append(current_line)
            current_line = [i]
            current_width = w
        else:
            # Add box to the current line
            current_line.append(i)
            current_width += w

    # Add the last line if it's not empty
    if current_line:
        lines.append(current_line)

    return lines


bb_list = [
    (13, 29, 27, 19),
    (49, 30, 38, 23),
    (95, 28, 72, 20),
    (176, 28, 85, 25),
    (270, 28, 93, 20),
    (373, 28, 102, 25),
    (485, 28, 60, 25),
    (556, 28, 57, 20),
    (623, 29, 85, 20),
    (717, 29, 61, 19),
    (788, 34, 24, 14),
    (821, 28, 58, 20),
    (889, 28, 49, 20),
    (948, 30, 115, 23),
    (1072, 28, 17, 20),
    (1099, 28, 62, 25),
    (1171, 29, 85, 20),
    (1265, 29, 69, 19),
]


@pytest.mark.parametrize(
    "inp,exp",
    [
        (
            (
                bb_list,
                400,
            ),
            [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9, 10], [11, 12, 13, 14, 15, 16], [17]],
        ),
        (
            (
                bb_list,
                200,
            ),
            [
                [0, 1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, 10, 11, 12],
                [13, 14, 15],
                [16, 17],
            ],
        ),
    ],
)
def test_mw(inp, exp):
    assert arrange_bounding_boxes(inp[0], inp[1]) == exp


def main():
    img_file = sys.argv[1]
    max_width = int(sys.argv[2])
    _, bounding_boxes = bb.get_bbs(img_file)
    arranged_lines = arrange_bounding_boxes(bounding_boxes, max_width)
    print(arranged_lines)


if __name__ == "__main__":
    main()
