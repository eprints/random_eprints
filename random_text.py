import collections, random, sys, textwrap
import re
import argparse
#source: https://benhoyt.com/writings/markov-chain/
#licence "I hereby give you permission to do whatever you want with it."

class RandomText:

    def __init__(self, source_file, max_words=200):
        self.possibles = self.get_possibles(source_file)
        self.max_words = 200

    def fix_line(self, line):
        if line.endswith("- \n"):
            # print(line)
            line = line[:-3]
        # line = re.sub('[\W_]+', '', line)
        if len(line) < 2:
            return ""
        return line

    def get_possibles(self, text_file_path):
        # Build possibles table indexed by pair of prefix words (w1, w2)
        w1 = w2 = ''
        possibles = collections.defaultdict(list)
        with open(text_file_path, encoding='utf-8') as textfile:


            all_text = "".join([self.fix_line(line) for line in textfile])
            # all_text = all_text.replace("- \n", "")
            # all_text= re.sub('[\W_]+', '', all_text)

            for line in all_text.split("\n"):
                for word in line.split():
                    word=word.strip()
                    # word = re.sub(r'[\W_.]+', '', word)
                    word = re.sub(r'[^a-zA-Z0-9 \-\,\.\'"]', '', word)
                    if len(word) == 0 or word.isnumeric():
                        continue
                    possibles[w1, w2].append(word)
                    w1, w2 = w2, word

        # Avoid empty possibles lists at end of input
        possibles[w1, w2].append('')
        possibles[w2, ''].append('')
        return possibles



    def get_words(self, min_words=100, max_words=-1):
        # Generate randomized output (start with a random capitalized prefix)
        # Try and end at a full stop,

        if max_words < 0:
            max_words = self.max_words

        w1, w2 = random.choice([k for k in self.possibles if k[0][:1].isupper()])
        output = [w1, w2]
        # for i in range(words):
        i = 0
        while i < max_words:
            word = random.choice(self.possibles[w1, w2])
            output.append(word)
            w1, w2 = w2, word
            if i > min_words and word.endswith("."):
                break
            i += 1

        return output
        # # Print output wrapped to 70 columns
        # print(textwrap.fill(' '.join(output)))


def parse_args_random_text():
    parser = argparse.ArgumentParser(description="Generate random text with markov chains")
    parser.add_argument('-t', '--textfile', type=str, help="path to text file for data", default='book.txt')
    parser.add_argument('-c', '--wordcount', help="Minimum words to generate", default=50)
    parser.add_argument('-w', '--wordwrap', help="Wordwrap output", action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args_random_text()
    #"C:/Users/lpw1r25/Documents/Tasks/3.5/random_data/themodernclock.txt"
    # possibles = get_possibles(args.textfile)
    # output = get_words(possibles, int(args.wordcount))

    textgen = RandomText(args.textfile)
    output = textgen.get_words(int(args.wordcount), 2*(int(args.wordcount)))

    if args.wordwrap:
        print(textwrap.fill(' '.join(output)))
    else:
        print(' '.join(output))
