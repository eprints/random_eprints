import argparse

from .random_text import RandomText

from fpdf import FPDF

# pdf = FPDF()
# pdf.add_page()
# pdf.set_font('helvetica', size=12)
# pdf.cell(text="hello world")
# pdf.output("hello_world.pdf")

class RandomEPrint:

    def __init__(self, textgenerator, pdfs=1, images=1, contributions=True):
        self.textgenerator =textgenerator
        self.pdfs = pdfs
        self.images = images
        #3.5 style contributions if true, else 3.4 style creators
        self.contributions = contributions

def parse_args_random_eprints():
    parser = argparse.ArgumentParser(description="Generate random EPrints with images and/or PDFs")
    # type=str
    parser.add_argument('-n', '--records', type=int, help="Number of records", default=10)
    parser.add_argument('-c', '--creatorcount', type=int, help="Size of creator name pool", default=5)
    parser.add_argument('-i', '--imagecount', type=int, help="Max images per record", default=1)
    parser.add_argument('-p', '--pdfcount', type=int, help="Max PDFS per record", default=1)
    parser.add_argument('-d', '--docs', type=bool, help="Include documents", action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args_random_eprints()