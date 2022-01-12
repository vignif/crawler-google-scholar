"""Utils for crawler google scholar
"""


def enable_debug_mode(debug_bool):
    if debug_bool == True:
        web_site = "http://127.0.0.1:5000"
        base_url = "http://127.0.0.1:5000/"
    else:
        web_site = "https://scholar.google.com"
        base_url = "https://scholar.google.com/citations?hl=it&view_op=search_authors&mauthors="
    return web_site, base_url


def init_file(name, df):
    assert (type(name), str)
    f = open(name, "a")
    # create base columns Names
    for i in range(len(df.columns)):
        f.write(df.columns[i] + "; ")
    f.write("\n")
    return f


def close_file(f):
    print("File saved \n")
    f.close()


def data_not_available(f, name, surname=None, i=0):
    print("Data not available for " + name + " " + surname + " in index " + str(i))
    f.write("Data Not available for " + name + " " + surname + "\n")
