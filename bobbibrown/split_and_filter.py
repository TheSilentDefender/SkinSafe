with open("bobbibrown/all_bb_link.txt", 'r') as f:
    text = f.read()

filtered = []

lines = text.split("http")
for i in range (1, len(lines)):
    lines[i] = "http" + lines[i]
    if ("https://www.bobbibrowncosmetics.com/product" in lines[i]):
        filtered.append(lines[i])

with open('bobbibrown/bobbi_brown_links.txt', mode='wt', encoding='utf-8') as f:
    f.write('\n'.join(filtered))
