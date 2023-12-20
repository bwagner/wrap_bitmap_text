# Wrap Bitmap Text

A crude implementation of text break for a text in a bitmap.

Tested with python 3.11.7.

## Uses
- cv2
- pytesseract
- Pillow

## Consists of Modules
- arrange_bb.py
  Arranges bounding boxes flush left according to given max. width.
- bb.py
  Finds bounding boxes of words of text found in given image.
- wrap_bitmap_text.py
  Glues everything together to provide the functionality
