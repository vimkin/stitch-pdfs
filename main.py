import argparse
from pathlib import Path
import PyPDF2
import logging

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(
    description="Stitch odd and reversed even pages of a pdf together"
)

parser.add_argument("--output", type=str, help="Output pdf file")
parser.add_argument(
    "--odd",
    type=str,
    help="This pdf starts with first page of your doc and contains only odd pages",
)
parser.add_argument(
    "--even",
    type=str,
    help="This pdf starts with the last page of your doc and contains only even pages",
)

args = parser.parse_args()

with open(Path(args.odd).resolve(), "rb") as file_odd, open(
    Path(args.even).resolve(), "rb"
) as file_even:
    reader_odd = PyPDF2.PdfReader(file_odd)
    reader_even = PyPDF2.PdfReader(file_even)
    reader_odd_pages = len(reader_odd.pages)
    reader_even_pages = len(reader_even.pages)

    if reader_odd_pages != reader_even_pages:
        logging.error("Number of pages in odd and even files should be equal")
        exit(1)

    i = 0
    j = reader_even_pages - 1
    writer = PyPDF2.PdfWriter()

    while i < reader_odd_pages:
        writer.add_page(reader_odd.pages[i])
        writer.add_page(reader_even.pages[j])
        i += 1
        j -= 1

    with open(Path(args.output).resolve(), "wb") as output_file:
        writer.write(output_file)
        logging.info(f"Output file is saved at {output_file}")
