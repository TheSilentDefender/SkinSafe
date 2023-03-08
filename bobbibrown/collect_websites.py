from bs4 import BeautifulSoup
import requests

link = "https://www.bobbibrowncosmetics.com/"

# CONSTANT
prefix = "https://www.bobbibrowncosmetics.com"

# LINK ACCUMULATOR
visited = set()

def get_all_links(link):

    visited.add(link)

    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    links = soup.find_all('a')
    for link in links:
        # adding Bobbi Brown specific rules for filtering/editing URLs, for example, the website for customer-service-contact-us crashes for unknown reasons
        suffix = link.get('href')
        if (suffix != None):
            if ("https" in suffix) or ("http" in suffix):
                url = suffix
            elif (not suffix.startswith("/")):
                url = prefix + "/" + suffix
            else:
                url = prefix + suffix
            if (url not in visited) and (url.startswith("https")) and ("www.bobbibrowncosmetics.com" in url) and (not "tmpl" in url) and (not "javascript" in url) and (not ":+" in url) and (not url == "https://www.bobbibrowncosmetics.com/customer-service-contact-us"):
                print(url)
                visited.add(url)
                get_all_links(url)

get_all_links(link)

with open("bobbibrown/all_bb_link.txt", 'w') as f:
    for link in visited:
        f.write(link)
    f.close()
    