"""this script crawls for the profile pictures of researchers in google scholar
    and saves them in a folder called [figures]
    the crawler exploit the informations via the description of the tags in the html of google scholar

    be aware that too many requests to a server might interrupt your script, please
    set a proper sleep timing

    debug mode is also available for crawl local hosted websites.
    make sure to create a folder named 'figures' in the same path where you run this script
    """


from pandas import read_excel
import math
import requests
from bs4 import BeautifulSoup
import re
import time
import urllib

##this script lets you collect the profile pictures from researcher given a list of researchers
##it crawls google scholar


my_sheet = 'Tabellenblatt1'
file_name = 'Research Statistics.xlsx' # name of your excel file

df = read_excel(file_name, sheet_name = my_sheet)


#evaluate performances
start = time.time()
##Definitions
def enable_debug_mode(debug_bool):
    if debug_bool == True:
        web_site = 'http://127.0.0.1:5000'
        base_url="http://127.0.0.1:5000/"
    else:
        web_site = 'https://scholar.google.com'
        base_url="https://scholar.google.com/citations?hl=it&view_op=search_authors&mauthors="
    return web_site, base_url

web_site, base_url=enable_debug_mode(False)

#Source excel for researcher names
#names are in first column
#surname are in second column
ind=df.index.values+2

def download_mainpage(name, surname):
    r=requests.get(base_url + name + "+" + surname)
    print(r.status_code)
    return r.text

def download_subpage(link):
    r1=requests.get(web_site + link)
    return r1.text


def name_surname():
    all=[]
    for i in range(len(df)):
        # print(df.iloc[i])
        name = df.iloc[i][1]
        surname = df.iloc[i][0]
        if isinstance(name, str):
            all.append([name, surname])
        else:
            break
    return all

def data_not_available(name, surname, i):
    print("Data not available for " + name + " "+ surname + " in index " + str(i))

def main():
    all=name_surname()
    size_db = len(name_surname())
    print("get picts: start now")

    for i in range(size_db):
        name=name_surname()[i][0]
        surname=name_surname()[i][1]
        print(name, surname)
        ind=i+2
        soup = BeautifulSoup(download_mainpage(name, surname), 'html.parser')
        result=soup.find("h3",{'class':'gs_ai_name'})

        if result is None:
            data_not_available(name, surname, i)
            continue
        else:
            link= result.find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
            soup = BeautifulSoup(download_subpage(link), 'html.parser')

            central_table=soup.find(id="gsc_prf_w")
            img=central_table.find(id="gsc_prf_pup-img")
            urllib.request.urlretrieve("https://scholar.google.com"+img["src"], "figures/"+str(ind)+"-"+surname+".jpg")
            time.sleep(0.5)


    end = time.time()
    print("elapsed time: ")
    print(end - start)


if __name__== "__main__":
  main()
