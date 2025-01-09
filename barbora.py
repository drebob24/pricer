import requests
import json
import re
from bs4 import BeautifulSoup


def grab_barbora_products():
    response = requests.get("https://barbora.lt/paieska?q=mint")
    soup_data = BeautifulSoup(response.text, "html.parser")
    return soup_data


def extract_barbora_items(raw_data):
    raw_data = raw_data.find("script", string=re.compile(r"window\.b_productList"))
    if raw_data:
        page_content = raw_data.string
        pattern = r"window\.b_productList\s*=\s*(.*);"
        match = re.search(pattern, page_content)
    items = match.group(1)
    return json.loads(items)


def parse_barbora_data(products, amount=5):
    '''
    amount is for future proofing if functionality to allow the user to choose how many items to grab is added.
    Would need to be capped at 52 because that's how many items are returned per page
    '''
    items = []
    i = 0
    for product in products:
        #Only want the first 5 listed (in stock) items
        if i > amount-1:
            break
        item = {}
        if product["status"] == "suspended":
            #Skip product if sold out
            continue
        item["title"] = product["title"]
        item["list_price"] = product["units"][0]["price"]
        try:
            item["retail_price"] = product["units"][0]["retail_price"]
        except KeyError:
            #If no retail_price exists, then item not on sale and retail_price = listed_price
            item["retail_price"] = product["units"][0]["price"]
        item["unit_price"] = product["comparative_unit_price"]
        item["unit"] = product["comparative_unit"]
        item["store"] = "Barbora"
        items.append(item)
        i += 1
    return items


def get_barbora():
    page_data = grab_barbora_products()
    product_list = extract_barbora_items(page_data)
    cleaned_list = parse_barbora_data(product_list)
    print_html(cleaned_list)


def print_html(html):
    with open("barbora_items.json", "w") as save:
        json.dump(html, save, indent=2)


if __name__ == "__main__":
    get_barbora()
