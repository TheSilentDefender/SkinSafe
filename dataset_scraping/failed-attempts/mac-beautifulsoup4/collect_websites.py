from bs4 import BeautifulSoup
import requests

link = "https://www.maccosmetics.com/bestsellers"

# CONSTANT
prefix = "https://www.maccosmetics.com"

# LINK ACCUMULATOR
visited = set()

def get_all_links(link):

    visited.add(link)

    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    links = soup.find_all('a')
    for link in links:
        # adding MAC specific rules for filtering/editing URLs, for example, the website giftcards/faq crashes for unknown reasons and is thus filtered out
        suffix = link.get('href')
        if (suffix != None):
            if ("https" in suffix) or ("http" in suffix):
                url = suffix
            elif (not suffix.startswith("/")):
                url = prefix + "/" + suffix
            else: 
                url = prefix + suffix
            if (url not in visited and (not "tmpl" in url)) and (url.startswith("https")) and ("www.maccosmetics.com" in url) and (url != "https://www.maccosmetics.com/giftcards/faq"):
                print(url)
                visited.add(url)
                get_all_links(url)

get_all_links(link)

with open("mac/all_mac_link.txt", 'w') as f:
    for link in visited:
        f.write(link)
    f.close()
    