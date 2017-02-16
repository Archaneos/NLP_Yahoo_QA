import string
import sys
import codecs
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", action="store")
    parser.add_argument("--output", "-o", action="store")

    args = parser.parse_args(sys.argv[1:])

    fin = codecs.open(args.input, "r")
    fout = open(args.output, "w")
    printable = set(string.printable)

    for line in fin:
        fout.write(''.join(filter(lambda x: x in printable, line)))

    fin.close()
    fout.flush()
    fout.close()
