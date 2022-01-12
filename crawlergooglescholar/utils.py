##Definitions
def enable_debug_mode(debug_bool):
    if debug_bool == True:
        web_site = "http://127.0.0.1:5000"
        base_url = "http://127.0.0.1:5000/"
    else:
        web_site = "https://scholar.google.com"
        base_url = "https://scholar.google.com/citations?hl=it&view_op=search_authors&mauthors="
    return web_site, base_url
