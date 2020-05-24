import bs4 as bs
from requests import get
import pickle
import os

with open('nifty_next_tickers.pickle', 'rb') as f:
    tickers = pickle.load(f)

for stock in tickers:

    # we will get the data from screener.in
    url = f"https://www.screener.in/company/{stock}/consolidated/#documents"

    # bs4
    response = get(url)
    soup = bs.BeautifulSoup(response.text, 'lxml')

    annual_report_section = soup.find_all('div', {'class': 'three columns'})[0]
    annual_report_list = annual_report_section.find('ul')
    lists = annual_report_list.find_all('li')

    href_links = []
    file_names = []

    for li in lists:
        text = li.a.text.strip().replace('Financial Year', 'Annual Report')
        file_names.append(text)

        a_tags = li.find('a', href=True)
        href = a_tags['href']
        if '.pdf' in href:
            href_links.append(href)

    x = list(zip(file_names, href_links))

    for year, link in x:

        if os.path.exists(f"{stock}\\{year}.pickle"):
            print(f"We already have a pickle of {year} for {stock}")

        else:
            pdf = get(link)

            if os.path.exists(f'{stock}'):

                with open(f"{stock}/{year}.pdf", 'wb') as f:
                    f.write(pdf.content)
                print(f"Got annual {year} for {stock}!")

            else:

                os.makedirs(f"{stock}")
                with open(f"{stock}/{year}.pdf", 'wb') as f:
                    f.write(pdf.content)
                print(f"Got annual {year} for {stock}!")
