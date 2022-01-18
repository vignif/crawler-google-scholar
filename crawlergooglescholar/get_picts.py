"""this script crawls for the profile pictures of researchers in google scholar
    and saves them in a folder called [figures]
    the crawler exploit the informations via the description of the tags in the html of google scholar

    be aware that too many requests to a server might interrupt your script, please
    set a proper sleep timing

    debug mode is also available for crawl local hosted websites.
    make sure to create a folder named 'figures' in the same path where you run this script
    """

import requests
from bs4 import BeautifulSoup
import re
import time
import urllib
from .utils import enable_debug_mode, name_surname

##this script lets you collect the profile pictures from researcher given a list of researchers
##it crawls google scholar

# evaluate performances
start = time.time()

web_site, base_url = enable_debug_mode(False)

# Source excel for researcher names
# names are in first column
# surname are in second column
# ind = df.index.values + 2


def download_mainpage(name, surname):
    r = requests.get(base_url + name + "+" + surname)
    print(r.status_code)
    return r.text


def download_subpage(link):
    r1 = requests.get(web_site + link)
    return r1.text


def data_not_available(name, surname, i):
    print("Data not available for " + name + " " + surname + " in index " + str(i))


def fetch(df):
    all = name_surname(df)
    size_db = len(name_surname(df))
    print("get picts: start now")

    for i in range(size_db):
        name = name_surname(df)[i][0]
        surname = name_surname(df)[i][1]
        print(name, surname)
        ind = i + 2
        soup = BeautifulSoup(download_mainpage(name, surname), "html.parser")
        result = soup.find("h3", {"class": "gs_ai_name"})

        if result is None:
            data_not_available(name, surname, i)
            continue
        else:
            link = result.find("a", href=re.compile(r"[/]([a-z]|[A-Z])\w+")).attrs[
                "href"
            ]
            soup = BeautifulSoup(download_subpage(link), "html.parser")

            central_table = soup.find(id="gsc_prf_w")
            img = central_table.find(id="gsc_prf_pup-img")
            try:
                urlpic = "https://scholar.google.com" + img["src"]
                save_to = "figures/" + str(ind) + "-" + surname + ".jpg"
                urllib.request.urlretrieve(urlpic, save_to)
            except Exception as e:
                print("Error: ", e)
                if e.reason.errno == -2:
                    print("try a new link")
                    urlpic = img["src"]
                    urllib.request.urlretrieve(urlpic, save_to)
            print(urlpic)
            time.sleep(0.5)

    end = time.time()
    print("elapsed time: ")
    print(end - start)


if __name__ == "__main__":
    print("run this script from crawl.py")
