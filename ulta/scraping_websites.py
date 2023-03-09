from bs4 import BeautifulSoup
import requests
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

all_rows = []

# driver = webdriver.Chrome('chromedriver')

# csv format: brand, tags, name, shade, ingredients, links

# with open("mac/rest_links.txt") as f:
#     all_links = f.readlines()

all_links = ["https://www.ulta.com/p/all-bright-c-serum-pimprod2038159"]

for link in all_links:

    # driver.get(link)
    # driver.implicitly_wait(20)
    # search = driver.find_elements(By.CLASS_NAME, "sc-pZBmh ksvXAS elc-body--2")
    # print(search)

    # for element in search:
    #     text = element.get_attribute("textContent")
    #     if "Ingredients:" in text:
    #         print(text)

    # scraping a single website
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    ingredient_div = soup.findAll('p')
    ingredients = ""
    for item in ingredient_div:
        text = item.text
        if ("Ingredients" in text) or ("Active:" in text) or ("Water" in text) or ("Mica" in text): 
            ingredients = ingredients + text
            print(text)

    # <span class="Text-ds Text-ds--body-3 Text-ds--left Text-ds--black">Global Citizen</span> shade name

    # <span class="Text-ds Text-ds--title-5 Text-ds--left">Retinol Fusion PM Night Serum</span> product name

    # link_parts = link.split("/")
    # products_index = link_parts.index("products")

    # # replacing this one unecessary string that sometimes appears
    # link_parts[-1] = link_parts[-1].replace("?vto_open", "")

    # if ingredients != None:
    #     ingredients = ingredients.text.strip()
    #     if len(link_parts) - products_index == 4:
    #         # it is a link thaat does not have shade separated with a /
    #         # get all the attributes into a tag
    #         tags = link_parts[products_index + 1] + ":" + link_parts[products_index + 2]
    #         # there is not a shade name
    #         product = link_parts[products_index + 3]
    #         shade = "N/A"
    #     elif len(link_parts) - products_index == 5:
    #         # it is a link that does not have shade separated with a /
    #         # get all the attributes into a tag
    #         tags = link_parts[products_index + 1] + ":" + link_parts[products_index + 2] + ":" + link_parts[products_index + 3]
    #         if ("?" in link_parts[products_index + 4]):
    #             # there is a shade name
    #             product_shade = link_parts[products_index + 4].split("?")
    #             product = product_shade[0]
    #             shade = product_shade[1].split("=")[1]
    #         else:
    #             # there is not a shade name
    #             product = link_parts[products_index + 4]
    #             shade = "N/A"
    #     else:
    #         # it is a link that has shades separated with a /
    #         tags = link_parts[products_index + 1] + ":" + link_parts[products_index + 2] + ":" + link_parts[products_index + 3]
    #         product = link_parts[products_index + 4].replace("#!", "")
    #         shade = re.sub("%[A-Z][0-9]", " ", link_parts[-1])
    #         shade = re.sub(' +', ' ', shade).strip()

    #     # prettify the product text
    #     product = product.replace("-", " ").replace("_", " ").title()
    #     shade = shade.replace("-", " ").replace("_", " ")

    #     data = ["MAC Cosmetics", tags.strip(), product.strip(), shade.strip(), ingredients.strip(), link.strip()]

    #     print(data)

    #     # write to csv
    #     f = open("mac/mac_cosmetics2.csv", "a")
    #     w = csv.writer(f, delimiter = ",")
    #     w.writerow(data)
    #     f.close()