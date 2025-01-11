from arg_parser import get_args
from barbora import get_barbora
from rimi import get_rimi
from process_results import process_results
from file_handling import read_item_file, write_results_txt, write_results_csv
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
        search_results = []
        for item in search_list:
            barbora_list = get_barbora(item, args.results)
            print(f"\nBarbora search '{item}' completed")
            rimi_list = get_rimi(item, args.results)
            print(f"Rimi search '{item}' completed\n")
            if barbora_list or rimi_list:
                sorted_results = process_results(barbora_list + rimi_list, item, args.order, args.save)
                if args.save == "csv":
                    search_results += sorted_results
                    time.sleep(random.randint(2,5))
                    continue
                search_results.append(f"Results for '{item}':\n")
                search_results.append(sorted_results)
            else:
                search_results.append(f"No Results for search: '{item}'")
            if not args.save:
                print("\n".join(search_results))
            time.sleep(random.randint(2,5))


    if args.save == "txt":
        write_results_txt(search_results)


    if args.save == "csv":
        write_results_csv(search_results)


if __name__ == "__main__":
    main()