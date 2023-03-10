from bs4 import BeautifulSoup
import requests

original_link = "https://www.ulta.com"

visited = set()

def get_all_links(link):

    visited.add(link)

    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    links = soup.find_all('a')
    for link in links:
        url = link.get('href')
        if url != None and url not in visited and url.startswith(original_link):
            print(url)
            get_all_links(url)

get_all_links(original_link)

with open("all_ulta_links.txt", 'w') as f:
    for link in visited:
        f.write(link)
    f.close()
