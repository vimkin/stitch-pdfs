import os
import unittest
import subprocess
from pathlib import Path
import logging
import PyPDF2

logging.basicConfig(level=logging.DEBUG)
OUTPUT_FILE_NAME = "test_stitch_pdfs_output.pdf"


class TestMain(unittest.TestCase):
    current_dir = None

    def setUp(self):
        self.current_dir = Path(__file__).resolve().parent
        self.output_file = Path(self.current_dir, OUTPUT_FILE_NAME)

    def tearDown(self):
        os.remove(self.output_file)

    def testStitchPdfs(self):
        cmd = [
            "python3",
            "main.py",
            "--output",
            self.output_file.resolve(),
            "--odd",
            Path(self.current_dir, "test_data/pages-odd.pdf").resolve(),
            "--even",
            Path(self.current_dir, "test_data/pages-even.pdf").resolve(),
        ]

        subprocess.run(cmd)

        reader_output = PyPDF2.PdfReader(self.output_file.open("rb"))

        self.assertEqual(len(reader_output.pages), 6)

        page_texts_correct = ["1", "2", "3", "4", "5", "6"]
        page_texts_actual = [page.extract_text() for page in reader_output.pages]

        self.assertEqual(page_texts_correct, page_texts_actual)


if __name__ == "__main__":
    unittest.main()
