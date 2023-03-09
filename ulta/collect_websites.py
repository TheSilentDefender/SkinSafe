
from bs4 import BeautifulSoup
import requests

link = "https://www.esteelauder.com/products/1799/product-catalog/bestsellers?gclid=Cj0KCQiAgaGgBhC8ARIsAAAyLfGZJ6H_fhpxRhZHfOUuygcR_v_8qk7Ybi4Vpw8PWEpcohSXlnRG_jQaArYPEALw_wcB&gclsrc=aw.ds"

links_that_wont_work_for_no_reason = ["https://www.esteelauder.com/customer-service/contact-us", "https://www.esteelauder.com/elist", "https://www.esteelauder.com/loyalty_ldg"]

# CONSTANT
prefix = "https://www.esteelauder.com"

# LINK ACCUMULATOR
visited = set()

def get_all_links(link):

    visited.add(link)

    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    links = soup.find_all('a')
    for link in links:
        suffix = link.get('href')
        print(suffix)
        if (suffix != None):
            if ("https" in suffix) or ("http" in suffix):
                url = suffix
            elif (not suffix.startswith("/")):
                url = prefix + "/" + suffix
            else: 
                url = prefix + suffix
            if (url not in visited and (not "tmpl" in url)) and (url.startswith("https")) and ("www.esteelauder.com" in url) and (url not in links_that_wont_work_for_no_reason):
                print(url)
                visited.add(url)
                get_all_links(url)

get_all_links(link)

with open("esteelauder/unfiltered_links.txt", 'w', encoding="utf-8") as f:
    for link in visited:
        f.write('\n'.join(link))
    f.close()

    