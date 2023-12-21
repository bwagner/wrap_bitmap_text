# Wrap Bitmap Text

A crude implementation of text break for a text in a bitmap.

Tested with python 3.11.7.

## Uses
- cv2
- pytesseract
- Pillow

## Consists of Modules
- `arrange_bb.py`:
  Arranges bounding boxes flush left according to given max. width.
- `bb.py`:
  Finds bounding boxes of words of text found in given image.
- `wrap_bitmap_text.py`:
  Glues everything together to provide the functionality.

## Example
![image](https://github.com/bwagner/wrap_bitmap_text/assets/447049/a1d54dd0-07e8-49f3-8b70-0fbea8be2aaf)

`./wrap_bitmap_text.py chrome.png 200`

outputs:

```console
created: chrome_stacked.png .
found text: 'To get future Google Chrome updates, you'll need macOS 10.15 or later. This computer is using macOS 10.14.'.
```

and generates:

![chrome_stacked](https://github.com/bwagner/wrap_bitmap_text/assets/447049/f6308ca8-baea-4e13-91a6-254b87326d57)

## Contributing
```console
git clone https://github.com/bwagner/wrap_bitmap_text/blob/main/README.md
cd wrap_bitmap_text
pip install -r requirements.txt -r dev-requirements.txt
pre-commit install
```

## Todo
- inter word space is currently an arbitrary choice, should be calculated, e.g.
  from the distance between adjacent bounding boxes.
