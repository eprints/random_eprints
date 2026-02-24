import argparse
import io
import random
from operator import indexOf

# from .random_text import RandomText

from fpdf import FPDF

# pdf = FPDF()
# pdf.add_page()
# pdf.set_font('helvetica', size=12)
# pdf.cell(text="hello world")
# pdf.output("hello_world.pdf")
import hashlib
import random
import os
from PIL import Image
from datetime import datetime, timedelta
import base64

dirname = os.path.dirname(__file__)

from random_text import RandomText

class Subjects:

    def __init__(self, subjects_file_path="/opt/eprints3/archives/clocks/cfg/subjects"):
        self.subjects_loc = []
        self.subjects_loc_lookup = {}
        self.subjects_divisions = []
        self.divisions_ids = []
        self.divisions_lookup = {}
        # self.subjects = []
        self.subject_ids = []
        with open(subjects_file_path) as subjects_file:
            lines = [line for line in subjects_file.readlines()]
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if len(line) == 0:
                    continue
                if line[0].islower():
                    (id, text, p, d) = line.split(":")
                    self.subjects_divisions.append(line)
                    self.divisions_ids.append(id)
                    self.divisions_lookup[id] = text
                if line[0].isupper():
                    self.subjects_loc.append(line)
                    (id, text, p, d) = line.split(":")
                    subject = text.replace(f"{id} ", "")
                    self.subjects_loc_lookup[id] = subject
                    # self.subjects.append(subject)
                    self.subject_ids.append(id)


    def get_random_subject(self):
        id = random.choice(self.subject_ids)
        division_id = random.choice(self.divisions_ids)
        return {
            "id": id,
            "subject": self.subjects_loc_lookup[id],
            "division_id": division_id,
            "division": self.divisions_lookup[division_id]
        }
        return random.choice(self.subjects)
    # def get_division(self, subject):
    #     return random.choice(self.subjects_divisions)


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

class RandomImage:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        #https://stackoverflow.com/a/3207973
        self.images = [os.path.join(self.folder_path, image) for image in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, image))]

    def get_random_image_path(self):
        return random.choice(self.images)

class RandomEPrint:

    def __init__(self, textgenerator, subjects, namegen, imagegen, pdfs=1, image_count=1, contributions=True,
                 wordcount= 100, author_count=3, eprint_id=1, include_docs=True):
        self.textgenerator =textgenerator
        self.subjects = subjects
        self.pdfs = pdfs
        self.imagegen = imagegen
        self.image_count = image_count
        #3.5 style contributions if true, else 3.4 style creators
        self.contributions = contributions
        self.wordcount = wordcount
        self.words = ""
        self.author_count = author_count
        self.namegen = namegen
        self.eprint_id = eprint_id
        self.include_docs = include_docs
        self.generate()

    def get_pdf(self, title, text, authors, image_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica', size=12)
        full_text=f"""{title}

by {', '.join(authors)}

{text}
"""
        # pdf.multi_cell(w=pdf.epw/2, text=title)
        # pdf.multi_cell(w=pdf.epw/2,text=f"by {', '.join(authors)}")
        # pdf.multi_cell(w=pdf.epw/2,text=text)

        image = Image.open(image_path)
        image.thumbnail((300,300), Image.Resampling.LANCZOS)

        pdf.image(image, x=pdf.epw * 0.6, y=10, keep_aspect_ratio=True, w=pdf.epw / 3)
        pdf.multi_cell(w=pdf.epw/2, text=full_text)
        # pdf.image(image_path, x=pdf.epw*0.75,y=10, keep_aspect_ratio=True,w=pdf.epw/4)
        # pdf.output("test.pdf")
        return pdf

    def generate(self):

        self.words = " ".join(self.textgenerator.get_words(self.wordcount))

        self.subject_info = self.subjects.get_random_subject()
        self.subject = self.subject_info["id"]
        self.division = self.subject_info["division_id"]
        self.publication = f"Journal of {self.subject_info['division']}"
        self.volume = random.randint(1,10)
        self.number = random.randint(1,4)

        min_date = datetime(1950, month=1, day=1)
        now = datetime.now()
        self.nowstring = now.strftime("%Y-%m-%d %H:%M:%S")
        self.date = min_date + (now - min_date) * random.random()
        self.authors = []
        for i in range(self.author_count):
            self.authors.append(self.namegen.get_name())

        if not "." in self.words:
            #make sure there's at least one sentance
            self.words += "."

        # up to the first full stop
        self.title = self.words[:self.words.index(".")]
        self.abstract = self.title
        self.image_path = self.imagegen.get_random_image_path()

        pdf = self.get_pdf(self.title, self.words, self.authors, self.image_path)

        pdf_bytes = pdf.output()
        # hash = hashlib.md5(pdf_bytes)
        md5_hasher = hashlib.md5()
        md5_hasher.update(pdf_bytes)
        self.pdf_hash = md5_hasher.hexdigest()
        self.pdf_size = len(pdf_bytes)
        self.pdf_base64 = base64.b64encode(pdf_bytes).decode()
        self.doc_id=1



    def get_xml(self):

        xml = f"""<eprint id='http://example.eprints-hosting.org/id/eprint/1'>
    <eprintid>{self.eprint_id}</eprintid>
    <rev_number>1</rev_number>
    <documents>
"""
        if self.include_docs:
            xml +=f"""<document id='http://example.eprints-hosting.org/id/document/1'>
        <docid>{self.eprint_id}</docid>
        <rev_number>1</rev_number>
        <files>
          <file id='http://example.eprints-hosting.org/id/file/$n'>
            <fileid>{self.eprint_id}</fileid>
            <datasetid>document</datasetid>
            <objectid>{self.eprint_id}</objectid>
            <filename>document{self.eprint_id}.pdf</filename>
            <mime_type>application/pdf</mime_type>
            <hash>$md5</hash>
            <hash_type>MD5</hash_type>
            <filesize>{self.pdf_size}</filesize>
            <mtime>{self.nowstring}</mtime>
            <url>http://example.eprints-hosting.org/id/eprint/$n/1/$name.pdf</url>
            <data encoding='base64'>{self.pdf_base64}</data>
          </file>
        </files>
        <eprintid>{self.eprint_id}</eprintid>
        <pos>{1}</pos>
        <placement>1</placement>
        <mime_type>application/pdf</mime_type>
        <format>text</format>
        <language>en</language>
        <security>public</security>
        <main>document{self.eprint_id}.pdf</main>
      </document>
"""

        xml += f"""</documents>
    <eprint_status>archive</eprint_status>
    <userid>1</userid>
    <dir>documents/disk0/00/00/00/01</dir>
    <datestamp>{self.nowstring}</datestamp>
    <date>{self.date.year}</date>
    <lastmod>{self.nowstring}</lastmod>
    <status_changed>{self.nowstring}</status_changed>
    <type>article</type>
    <metadata_visibility>show</metadata_visibility>
"""
        if self.contributions:
            xml += "    <contributions>"
            for author in self.authors:
                given, family = author.split(" ")
                xml += f"""<item>
                <type>http://www.loc.gov/loc.terms/relators/AUT</type>
                   <contributor>
                        <datasetid>person</datasetid>
                        <name>{family}, {given}</name>
                    </contributor>
                 </item>"""
            xml += "    </contributions>"

        else:
            xml+="    <creators>"
            for author in self.authors:
                given, family = author.split(" ")
                email = f"{given}.{family}@example.ac.uk"
                xml+=f"""<item>
        <name>
          <family>{family}</family>
          <given>${given}</given>
        </name>
        <id>{email}</id>
      </item>"""
            xml += "    </creators>"

        xml +=f"""<title>{self.title}</title>
    <ispublished>pub</ispublished>
    <subjects>
      <item>{self.subject}</item>
    </subjects>
    <divisions>
      <item>{self.division}</item>
    </divisions>
    <abstract>{self.abstract}</abstract>
    <publication>{self.publication}</publication>
    <volume>{self.volume}</volume>
    <number>{self.number}</number>
    <refereed>TRUE</refereed>
  </eprint>"""

        return xml

def parse_args_random_eprints():
    parser = argparse.ArgumentParser(description="Generate random EPrints with images and/or PDFs")
    # type=str
    parser.add_argument('-n', '--records', type=int, help="Number of records", default=10)
    parser.add_argument('-c', '--creatorcount', type=int, help="Size of creator name pool", default=5)
    parser.add_argument('-i', '--imagecount', type=int, help="Max images per record", default=1)
    parser.add_argument('-p', '--pdfcount', type=int, help="Max PDFS per record", default=1)
    parser.add_argument('-d', '--docs', help="Include documents", action='store_true')
    parser.add_argument('-s', '--subjects', type=str, help="subjects file path", default='/opt/eprints3/flavours/pub_lib/defaultcfg/subjects')
    parser.add_argument('-t', '--textfile', type=str, help="path to text file for data", default=os.path.join(dirname,'book.txt'))
    parser.add_argument('-f', '--tofile', type=str, help="produce file rather than stdout",)

    return parser.parse_args()

if __name__ == "__main__":
    #random.seed(1)
    args = parse_args_random_eprints()

    subjects = Subjects(args.subjects)

    textgen = RandomText(args.textfile)

    namegen = RandomName()
    imagegen = RandomImage(os.path.join(dirname,"images"))

    final_xml = f"""<?xml version='1.0' encoding='utf-8'?>
    <eprints xmlns='http://eprints.org/ep2/data/2.0'>"""

    eprints = []
    for i in range(args.records):
        eprint = RandomEPrint(textgen, subjects, namegen, imagegen)

        eprints.append(eprint)
        final_xml += eprint.get_xml()



    final_xml += "</eprints>"
    if args.tofile:
        with open(args.tofile, "w") as file:
            file.write(final_xml)
    else:
        print(final_xml)
