from bs4 import BeautifulSoup
import requests

original_link = "https://www.ulta.com"

visited = []
unvisited = [original_link]

def get_all_links():
    
    while len(unvisited) > 0:

        visited.append(unvisited[0])
        html_text = requests.get(unvisited[0]).text

        del unvisited[0]

        soup = BeautifulSoup(html_text, 'lxml')
        links = soup.find_all('a')

        for link in links:
            url = link.get('href')
            if url != None and url not in visited and url.startswith(original_link) and url not in unvisited:
                unvisited.append(url)
                print(url)

get_all_links()

with open("all_ulta_links.txt", 'w') as f:
    for link in visited:
        f.write(link)
    f.close()
