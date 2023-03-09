from selenium import webdriver
from selenium.webdriver.common.by import By

all_rows = []

driver = webdriver.Chrome('chromedriver')

def scrape_sites(links):

    for link in links:
        # if the current website is a product page, scrape it for product information
        if "https://www.maccosmetics.com/product" in link and "products" in link:

            driver.get(link)

            print("Scraping for product information")

            product = driver.find_element(By.XPATH, "//h1[@class='product-full__name']").get_attribute("textContent")
            shade = driver.find_element(By.XPATH, "//div[@class='product-full__shade-info-name']").get_attribute("textContent")
            ingredients = driver.find_element(By.XPATH, "//span[@class='sku-ingredients js-sku-ingredients']").get_attribute("textContent")

            print(product)
            print(shade)
            print(ingredients)

            all_rows.append("MAC Cosmetics" + "," + product + "," + shade + "," + ingredients + "," + link)
   
with open("mac-redo/mac_links.txt", "r") as f:
    lines = f.read().splitlines()
    scrape_sites(lines)

