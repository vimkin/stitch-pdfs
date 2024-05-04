# PDF Page Stitcher

CLI utility to stitch odd and reversed even pages of a PDF together. It uses the PyPDF2 library to manipulate PDF files.

## Usage
```
usage: main.py [-h] [-o OUTPUT] [--odd ODD] [--even EVEN]

Stitch odd and reversed even pages of a pdf together

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output pdf file
  --odd ODD             This pdf starts with first page of your doc and contains only odd pages
  --even EVEN           This pdf starts with the last page of your doc and contains only even pages

Example:
    python3 main.py --output output.pdf --odd pages-odd.pdf --even pages-even.pdf
```
