from arg_parser import get_args
from barbora import get_barbora
from rimi import get_rimi
from process_results import process_results
import time
import random


def main():
    '''
    FURTHER FUNCTIONS:
    -Save watch list
        -Track if price goes up/down from last fetch
        -Save history of price data?
    -Create list in program

    -Make results more robust such as sorting by similarity to search term    
    '''
    args = get_args()

    if args.items:
        search_list = args.items
    if args.file:
        search_list = read_item_file(args.file)

    if args.search:
        max_items = 10
        if len(search_list) > max_items:
            raise ValueError(f"Error: At most {max_items} items may be searched per instance.")
        print("Searching for items...")
            
        for item in search_list:
            barbora_list = get_barbora(item, args.results)
            print(f"\nBarbora search '{item}' completed")
            rimi_list = get_rimi(item, args.results)
            print(f"Rimi search '{item}' completed\n")
            if barbora_list or rimi_list:
                cheapest_items, options = process_results(barbora_list + rimi_list, args.order)
                print(cheapest_items)
                print(options)
            else:
                print(f"No Results for search: '{item}'")
            time.sleep(random.randint(2,5))


def read_item_file(file_path: str) -> list:
    with open(file_path, "r") as f:
        items = [line.strip() for line in f]
    return items


if __name__ == "__main__":
    main()