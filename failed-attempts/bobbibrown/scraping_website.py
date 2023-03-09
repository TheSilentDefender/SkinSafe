from bs4 import BeautifulSoup
import requests
import csv
import re

# csv format: brand, tags, name, shade, ingredients, links

# with open("bobbibrown/bobbi_brown_links") as f:
#     all_links = f.readlines()

all_links = ["https://www.bobbibrowncosmetics.com/product/2327/35645/makeup/eyes/brows/perfectly-defined-long-wear-brow-pencil/ss15#/shade/Slate", "https://www.bobbibrowncosmetics.com/product/2321/39562/makeup/extra-lip-tint/ss16", "https://www.bobbibrowncosmetics.com/product/2343/32757/makeup/lips/lip-liner/lip-pencil/fh14?vto_open", "https://www.bobbibrowncosmetics.com/product/2341/39562/makeup/lips/lip-care/extra-lip-tint", 
"https://www.bobbibrowncosmetics.com/product/14017/55680/makeup/face/foundation/skin-long-wear-weightless-foundation-spf-15/16-hour-breathable-natural-matte-coverage"]

for link in all_links:

    # scraping a single website
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    ingredients = soup.find('p', class_='js-product-full-iln-content')

    if ingredients != None:

        ingredients = ingredients.text.strip()

        link_parts = link.split("/")
        product_index = link_parts.index("product")
        link.replace("?vto_open", "")

        content = []
        for i in range(product_index + 1, len(link_parts)):
            if (re.search("[0-9]{4,}?", link_parts[i])) == None and (re.search("[a-z][a-z][0-9][0-9]", link_parts[i])) == None:
                link_parts[i].replace("#", "")
                content.append(link_parts[i])

        if "shade" in content:
            shade_index = content.index("shade")
            tags = ""
            for i in range(0, shade_index - 1):
                tags = tags + ":" + content[i]
            tags = tags.removeprefix(":")
            product = content[shade_index - 1]
            shade = content[shade_index + 1]
        else:
            shade = "N/A"
            tags = ""
            for i in range(0, len(content) - 1):
                tags = tags + ":" + content[i]
            tags = tags.removeprefix(":")
            product = content[-1]

        # prettify everything
        product = product.replace("-", " ").title()

        print(tags)
        print(product)
        print(shade)
        print(ingredients)

    # if ingredients != None or not "auto-replenishment/" in link:
    #     ingredients = ingredients.text.strip()
    #     if len(link_parts) - products_index == 4:
    #         # it is a link thaat does not have shade separated with a /
    #         # get all the attributes into a tag
    #         tags = link_parts[products_index + 1] + ":" + link_parts[products_index + 2]
    #         # there is not a shade name
    #         product = link_parts[products_index + 3]
    #         shade = "N/A"
    #     elif len(link_parts) - products_index == 5:
    #         # it is a link thaat does not have shade separated with a /
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
    #     shade = shade.replace("-", " ").replace("_", " ").title()

    # data = ["Bobbi Brown Cosmetics", tags.strip(), product.strip(), shade.strip(), ingredients.strip(), link.strip()]

    # # write to csv
    # f = open("bobbibrown/bobbi_brown_cosmetics.csv", "a")
    # w = csv.writer(f, delimiter = ",")
    # w.writerow(data)
    # f.close()