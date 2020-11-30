
from bs4 import BeautifulSoup
from lxml import etree
import lxml
import re
import pandas as pd
import nltk
from itertools import islice

def stats(chan, yung):
    chan_fd = nltk.FreqDist(chan)
    chan_fd_s = sort_dict(chan_fd)

    yung_fd = nltk.FreqDist(yung)
    yung_fd_s = sort_dict(nltk.FreqDist(yung))

    chan_top20 = take(20, chan_fd_s)
    yung_top20 = take(20, yung_fd_s)

    common_word = set(list(chan_fd)) & set(list(yung_fd))
    common_fq = { w : (chan_fd[w] + yung_fd[w])  for w in common_word}
    common_fq_s = sort_dict(common_fq)

    print(chan_top20, '\n')
    print(yung_top20, '\n')
    print(common_fq_s, '\n')


def clean_text(xml_txt):

    f = open(xml_txt,'r')
    content = f.read()
    f.close()
    soup = BeautifulSoup(content, 'lxml')

    chan_text = soup.chan_laisun.get_text()
    yung_text = soup.yung_wing.get_text()

    pattern =  r'\w+'

    chan_tokens = nltk.regexp_tokenize(chan_text, pattern)
    yung_tokens = nltk.regexp_tokenize(yung_text, pattern)

    wnl = nltk.WordNetLemmatizer()
    sw = nltk.corpus.stopwords.words('english')
    chan_norm = [wnl.lemmatize(t) for t in chan_tokens if t.lower() not in sw]
    yung_norm  = [wnl.lemmatize(t) for t in yung_tokens if t.lower() not in sw]

    return chan_norm, yung_norm


def make_xml():

    df = pd.read_csv('text_metadata.csv', index_col=None, sep=', ', engine='python')
    # df.index = [x for x in range(1, len(df.values)+1)]
    # print(df)
    root_element = etree.Element("excerpts")
    chan_element = etree.SubElement(root_element, "chan_laisun")
    yung_element = etree.SubElement(root_element, "yung_wing")

    for i in range(len(df)):

        if df.iloc[i]["Author"] == "Chan Laisun":
            parent_tree = chan_element
        if df.iloc[i]["Author"] == "Yung Wing":
            parent_tree = yung_element

        text_element = etree.SubElement(parent_tree, "text")

        info_items = ["Source", "Date", "Title", "Page"]
        for info in info_items:
            text_element.set(info, df.iloc[i][info])

        txt = open(('text_files/' + df.iloc[i]["File"]), 'r')
        text_element.text = txt.read()
        txt.close()

    xml_string = etree.tostring(root_element, pretty_print = True, encoding = 'UTF-8')

    f = open('marked_data.xml', 'wb')
    f.write(xml_string)
    f.close()

    return 'marked_data.xml'


def sort_dict(dic):
    """ Sort a dictionary keys by values, in descending order. """

    return {k: v for k, v in sorted(dic.items(), key=lambda item: item[1], reverse=True)}


def take(n, iterable):
    """ Return the first n items from an iterable object. """

    return list(islice(iterable, n))


def main():

    file_name = make_xml()
    chan_norm_tokens, yung_norm_tokens = clean_text(file_name)
    stats(chan_norm_tokens, yung_norm_tokens)


if __name__ == '__main__':
    main()
