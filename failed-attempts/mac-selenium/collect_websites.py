from selenium import webdriver
from selenium.webdriver.common.by import By

original_link = "https://www.maccosmetics.com/product/13838/103725/products/makeup/eyes/eyeliner/mac-colour-excess-gel-pencil-eye-liner?shade=Serial_Monogamist"

visited = set()
visited.add(original_link)

driver = webdriver.Chrome('chromedriver')

current_header = ""

def visit_site(link):

    driver.get(link)
    driver.implicitly_wait(5)
    search = driver.find_elements(By.TAG_NAME, "a")

    for element in search:
        
        url = element.get_attribute("href")

        if (url != None) and (url not in visited) and (not "tmpl" in url) and (original_link in url):
            visited.add(url)
            print("Recurring on " + url + " next.")
            visit_site(url)

visit_site(original_link)

with open("mac-redo/mac_link.txt", 'w') as f:
    for row in visited:
        f.write('\n'.join(row))
    f.close()