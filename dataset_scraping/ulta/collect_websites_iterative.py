from bs4 import BeautifulSoup
import requests

possible_prefixes = ["https://www.ulta.com/shop", "https://www.ulta.com/p", "https://www.ulta.com/brand"]

visited = set()
unvisited = {"https://www.ulta.com"}

def contains_one_of(link, list):
    for item in list:
        if item in link:
            return True
    return False


def get_all_links(allowed_prefixes):
    
    while len(unvisited) > 0:

        elem = unvisited.pop()
        visited.add(elem)

        try:
            html_text = requests.get(elem).text
            soup = BeautifulSoup(html_text, 'lxml')
            links = soup.find_all('a')
        except:
            continue

        # write immediately
        with open('dataset_scraping/ulta/visited.txt', mode='a', encoding='utf-8') as f:
            f.write(elem + "\n")
            f.close()

        for link in links:
            url = link.get('href')
            if url != None and url not in visited and contains_one_of(url, allowed_prefixes) and url not in unvisited:
                unvisited.add(url)

                # write immediately
                with open('dataset_scraping/ulta/unvisited.txt', mode='a', encoding='utf-8') as f:
                    f.write(url + "\n")
                    f.close()
                
                print(url)

get_all_links(possible_prefixes)


