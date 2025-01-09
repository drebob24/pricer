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
        rimi_list = get_rimi(args.search)
        full_list = sort_lists(barbora_list, rimi_list)
        cheapest, options_list = generate_results(full_list)
        print(create_cheapest_text(cheapest))
        print(create_options_text(options_list))


def sort_lists(list_a, list_b):
    sorted_list = sorted(list_a + list_b, key=lambda x: (x["list_price"],
                                                         x["unit_price"],
                                                         x["title"]))
    return sorted_list


def generate_results(item_list):
    info = [f"{item["title"]}:\n{item["list_price"]} € at {item["store"]}" for item in item_list]
    return info[0], info[1:]


def create_cheapest_text(item):
    return f"The cheapest item is:\n{item}\n"


def create_options_text(options):
    options_text = "\n".join(options)
    return f"Other options:\n{options_text}"





if __name__ == "__main__":
    main()