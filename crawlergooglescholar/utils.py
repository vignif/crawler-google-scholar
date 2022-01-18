"""Utils for crawler google scholar
"""
import pandas as pd
import glob

def enable_debug_mode(debug_bool):
    if debug_bool == True:
        web_site = "http://127.0.0.1:5000"
        base_url = "http://127.0.0.1:5000/"
    else:
        web_site = "https://scholar.google.com"
        base_url = "https://scholar.google.com/citations?hl=it&view_op=search_authors&mauthors="
    return web_site, base_url


def init_file(name):
    f = open(name, "a")
    print("Output file opened")
    # create base columns Names
    t = glob.glob("*/template.txt")
    if len(t) > 0:
        df = pd.read_csv(t[0], sep=";", header=0)
    else:
        print("template invalid")
    for i in range(len(df.columns)):
        f.write(str(df.columns[i]) + "; ")
    f.write("\n")
    return f


def close_file(f):
    print("File saved \n")
    f.close()


def data_not_available(f, name, surname=None, i=0):
    print("Data not available for " + name + " " + surname + " in index " + str(i))
    f.write("Data Not available for " + name + " " + surname + "\n")


def name_surname(df):
    all = []
    for i in range(len(df)):
        name = df.iloc[i][1]
        surname = df.iloc[i][0]
        if isinstance(name, str):
            all.append([name, surname])
        else:
            break
    return all


def cut(L, n):
    """
    Takes a list [L] and crop the first n elements
    this fuction is useful for testing
    i.e if your file is really big and you just want to receive the stats of
    the first 5 researcher set n=5 in main()
    """
    if n == 0:
        n = len(L)
    return L[:n]

async def save_in_file(f, name, Data):
    """used in coroutine and parallel scripts

    Args:
        f (file handle): reference for saving data in disk
        name (str): name of the researcher
        Data (pandas dataframe): in memory data 
    """
    temp_name_list = name.split("+")
    name = temp_name_list[0]
    surname = temp_name_list[1]
    print("saving: " + name + " " + surname)
    f.write(name + "; " + surname + "; ")
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
    
if __name__ == "__main__":
    init_file("name")