"""
this script crawls for the statistics of researchers in google scholar
and save them in a file called: co_data.txt
the source information must be an .xlsx file with two columns [surname, name]
very little preprocessing is made for these values so be sure to use UTF-8 for the enconding
per each researcher provided in the file it gets
[tot # citations; h-index; i10_index; fields_of_research; #citations last 5 years]
the crawler exploit the informations via the description of the tags in the html of google scholar
be aware that too many requests to a server might interrupt your script, please
set a proper sleep timing
debug mode is also available for crawl local hosted websites.

if a 429 error is returned, google a bit how to overcome it
"""

import aiohttp
import asyncio
import bs4
import re
from pandas import read_excel
from utils import (
    enable_debug_mode,
    init_file,
    close_file,
    data_not_available,
    cut
)

# set debut to true if you run a local server for testing
debug = False

# set verbose to true to get additional infos in nested functions
verbose = True

# define your output filename
output = "coroutine.txt"

web_site, base_url = enable_debug_mode(debug)

to_cut = len(base_url)


async def get_name(url):
    name = url[to_cut:]
    return name


async def find_and_extract_data(soup):
    """
    This function parse the html structure and look for specific fields of the css
    It is returning the statistic of the researcher up to 5 years ago in as a list [Data]
    """
    central_table = soup.find(id="gsc_prf_w")
    description = central_table.find("div", {"class": "gsc_prf_il"}).text
    fields = []
    for field in central_table.find(
        "div", {"class": "gsc_prf_il", "id": "gsc_prf_int"}
    ).contents:
        if isinstance(field, bs4.element.NavigableString):
            continue
        if isinstance(field, bs4.element.Tag):
            fields.append(field.text)
    corner_table = soup.find("div", {"class": "gsc_rsb_s gsc_prf_pnl"})
    try:
        num_cit_index = list(corner_table.find_all("td", {"class": "gsc_rsb_std"}))
        hist = corner_table.find("div", {"class": "gsc_md_hist_b"}).contents
    except:
        raise ValueError

    for i in range(len(hist)):
        if isinstance(hist[i], bs4.element.Tag):
            hist.append(hist[i])
    ##take stats all time index [0] , [2] , [4]
    ##take stats last 5 years index [1], [3], [5]

    num_cit = num_cit_index[0].text  # all time
    h_index = num_cit_index[2].text
    i10_index = num_cit_index[4].text
    n14 = hist[-6].text  # year-5
    n15 = hist[-5].text  # year-4
    n16 = hist[-4].text  # year-3
    n17 = hist[-3].text  # year-2
    n18 = hist[-2].text  # last_year
    n19 = hist[-1].text  # current_year
    Data = [num_cit, h_index, i10_index, fields, n14, n15, n16, n17, n18, n19]
    return Data


async def fetch_all(url, f):
    """
    Core function of the whole Program
    fetch_all is iteratively requesting an html page and calling other functions
    it's receiving as input the complete url with appended name and surname of the researcher
    for parsing and saving data without idle time
    """
    async with aiohttp.ClientSession() as session:
        # create get request
        async with session.get(url) as response:
            name = await get_name(url)
            status = response.status
            response = await response.text()
            # check on server response
            if status == 429:
                print("too many requests to server, error code: 429")
            if verbose:
                print(name, status)
            soup = bs4.BeautifulSoup(response, "html.parser")
            result = soup.find("h3", {"class": "gs_ai_name"})  # find name and its url
            if result is None:
                data_not_available(f, name)
            else:
                link = result.find("a", href=re.compile(r"[/]([a-z]|[A-Z])\w+")).attrs[
                    "href"
                ]
                L = []
                # create sub get request
                async with session.get(web_site + link) as subresponse:
                    # print("start: " + name)
                    print(
                        "request: " + name + " with status: " + str(subresponse.status)
                    )
                    html = await subresponse.text()
                    soup = bs4.BeautifulSoup(html, "html.parser")
                    Data = await find_and_extract_data(soup)
                    # print(await get_name(web_site+link))
                    # a = await store_in_list(L, name, Data)

                    # await save_in_file(f, name, Data)

def create_links(df, n):
    """
    Given a name and surname of the input file, this function create the url string
    to be given for the request
    """
    all=[]
    for i in range(len(df)):
        name = df.iloc[i][1]
        surname = df.iloc[i][0]
        if isinstance(name, str) and isinstance(surname,str): # the couple name, surname must be given in the xlsx file
            all.append(base_url+name+"+"+surname)
        else:
            break
    all=cut(all,n)
    return all

def print_all_pages(df, out, n):
    """
    iteratively initiating a new task for crawls
    higher level of fetch_all, this function is computing the complete urls
    and passing them to fetch_all for a deeper investigation
    """
    f = init_file(out)
    pages = create_links(df, n)
    # print(pages)
    tasks = []
    loop = asyncio.new_event_loop()
    try:
        for page in pages:
            tasks.append(loop.create_task(fetch_all(page, f)))
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        print("Program terminated by user")
        print("<---Bye--->")
    loop.close()
    close_file(f)


def outer_fetch(df):
    """
    main function check for all the names in the file_name
    set n to crawl only the first [n] rows of your researcher file_name
    if n=0 it takes all the rows of the input file
    """
    out_file = "out_coroutine.txt"
    n = 0
    print_all_pages(df, out_file, n)


if __name__ == "__main__":
    print("run this script from crawl.py")
    # outer_fetch(df)
