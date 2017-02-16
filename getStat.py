import csv
import string
import sys
import argparse


def count_punctuation(csv_row, csvfield):
    return len(list(filter(lambda c: c in csv_row[csvfield], string.punctuation)))


def get_nb_char(csv_row, csvfield):
    return len(csv_row[csvfield])


def get_nb_words(csv_row, csvfield):
    return len(csv_row[csvfield].split())

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-i", action="store")
    parser.add_argument("--fields", "-f", nargs="+")

    args = parser.parse_args(sys.argv[1:])

    print "Filename: ", args.file
    print "Fields to analyze: ",args.fields

    f = open(args.file)
    csvfile = csv.DictReader(f)

    if len(csvfile.fieldnames) < len(args.fields):
        print "Too many fields compare to CSV header"
        exit()

    for x in args.fields:
        if x not in csvfile.fieldnames:
            print "{} does not exist in the CSV Header.".format(x)
            print csvfile.fieldnames
            exit()

    length = 0

    resultChar = dict()
    resultWord = dict()
    resultPunct = dict()

    for field in args.fields:
        resultChar[field] = 0
        resultWord[field] = 0
        resultPunct[field] = 0

    for row in csvfile:
        # print row
        for field in args.fields:
            resultChar[field] += get_nb_char(row, field)
            resultWord[field] += get_nb_words(row, field)
            resultPunct[field] += count_punctuation(row, field)

        length += 1

    for key in resultChar:
        resultChar[key] /= float(length)
        resultWord[key] /= float(length)
        resultPunct[key] /= float(length)

    print "Avg Char/Line:"
    for field in args.fields:
        print "  {:<15} {} ".format(field, resultChar[field])

    print "==========="
    print "Avg Word/Line:"
    for field in args.fields:
        print "  {:<15} {} ".format(field, resultWord[field])

    print "==========="
    print "Avg Punct/Line:"
    for field in args.fields:
        print "  {:<15} {} ".format(field, resultPunct[field])

    f.close()
