import argparse
import random
from operator import indexOf

# from .random_text import RandomText

from fpdf import FPDF

# pdf = FPDF()
# pdf.add_page()
# pdf.set_font('helvetica', size=12)
# pdf.cell(text="hello world")
# pdf.output("hello_world.pdf")

import random
from datetime import datetime, timedelta

from random_text import RandomText

class Subjects:

    def __init__(self, subjects_file_path="/opt/eprints3/archives/clocks/cfg/subjects"):
        self.subjects_loc = []
        self.subjects_loc_lookup = {}
        self.subjects_divisions = []
        with open(subjects_file_path) as subjects_file:
            lines = [line for line in subjects_file.readlines()]
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if len(line) == 0:
                    continue
                if line[0].islower():
                    self.subjects_divisions.append(line)
                if line[0].isupper():
                    self.subjects_loc.append(line)
                    (id, text, p, d) = line.split(":")
                    self.subjects_loc_lookup[id] = text.replace(f"{id} ", "")


class RandomName:
    def __init__(self):
        self.all_names = []
        firstnames = ["given_names_male", "given_names_female"]
        for filename in firstnames:
            with open(filename) as namesfile:
                names = [name.strip() for name in namesfile.readlines()]
                self.all_names += names
        with open("surnames") as namesfile:
            self.surnames = [name.strip() for name in namesfile.readlines()]

    def get_name(self):
        name = random.choice(self.all_names) + " " + random.choice(self.surnames)
        #make lowercase than capitalise each word
        name = name.lower().title()
        return name

class RandomEPrint:

    def __init__(self, textgenerator, subjects, namegen, pdfs=1, images=1, contributions=True, wordcount= 100, author_count=3):
        self.textgenerator =textgenerator
        self.subjects = subjects
        self.pdfs = pdfs
        self.images = images
        #3.5 style contributions if true, else 3.4 style creators
        self.contributions = contributions
        self.wordcount = wordcount
        self.words = ""
        self.author_count = author_count
        self.namegen = namegen
        self.generate()


    def generate(self):

        self.words = " ".join(self.textgenerator.get_words(self.wordcount))

        min_date = datetime(1950, month=1, day=1)
        now = datetime.now()
        self.date = min_date + (now - min_date) * random.random()
        self.authors = []
        for i in range(self.author_count):
            self.authors.append(self.namegen.get_name())

        if not "." in self.words:
            #make sure there's at least one sentance
            self.words += "."
        # print(self.date)
        print(self.authors)

        # up to the first full stop
        self.title = self.words[:self.words.index(".")]






def parse_args_random_eprints():
    parser = argparse.ArgumentParser(description="Generate random EPrints with images and/or PDFs")
    # type=str
    parser.add_argument('-n', '--records', type=int, help="Number of records", default=10)
    parser.add_argument('-c', '--creatorcount', type=int, help="Size of creator name pool", default=5)
    parser.add_argument('-i', '--imagecount', type=int, help="Max images per record", default=1)
    parser.add_argument('-p', '--pdfcount', type=int, help="Max PDFS per record", default=1)
    parser.add_argument('-d', '--docs', help="Include documents", action='store_true')
    parser.add_argument('-s', '--subjects', type=str, help="subjects file path", default='/opt/eprints3/archives/clocks/cfg/subjects')
    parser.add_argument('-t', '--textfile', type=str, help="path to text file for data", default='book.txt')

    return parser.parse_args()

if __name__ == "__main__":
    #random.seed(1)
    args = parse_args_random_eprints()

    subjects = Subjects(args.subjects)

    textgen = RandomText(args.textfile)

    namegen = RandomName()

    for i in range(args.records):
        eprint = RandomEPrint(textgen, subjects, namegen)

        print(eprint)

    # print (subjects.subjects_loc_lookup)
