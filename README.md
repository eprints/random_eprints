# Random EPrint Generator
Takes in text from provided text file, uses a markov chain to generate text. Selects a random image from images/ and produces a PDF file.

Will spit out XML which can be imported into EPrints to fill a test repository with dummy data.

This is intended as a much faster replacement for Victor.xml, with support for EPrints 3.5. I had the various parts lying around and this puts them all together.

## Usage

Needs python with fpdf2 installed. This is best managed in a virtual environment:

```commandline
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

```
python random_eprints.py -f out.xml
/opt/eprints3/bin/import [ARCHIVEID] --user=[ADMINUSERNAME] archive XML out.xml
```

By default it assumes it's running on the same box as an EPrints install. If it isn't you'll need to provide a subjects file with `-s /path/to/subjects`.

## TODOs

Internally it can support creators or contributors (EPrints 3.4 or 3.5), but there's no command line flag to choose between them.


## Source Material

 - themodernclock.txt - The Modern Clock by Ward L. Goodrich: https://www.gutenberg.org/ebooks/61494
 - 20thousandleagues.txt - Twenty Thousand Leagues under the Sea by Jules Verne: https://www.gutenberg.org/ebooks/164
 - howitworks.txt - How it Works by Archibald Williams https://www.gutenberg.org/ebooks/28553