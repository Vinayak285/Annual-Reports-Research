import os
import winerror
from win32com.client.dynamic import Dispatch, ERRORS_BAD_CONTEXT

import pickle
import glob

with open('nifty_next_tickers.pickle', 'rb') as f:
    tickers = pickle.load(f)

count = 0
for ticker in tickers:

    print(ticker)

    ERRORS_BAD_CONTEXT.append(winerror.E_NOTIMPL)

    my_dir = f"{ticker}/"

    my_pdfs = glob.glob(f"*.pdf")

    for my_pdf in my_pdfs:

        file_name = my_pdf.split(".")[0].split("\\")[1]

        os.chdir(my_dir)
        src = os.path.abspath(my_pdf)

        if os.path.exists(f'{ticker}/{file_name}.docx'):
            print(f"Already have {ticker}/{file_name}.docx")

        else:
            try:
                AvDoc = Dispatch("AcroExch.AVDoc")

                if AvDoc.Open(src, ""):
                    pdDoc = AvDoc.GetPDDoc()
                    jsObject = pdDoc.GetJSObject()
                    jsObject.SaveAs(os.path.join(my_dir, f'{file_name}.docx'), "com.adobe.acrobat.docx")
                    print(f"Converted {ticker}/{file_name}.pdf to {file_name}.docx!")

            except Exception as e:
                print(str(e))

            finally:
                AvDoc.Close(True)

                jsObject = None
                pdDoc = None
                AvDoc = None

    count += 1
    print(count)
