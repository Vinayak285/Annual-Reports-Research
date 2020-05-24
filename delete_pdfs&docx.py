import glob
import os

import pickle

with open('nifty_next_tickers.pickle', 'rb') as f:
    tickers = pickle.load(f)

for ticker in tickers:

    file_dir = f"{ticker}/"

    pdfs = glob.iglob(os.path.join(file_dir, '*.pdf'))
    docx = glob.iglob(os.path.join(file_dir, '*.docx'))
    pickles = glob.iglob(os.path.join(file_dir, '*.pickle'))

    zipped = list(zip(pdfs, docx, pickles))

    for pdf, doc, pickle_file in zipped:

        if pdf.split('.')[0] == pickle_file.split('.')[0]:
            os.remove(pdf)
            print(f"Removed {pdf}!")
        else:
            print(f"There seems to be a mismatch between {pdf} and {pickle_file}!")

        if doc.split('.')[0] == pickle_file.split('.')[0]:
            os.remove(doc)
            print(f"Removed {doc}!")
        else:
            print(f"There seems to be a mismatch between {doc} and {pickle_file}!")
