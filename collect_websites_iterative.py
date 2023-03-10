from bs4 import BeautifulSoup
import requests

possible_prefixes = ["https://www.ulta.com/shop", "https://www.ulta.com/p", "https://www.ulta.com/brand"]

visited = set()
unvisited = {"https://www.ulta.com/shop/makeup", "https://www.ulta.com/shop/skin-care", "https://www.ulta.com/shop/hair", "https://www.ulta.com/shop/fragrance", "https://www.ulta.com/shop/bath-body", "https://www.ulta.com/shop/tools-brushes"}

def contains_one_of(link, list):
    for item in list:
        if item in link:
            return True
    return False


def get_all_links(allowed_prefixes):
    
    while len(unvisited) > 0:

        elem = unvisited.pop()
        visited.add(elem)
        html_text = requests.get(elem).text
        soup = BeautifulSoup(html_text, 'lxml')
        links = soup.find_all('a')

        for link in links:
            url = link.get('href')
            if url != None and url not in visited and contains_one_of(url, allowed_prefixes) and url not in unvisited:
                unvisited.add(url)
                print(url)

get_all_links(possible_prefixes)

with open('all_ulta_links.txt', mode='wt', encoding='utf-8') as f:
    f.write('\n'.join(visited))
