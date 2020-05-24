import zipfile
import pickle
import os
import glob

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML

# The function required
"""
Module that extract text from MS XML Word document (.docx).
(Inspired by python-docx <https://github.com/mikemaccana/python-docx>)
"""

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'


def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return ' '.join(paragraphs)


# The beginning of the loop

with open('nifty_next_tickers.pickle', 'rb') as f:
    tickers = pickle.load(f)

count = 0
for ticker in tickers:
    my_dir = f"C:/Users/SKA/OneDrive/Desktop/annual_reports/"

    my_docx = glob.glob(f"{ticker}/*.docx")

    for file_path in my_docx:

        file_name = file_path.split(".")[0].split("\\")[1]

        if os.path.exists(f"{ticker}\\{file_name}.pickle"):
            print(f"Already have {ticker}\\{file_name}.pickle")

        else:
            try:
                text = get_docx_text(file_path)

                with open(f"{ticker}\\{file_name}.pickle", 'wb') as f:
                    pickle.dump(text, f)
                print(f"Converted {ticker}\\{file_name}.docx to {file_name}.pickle")


            except Exception as e:
                print(f"File at {ticker}\\{file_name}.docx cause a problem")
                print(str(e))
    count += 1
    print(count)