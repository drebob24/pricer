from arg_parser import get_args
from process_results import generate_cost_report
from file_handling import (
    get_search_list,
    save_results,
    load_watchlist,
    delete_watchlist,
)
from process_searches import handle_item_search
from cost_comparison import handle_cost_comparison
from datetime import datetime


def main():
    """
    FURTHER FUNCTIONS:
    -Save watch list
        -Track if price goes up/down from last fetch
        -Save history of price data?
    -Create list in program (why?)

    -Make results more robust such as sorting by similarity to search term
    """
    args = get_args()
    search_list = get_search_list(args)
    if args.search:
        search_results = handle_item_search(search_list, args)
        save_results(search_results, args)

    if args.compare:
        search_results = handle_item_search(search_list, args)
        cost_data = handle_cost_comparison(search_results, args)
        report = generate_cost_report(cost_data, args)
        if args.save:
            save_results(report, args)
        else:
            print("\n" + "\n".join(report))

    if args.watch:
        try:
            watchlist = load_watchlist("watchlist.csv")
        except FileNotFoundError:
            print("No watchlist.csv found, creating new one.")
            watchlist = []
        if args.watch == "add":
            new_items = get_search_list(args)
            search_results = handle_item_search(new_items, args)
            search_results = add_timestamp(search_results)
            new_watchlist = watchlist + search_results
            save_results(new_watchlist, args)
        if args.watch == "delete":
            delete_watchlist()


def add_timestamp(item_list: list) -> list:
    for item in item_list:
        item["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return item_list


if __name__ == "__main__":
    main()
