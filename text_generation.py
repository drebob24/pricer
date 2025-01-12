def get_discount(item: dict) -> int:
    discount_amount = (1 - item["list_price"] / item["retail_price"]) * 100
    return int(round(discount_amount))


def create_cheapest_output(items):
    if len(items) == 1:
        return f"The cheapest item is:\n{items[0]}\n"
    else:
        return f"The cheapest items are:\n{"\n".join(items)}\n"


def create_options_output(options):
    options_text = "\n".join(options)
    return f"\nOther options:\n{options_text}"


def generate_cost_report(cost_data: list, args) -> list:
    report = []
    sorted_data = sorted(cost_data, key=lambda x: x["cost"])
    report += [
        f"The Cheapest Total Cost for the Shopping List is: {sorted_data[0]["cost"]} €"
    ]
    if sorted_data[0]["store"] != "both":
        report[-1] += f" from {sorted_data[0]["store"]}."
        report += [
            f"Total Cost is {sorted_data[1]["cost"]} € at {sorted_data[1]["store"]}."
        ]
    for data in sorted_data:
        report += generate_item_text(data["items"], args)
    return report


def generate_update_report(item_list: list, args) -> list:
    report = []
    report.append("Watchlist Update:")
    report += generate_item_text(item_list, args)
    return report


def generate_item_text(item_list, args):
    if args.compare:
        barbora = []
        rimi = []
        for item in item_list:
            if item["store"] == "Barbora":
                barbora += [format_total_item(item)]
            if item["store"] == "Rimi":
                rimi += [format_total_item(item)]
        if barbora:
            barbora = ["Babora:"] + barbora
        if rimi:
            rimi = ["Rimi:"] + rimi
        return barbora + rimi
    if args.search:
        return [format_search_item(item) for item in item_list]
    if args.watchlist == "update":
        return [format_update_item(item) for item in item_list]


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


def format_update_item(item):
    if item["on_sale"]:
        sale_info = f" -{get_discount(item)}% SALE"
    else:
        sale_info = ""
    return f"{item['search']}: {item['title']}: {item['list_price']} € ({item['unit_price']} €/{item['unit']}){sale_info}\nPrice change: {item["percent_change"]}%"


def create_results_text_list(cheapest_list, options_list, args):
    cheapest_list = generate_item_text(cheapest_list, args)
    options_list = generate_item_text(options_list, args)
    cheapest_text = create_cheapest_output(cheapest_list)
    options_text = create_options_output(options_list)
    return [cheapest_text + options_text]
