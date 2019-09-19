import aiohttp
import asyncio
from pandas import read_excel
import time
from bs4 import BeautifulSoup
import re

web_site = 'https://scholar.google.com'
my_sheet = 'Tabellenblatt1'
file_name = 'Research Statistics.xlsx' # name of your excel file
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
df = read_excel(file_name, sheet_name = my_sheet)


def cut(L,n):
    'takes a list [L] and crop the first n elements'
    return L[:n]

def name_surname():
    all=[]
    for i in range(len(df)):
        name = df.iloc[i][1]
        surname = df.iloc[i][0]
        if isinstance(name, str):
            all.append([name, surname])
        else:
            break
    #all=cut(all,4)
    return all

async def find_and_extract_data(soup):
    central_table=soup.find(id="gsc_prf_w")
    description=central_table.find("div", {'class':"gsc_prf_il"}).text
    fields=[]
    for field in central_table.find("div", {'class':"gsc_prf_il", 'id':'gsc_prf_int'}).contents:
        fields.append(field.text)
    ##[fields] now we have a list of fields of the current professor
    corner_table = soup.find("div",{"class":"gsc_rsb_s gsc_prf_pnl"})
    #num cit in last 5 years
    num_cit_index=list(corner_table.find_all("td", {"class":"gsc_rsb_std"}))
    hist=corner_table.find("div",{"class":"gsc_md_hist_b"}).contents

    num_cit  = num_cit_index[1].text
    h_index  = num_cit_index[3].text
    i10_index= num_cit_index[5].text
    n14 = hist[-6].text
    n15 = hist[-5].text
    n16 = hist[-4].text
    n17 = hist[-3].text
    n18 = hist[-2].text
    n19 = hist[-1].text
    Data = [num_cit, h_index, i10_index, fields, n14, n15, n16, n17, n18, n19]
    return Data


def define_urls():
    base_url="https://scholar.google.com/citations?hl=it&view_op=search_authors&mauthors="
    #base_url="http://127.0.0.1:5000/"
    all=name_surname()
    urls=[base_url+name_surname()[i][0] + "+"+name_surname()[i][1] for i in range(len(name_surname()))]
    return urls

async def save_in_file(f, name, Data):
    temp_name_list=name.split('+')
    name=temp_name_list[0]
    surname=temp_name_list[1]
    #print("saving: " + name + " " + surname)
    #f.write(df.iloc[i][0] + "; " + df.iloc[i][1] + "; " + df.iloc[i][2] + "; " +
    #str(df.iloc[i][3]) + "; " + str(df.iloc[i][4]) + "; " + str(df.iloc[i][5]) + "; " +
    #str(df.iloc[i][6]) + "; " + str(df.iloc[i][7]) + "; " + str(df.iloc[i][8]) + "; ")
    f.write(name + "; " + surname + "; ")
    f.write(Data[0] + "; " + Data[1] + "; " + Data[2] + "; ")
    for i in Data[3]:
        f.write(i + ", ")
    f.write("; " + Data[4] + "; " + Data[5] + "; " + Data[6] + " ;" + Data[7]+ "; " + Data[8] + "; " + Data[9] + "\n")

def init_file():
    f=open("stats_parallel.txt","a")
    #create base columns Names
    for i in range(len(df.columns)):
        f.write(df.columns[i] + "; ")
    f.write("\n")
    return f

def close_file(f):
    print("File saved \n")
    f.close()

async def fetch_sub(session, url, f, name):
    async with session.get(url, timeout=60) as response:
        #time.sleep(0.2) #avoid error 429
        assert response.status == 200
        #print("fetching: " + name)
        #print(type(await response.text()))
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        Data = await find_and_extract_data(soup)
        await save_in_file(f, name, Data)
        #print(response)
        #print(await response.reason)

        #rint(await response.status_code)
        #print(response.text())
        #return await response.status()


async def fetch(session, url, f):
    async with session.get(url, timeout=60) as response:
        #time.sleep(0.2) #avoid error 429
        soup=BeautifulSoup(await response.text(), 'html.parser')
        result=soup.find("h3",{'class':'gs_ai_name'})
        #print(type(result.text))
        if result is not None:
            link= result.find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
            #print(web_site+link)
            assert response.status==200
            #print('\n')
            name=url[75:]
            await fetch_sub(session, web_site+link, f, name)
        #return await response.text()


async def fetch_all_urls(session, urls, loop, f):
    results = await asyncio.gather(*[fetch(session, url, f) for url in urls],
    return_exceptions=True)
    return results

async def main():
    start = time.time()
    #aiohttp.ClientSession.head(headers)
    f=init_file()
    loop = asyncio.get_event_loop()
    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector, loop=loop, headers=headers) as session:
        urls=define_urls()
        html = await fetch_all_urls(session, urls, loop, f)
        #print(html)

    close_file(f)
    end = time.time()
    print("elapsed time: ")
    print(end - start)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
