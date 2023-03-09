from selenium import webdriver
from selenium.webdriver.common.by import By

visited = set()

url = "https://www.bobbibrowncosmetics.com/product/2330/108070/makeup/eyes/eye-shadow/long-wear-cream-shadow-stick/fh22#/shade/Sun_Pearl"
driver = webdriver.Chrome('chromedriver')
driver.get(url)
driver.implicitly_wait(10)
search = driver.find_elements(By.TAG_NAME, "a")
for element in search:
    link = element.get_attribute("href")
    if link not in visited:
        print(link)
        visited.add(link)