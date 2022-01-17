from pandas import read_excel
import requests
from bs4 import BeautifulSoup
import re
import time
from utils import enable_debug_mode, init_file, close_file, data_not_available, name_surname

##this script lets you collect researcher statistics from a list of researchers
##it crawls google scholar and collects
## num of citations last 5 years
## num of citations per year of last 5 years
## h-index
## i10-index


# evaluate performances
start = time.time()

web_site, base_url = enable_debug_mode(False)

# Source excel for researcher names
# names are in first column
# surname are in second column

def download_mainpage(name, surname):
    r = requests.get(base_url + name + "+" + surname)
    print(r.status_code)
    return r.text


def download_subpage(link):
    r1 = requests.get(web_site + link)
    return r1.text


def save_in_file(df, f, i, Data):
    f.write(
        df.iloc[i][1]
        + "; "
        + df.iloc[i][0]
        + "; ")
    f.write(Data[0] + "; " + Data[1] + "; " + Data[2] + "; ")
    for i in Data[3]:
        f.write(i + ", ")
    f.write(
        "; "
        + Data[4]
        + "; "
        + Data[5]
        + "; "
        + Data[6]
        + " ;"
        + Data[7]
        + "; "
        + Data[8]
        + "; "
        + Data[9]
        + "\n"
    )

def find_and_extract_data(soup):
    central_table = soup.find(id="gsc_prf_w")
    description = central_table.find("div", {"class": "gsc_prf_il"}).text
    fields = []
    for field in central_table.find(
        "div", {"class": "gsc_prf_il", "id": "gsc_prf_int"}
    ).contents:
        fields.append(field.text)
    ##[fields] now we have a list of fields of the current professor
    corner_table = soup.find("div", {"class": "gsc_rsb_s gsc_prf_pnl"})
    # num cit in last 5 years
    num_cit_index = list(corner_table.find_all("td", {"class": "gsc_rsb_std"}))
    hist = corner_table.find("div", {"class": "gsc_md_hist_b"}).contents

    num_cit = num_cit_index[1].text
    h_index = num_cit_index[3].text
    i10_index = num_cit_index[5].text
    n14 = hist[-6].text
    n15 = hist[-5].text
    n16 = hist[-4].text
    n17 = hist[-3].text
    n18 = hist[-2].text
    n19 = hist[-1].text
    Data = [num_cit, h_index, i10_index, fields, n14, n15, n16, n17, n18, n19]
    print(Data)
    return Data


def fetch(df):
    # print("Let's download the statistics from google scholar\n")
    f = init_file("get_serial.txt")
    all = name_surname(df)
    size_db = len(name_surname(df))

    for i in range(size_db):
        name = name_surname(df)[i][0]
        surname = name_surname(df)[i][1]

        # print("Status: %3.2f%%" % (i/size_db*100))

        # print("\n \n")
        soup = BeautifulSoup(download_mainpage(name, surname), "html.parser")
        result = soup.find("h3", {"class": "gs_ai_name"})

        # if is not able to find the person, tell me and skip the data in the db
        if result is None:
            data_not_available(f, name)
            continue
        else:
            link = result.find("a", href=re.compile(r"[/]([a-z]|[A-Z])\w+")).attrs[
                "href"
            ]
            soup = BeautifulSoup(download_subpage(link), "html.parser")
            Data = find_and_extract_data(soup)
            save_in_file(df, f, i, Data)

    close_file(f)

    end = time.time()
    print("elapsed time: ")
    print(end - start)


if __name__ == "__main__":
    print('run this script from crawl.py')
    # fetch(df)
