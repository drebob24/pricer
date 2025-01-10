from arg_parser import get_args
from barbora import get_barbora
from rimi import get_rimi


def main():
    '''
    -Get User Input
    (command line program)

    -Grab data for item

    -Sort data

    -Return items


    FURTHER FUNCTIONS:
    -Import list of items
    -Choose to sort by list price or unit price
    -Save watch list
        -Track if price goes up/down from last fetch
        -Save history of price data?
    -Create list in program

    -Make results more robust such as sorting by similarity to search term    
    '''
    args = get_args()

    if args.search:
        barbora_list = get_barbora(args.search)
        print("Barbora search completed")
        rimi_list = get_rimi(args.search)
        print("Rimi search completed\n")
        cheapest_list, options_list = sort_lists(barbora_list, rimi_list, args.order)
        cheapest_list, options_list = generate_item_text(cheapest_list), generate_item_text(options_list)
        print(create_cheapest_output(cheapest_list))
        print(create_options_output(options_list))


def sort_lists(list_a, list_b, order):
    if order == "list":
        sorted_list = sorted(list_a + list_b, key=lambda x: (x["list_price"],
                                                            x["unit_price"],
                                                            x["title"]))
    if order == "unit":
        sorted_list = sorted(list_a + list_b, key=lambda x: (x["unit_price"],
                                                            x["title"]))
    i = 0
    cheapest_price = sorted_list[0][f"{order}_price"]
    for item in sorted_list:
        if item[f"{order}_price"] > cheapest_price:
            break
        i += 1
    return sorted_list[0:i], sorted_list[i:]


def generate_item_text(item_list):
    return [f"{item["title"]}:\n{item["list_price"]} € ({item["unit_price"]} €/{item["unit"]}) at {item["store"]}" for item in item_list]


def create_cheapest_output(items):
    if len(items) == 1:
        return f"The cheapest item is:\n{"\n".join(items)}\n"
    else:
        return f"The cheapest items are:\n{"\n".join(items)}\n"
    

def create_options_output(options):
    options_text = "\n".join(options)
    return f"Other options:\n{options_text}"




if __name__ == "__main__":
    main()