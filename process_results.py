def process_results(results_list, search_input, args):
    sorted_list = sort_results(results_list, args.order)
    sorted_list = check_for_sales(sorted_list)
    if args.save == "csv" or (args.mode == "total" and args.compare == "seperate"):
        sorted_list = add_search_field(sorted_list, search_input)
        return sorted_list
    cheapest_list, options_list = split_cheapest(sorted_list, args.order)
    if args.mode == "total" and args.compare == "together":
        return add_search_field(cheapest_list, search_input)
    cheapest_list, options_list = generate_item_text(cheapest_list, args.mode), generate_item_text(options_list, args.mode)
    cheapest_text = create_cheapest_output(cheapest_list)
    options_text = create_options_output(options_list)
    return [cheapest_text + options_text]


def sort_results(item_list, order):
    if order == "list":
        sorted_list = sorted(item_list, key=lambda x: (x["list_price"],
                                                            x["unit_price"],
                                                            x["title"]))
    if order == "unit":
        sorted_list = sorted(item_list, key=lambda x: (x["unit_price"],
                                                            x["title"]))
    return sorted_list


def split_cheapest(item_list, order):
    i = 0
    cheapest_price = item_list[0][f"{order}_price"]
    for item in item_list:
        if item[f"{order}_price"] > cheapest_price:
            break
        i += 1
    return item_list[0:i], item_list[i:]


def generate_item_text(item_list, mode):
    if mode == "search":
        return [format_search_item(item) for item in item_list]
    if mode == "total":
        barbora = ["Babora:"]
        rimi = ["Rimi:"]
        for item in item_list:
            if item["store"] == "Barbora":
                barbora += [format_total_item(item)]
            if item["store"] == "Rimi":
                rimi += [format_total_item(item)]
        return barbora + rimi


def format_search_item(item):
    if item["on_sale"]:
        sale_info = f" -{get_discount(item)}% SALE" 
    else:
        sale_info = ""
    return f"{item['title']}:\n{item['list_price']} € ({item['unit_price']} €/{item['unit']}) at {item['store']}{sale_info}"


def format_total_item(item):
    if item["on_sale"]:
        sale_info = f" -{get_discount(item)}% SALE" 
    else:
        sale_info = ""
    return f"{item['search']}: {item['title']}: {item['list_price']} € ({item['unit_price']} €/{item['unit']}){sale_info}"


def check_for_sales(item_list):
    for item in item_list:
        item["on_sale"] = item["list_price"] < item["retail_price"]
        item["discount"] = get_discount(item)
    return item_list
    

def get_discount(item):
    discount_amount = (1 - item["list_price"]/item["retail_price"]) * 100
    return int(round(discount_amount))


def create_cheapest_output(items):
    if len(items) == 1:
        return f"The cheapest item is:\n{items[0]}\n"
    else:
        return f"The cheapest items are:\n{"\n".join(items)}\n"
    

def create_options_output(options):
    options_text = "\n".join(options)
    return f"\nOther options:\n{options_text}"


def add_search_field(item_list, search_term):
    for item in item_list:
        item["search"] = search_term
    return item_list