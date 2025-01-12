from text_generation import create_results_text_list, get_discount


def process_results(results_list: list, search_input: list, args) -> list:
    sorted_list = sort_results(results_list, args.order)
    sorted_list = check_for_sales(sorted_list)
    if args.save == "csv" or args.compare == "seperate":
        sorted_list = add_search_field(sorted_list, search_input)
        return sorted_list
    cheapest_list, options_list = split_cheapest(sorted_list, args.order)
    if args.compare == "together" or args.watchlist:
        return add_search_field(cheapest_list, search_input)
    return create_results_text_list(cheapest_list, options_list, args)


def sort_results(item_list, order):
    if order == "list":
        sorted_list = sorted(
            item_list, key=lambda x: (x["list_price"], x["unit_price"], x["title"])
        )
    if order == "unit":
        sorted_list = sorted(item_list, key=lambda x: (x["unit_price"], x["title"]))
    return sorted_list


def split_cheapest(item_list, order):
    i = 0
    cheapest_price = item_list[0][f"{order}_price"]
    for item in item_list:
        if item[f"{order}_price"] > cheapest_price:
            break
        i += 1
    return item_list[0:i], item_list[i:]


def check_for_sales(item_list):
    for item in item_list:
        item["on_sale"] = item["list_price"] < item["retail_price"]
        item["discount"] = get_discount(item)
    return item_list


def add_search_field(item_list, search_term):
    for item in item_list:
        item["search"] = search_term
    return item_list
