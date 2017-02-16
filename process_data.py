import numpy as np
import tensorflow as tf
import tensorflow.contrib.learn as learn
import re
import csv

tf.flags.DEFINE_integer("min_word_frequency", 5, "Minimum frequency of words in the vocabulary")

tf.flags.DEFINE_integer("max_sentence_len", 160, "Maximum Sentence Length")

tf.flags.DEFINE_string(
        "input_dir", os.path.abspath("./data"),
        "Input directory containing original CSV data files")

tf.flags.DEFINE_string(
        "output_dir", os.path.abspath("./data"),
        "Output directeory for TFRecord files")
                                
FLAGS = tf.flags.FLAGS

TRAIN_PATH = os.path.join(FLAGS.input_dir, "train.csv")
TEST_PATH = os.path.join(FLAGS.input_dir, "test.csv")
VALID_PATH = os.path.join(FLAGS.input_dir, "valid.csv")


def clean_str(string):
    """
    Data cleaning. Remove unknown char and space words
    """

    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def tokenizer_fn(iterator):
    return (x.split(" ") for x in iterator)


def create_csv_iter(filename):
    """
    Return an iterator on a csv file
    """

    with open(filename) as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            yield row


def create_vocab(input_iter, min_frequency):
    """
    Create and returns a VocabularyProcessor object with the vocabulary for the input iterator.
    """

    vocab_processor = learn.preporcessing.VocabularyProcessor(
      FLAGS.max_sentence_len,
      min_frequency=min_frequency,
      tokenizer_fn=tokenizer_fn)
    vocab_processor.fit(input_iter)
    return vocab_processor


def write_vocabulary(vocab_processor, outfile):
    """
    Writes the vocabulary to a file, one word per line.
    """

    vocab_size = len(vocab_processor.vocabulary_)
    with open(outfile, "w") as vocabfile:
        for id in range(vocab_size):
            word = vocab_processor.vocabulary_._reverse_mapping[id]
            vocabfile.write(word+"\n")

    print(" Saved vocabulary to {}".format(outfile))


if __name__ == "__main__":
  
    print "Creating vocabulary..."
    input_iter = create_csv_iter("manner_print.csv")
    input_iter = (x[1]+" "+x[2] for x in input_iter)

    vocab = create_vocab(input_iter, min_frequency=FLAGS.min_word_frequency)

    print("Total vocabulary size: {}".format(len(vocab.vocabulary_)))

    # Write vocab file
    write_vocabulary(vocab, os.path.join(FLAGS.output_dir, "vocabulary.txt"))

    # Save vocab processor
    vocab.save(os.path.join(FLAGS.output_dir, "vocab_processor.bin"))
