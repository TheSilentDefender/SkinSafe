from bs4 import BeautifulSoup
import requests
import csv
import re

def is_ingredient_label(text):

    # common ingredients that are usually not advertised 
    special_ingredients = {"oxide", "poly", "sulfate", "kaolin", "benz", "talc", "mica", "acetylsalicylic"}
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

        html_text = requests.get(link)
        soup = BeautifulSoup(html_text.content.decode('utf-8'), "lxml")
        
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

            ingredients = '"' + ingredients + '"'
            data_array = [brand, tags, product, shade, ingredients, link]
            data = ",".join(data_array)

            print(data)

            # write to csv
            with open("/dataset_scraping/ulta/products.csv", 'a', encoding="utf-8") as f:
                f.write(data + "\n")
        
        else:
            print("Not makeup or skin care")


test_links = ["https://www.ulta.com/p/cleanancehydra-soothing-cream-pimprod2020800?sku=2577347&dcEvent=true",
"https://www.ulta.com/p/hyaluron-activ-b3-concentrated-plumping-serum-pimprod2036540?sku=2605858&dcEvent=true",
"https://www.ulta.com/p/a-oxitive-antioxidant-defense-serum-pimprod2020799?sku=2577162&dcEvent=true",
"https://www.ulta.com/p/cleanance-cleansing-gel-pimprod2021596?sku=2586859&dcEvent=true",
"https://www.ulta.com/p/tolerance-extremely-gentle-cleanser-lotion-pimprod2026572?sku=2586858&dcEvent=true",
"https://www.ulta.com/p/moisturizing-melt-in-balm-pimprod2020812?sku=2577350&dcEvent=true",
"https://www.ulta.com/p/trixera-nutrition-nutri-fluid-balm-pimprod2020820?sku=2577353&dcEvent=true",
"https://www.ulta.com/p/hypersensitive-skin-starter-kit-pimprod2026571?sku=2586857&dcEvent=true",
"https://www.ulta.com/p/cleanance-night-blemish-correcting-age-renewing-cream-pimprod2035345?sku=2599781&dcEvent=true",
"https://www.ulta.com/p/hydrance-boost-concentrated-hydrating-serum-pimprod2037832?sku=2605878&dcEvent=true",
"https://www.ulta.com/p/cleanance-blemish-control-blemish-control-starter-kit-pimprod2021734?sku=2578782&dcEvent=true",
"https://www.ulta.com/p/rich-revitalizing-nourishing-cream-pimprod2020818?sku=2577352&dcEvent=true"]

extract_content(test_links)
