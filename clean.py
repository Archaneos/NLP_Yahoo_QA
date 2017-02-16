import csv
# import sklearn
import nltk
import re
from nltk.corpus import stopwords

TOKENS = {"NOUN": "<NOUN>", "URL": "<URL>"}


def tokenize(string):
    return string.split(" ") if string != "" else []


def clean_str(string):
    """
    Data cleaning. Remove unknown char and space words.
    Remove english most common abreviations.
    TODO: improve the 'd 
    """

    string = re.sub(r"[^A-Za-z0-9(),!?\'\`<>]", " ", string)
    string = re.sub(r"\'ve", " have", string)
    string = re.sub(r"he\'s", " he is", string)
    string = re.sub(r"she\'s", " she is", string)
    string = re.sub(r"n\'t", " not", string)
    string = re.sub(r"\'re", " are", string)
    string = re.sub(r"\'d", " d", string)
    string = re.sub(r"\'ll", " will", string)
    string = re.sub(r"\'m", " am", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"\(", " ( ", string)
    string = re.sub(r"\)", " ) ", string)
    string = re.sub(r"\?", " ? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip()


def remove_url(string):
    s = []
    for x in string.split(" "):
        if x.startswith("http"):
            s.append(TOKENS["URL"])
        else:
            s.append(x)
    return " ".join(s)


def remove_proper_noun(string):

    tok2 = nltk.tokenize.word_tokenize(string)

    tok = tokenize(string)
    pos = nltk.pos_tag(tok)

    s = []
    for (word, tag) in pos2:
        if tag == "NNP" or tag == "NNPS":
            print word

    for (word, tag) in pos:
        if (tag == "NNP" or tag == "NNPS") and word not in TOKENS.values():
            s.append(TOKENS["NOUN"])
        else:
            s.append(word)

    return " ".join(s)


def remove_stopword(string):
    stop_word_list = set(stopwords.words("english"))
    tok = tokenize(string)
    stopless_tok = [x for x in tok if x not in stop_word_list]
    return ' '.join(stopless_tok)


outFile = open("clean_manner_print.csv", "w")
columns = ["uri", "subject", "content", "bestanswer"]
for i in range(10):
    columns.append(''.join(["answer_item", str(i)]))

outFileWrite = csv.DictWriter(outFile, columns, extrasaction="ignore")
outFileWrite.writeheader()

with open("manner_print.csv") as file:
    csvfile = csv.DictReader(file)
    data = dict()

    for row in csvfile:
        data["uri"] = row["uri"]

        for field in columns[1:]:
            s = row[field].lower()
            s = remove_url(s)
            s = clean_str(s)
            s = remove_proper_noun(s)
            # s = remove_stopword(s)
            data[field] = s
        # data["uri"] = row["uri"]
        # data["subject"] = clean_str(row["subject"])
        # data["content"] = clean_str(row["content"])
        # data["bestanswer"] = clean_str(row["bestanswer"])

        # for i in range(9):
        #     data["answer_item" + str(i)] = clean_str(row[4 + i])

        outFileWrite.writerow(data)

outFile.flush()
outFile.close()
