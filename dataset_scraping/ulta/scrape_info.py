from bs4 import BeautifulSoup
import requests
import re

def is_ingredient_label(text):

    # common ingredients that are usually not advertised 
    special_ingredients = {"oxide", "poly", "sulfate", "kaolin", "benz", "talc", "mica", "acetylsalicylic", "glycerin", "water", "sodium", "retinol", "fiber", "synthetic"}
    # words that indicate text is a review and not an ingredient
    human_words = {"i", "tried", "and", "have", "too", "in", "with", "this", "it", "by", "or", "as"}

    like_ingredient = False
    like_human = False

    for ingredients in special_ingredients:
        if ingredients in text.lower():
            like_ingredient = True
         
    # dyes of the form Red 4, or CI 23494
    if re.search("Red [0-9][0-9]?", text) or re.search("Blue [0-9][0-9]?", text) or re.search("Yellow [0-9][0-9]?", text) or re.search("CI [0-9]{5}", text):
        like_ingredient = True

    all_words = text.replace(".", "").replace(",", "").split(" ")
    for word in all_words:
        if word in human_words:
            like_human = True

    if (like_human or not like_ingredient):
        return False
    else:
        return True

def extract_content(link_list):

    for link in link_list:

        # scraping a single website

        if ("https://www.ulta.com/p" in link): 

            try:
                html_text = requests.get(link)
                soup = BeautifulSoup(html_text.content.decode('utf-8'), "lxml")
            except:
                with open('dataset_scraping/ulta/errored.txt', 'a', encoding="utf-8") as f:
                    f.write(link + "\n")
                continue
            
            # tags
            tags = ""
            tag_containers = soup.find_all('li', class_="Breadcrumbs__List--item")
            for i in range(1, len(tag_containers)):
                if i == len(tag_containers) - 1:
                    tags += tag_containers[i].contents[1].text
                else:
                    tags += tag_containers[i].contents[1].text + ":"
            
            # only collecting makeup or skincare items 

            if "Makeup" in tags or "Skin Care" in tags:

                # brand name
                possible_brand = soup.find_all('a', class_="Link_Huge Link_Huge--compact")
                for b in possible_brand:
                    brand_link = b.get('href')
                    if brand_link != None and "https://www.ulta.com/brand" in brand_link:
                        brand = b.text

                # product name
                product = soup.find('span', class_='Text-ds Text-ds--title-5 Text-ds--left').text

                # shade name if applicable
                shade = "N/A"
                shade_container = soup.find('div', class_="SwatchDropDown__nameDescription")
                if shade_container != None and shade_container.contents[0] != None:
                    shade = shade_container.contents[0].text
                
                # ingredients
                ingredients = "N/A"
                possible_ingredients = soup.findAll('p')
                for item in possible_ingredients:
                    if is_ingredient_label(item.text):
                        ingredients = re.sub("\w+: ", "", item.text)

                if (ingredients != "N/A"):

                    # necessary addition since some of the product names + shades have a comma in them 
                    # which is recognized as a new column in a csv file
                    ingredients = '"' + ingredients + '"'
                    brand = '"' + brand + '"'
                    tags = '"' + tags + '"'
                    product = '"' + product + '"'
                    shade = '"' + shade + '"'

                    data_array = [brand, tags, product, shade, ingredients, link]
                    data = ",".join(data_array)

                    print(data)

                    # write to csv
                    with open("dataset_scraping/ulta/products.csv", 'a', encoding="utf-8") as f:
                        f.write(data)

with open('dataset_scraping/ulta/visited.txt') as f:
    all_links = f.readlines()

extract_content(all_links)
