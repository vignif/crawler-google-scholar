import aiohttp
import asyncio
import bs4
import re
from pandas import read_excel
import time


debug = 1


def enable_debug_mode(debug_bool):
    if debug_bool == True:
        web_site = 'http://127.0.0.1:5000'
        base_url="http://127.0.0.1:5000/"
        to_cut=len(base_url)
    else:
        web_site = 'https://scholar.google.com'
        base_url="https://scholar.google.com/citations?hl=it&view_op=search_authors&mauthors="
        to_cut=len(base_url)
    return web_site, base_url, to_cut

web_site, base_url, to_cut=enable_debug_mode(debug)

def init_file():
    f=open("stats_parallel.txt","a")
    #create base columns Names
    for i in range(len(df.columns)):
        f.write(df.columns[i] + "; ")
    f.write("\n")
    return f


async def get_name(url):
    name=url[to_cut:]
    return name


async def save_in_file(f, name, Data):
    print("name: ",name)
    temp_name_list=name.split('+')
    name=temp_name_list[0]
    surname=temp_name_list[1]
    print("saving: " + name + " " + surname)
    f.write(name + "; " + surname + "; ")
    f.write(Data[0] + "; " + Data[1] + "; " + Data[2] + "; ")
    for i in Data[3]:
        f.write(i + ", ")
    f.write("; " + Data[4] + "; " + Data[5] + "; " + Data[6] + " ;" + Data[7]+ "; " + Data[8] + "; " + Data[9] + "\n")

async def find_and_extract_data(soup):
    print("find_and_extract_data")
    central_table=soup.find(id="gsc_prf_w")
    description=central_table.find("div", {'class':"gsc_prf_il"}).text
    fields=[]
    for field in central_table.find("div", {'class':"gsc_prf_il", 'id':'gsc_prf_int'}).contents:
        if isinstance(field, bs4.element.NavigableString):
            continue
        if isinstance(field, bs4.element.Tag):
            fields.append(field.text)
    corner_table = soup.find("div",{"class":"gsc_rsb_s gsc_prf_pnl"})
    #print(fields)
    #print(corner_table.text)
    try:
        num_cit_index=list(corner_table.find_all("td", {"class":"gsc_rsb_std"}))
        hist=corner_table.find("div",{"class":"gsc_md_hist_b"}).contents
        #print(num_cit_index)
    except:
        raise ValueError

    for i in range(len(hist)):
        if isinstance(hist[i], bs4.element.Tag):
            hist.append(hist[i])

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


async def fetch_all(url):
    # connect to the server
    async with aiohttp.ClientSession() as session:
        # create get request
        async with session.get(url) as response:
            #assert response.status==200
            response = await response.text()
            soup=bs4.BeautifulSoup(response, 'html.parser')
            result=soup.find("h3",{'class':'gs_ai_name'}) #find name and its url
            if result is not None:
                link= result.find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']

                #create sub get request
                async with session.get(web_site+link) as subresponse:
                    name= await get_name(url)
                    #print("start: " + name)
                    html = await subresponse.text()
                    soup = bs4.BeautifulSoup(html, 'html.parser')
                    Data = await find_and_extract_data(soup)
                    #print(await get_name(web_site+link))
                    f=open("stats_parallel.txt","a")
                    await save_in_file(f, name, Data)

                    #print("finish: ", name)
                    #print("\n")





my_sheet = 'Tabellenblatt1'
file_name = 'Research Statistics.xlsx' # name of your excel file
df = read_excel(file_name, sheet_name = my_sheet)

def cut(L,n):
    'takes a list [L] and crop the first n elements'
    return L[:n]


def create_links():
    # base_url="https://scholar.google.com/citations?hl=it&view_op=search_authors&mauthors="
    all=[]
    for i in range(len(df)):
        name = df.iloc[i][1]
        surname = df.iloc[i][0]
        if isinstance(name, str):
            all.append(base_url+name+"+"+surname)
        else:
            break
    #all=cut(all,3)
    return all



def print_all_pages():
    f=init_file()
    pages = create_links()
    #print(pages)
    tasks =  []
    loop = asyncio.new_event_loop()
    for page in pages:
        tasks.append(loop.create_task(fetch_all(page)))

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    close_file(f)
