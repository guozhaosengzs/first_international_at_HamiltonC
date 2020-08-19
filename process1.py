
from bs4 import BeautifulSoup
from lxml import etree
import lxml
import re
import pandas as pd



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


def main():

    files = make_xml()


if __name__ == '__main__':
    main()
