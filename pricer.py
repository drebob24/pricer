from arg_parser import get_args
from text_generation import generate_cost_report
from file_handling import (
    get_item_list,
    save_results,
    load_watchlist,
)
from process_searches import handle_item_search
from cost_comparison import handle_cost_comparison
from watchlist_add import add_to_watchlist
from watchlist_remove import remove_from_watchlist
from watchlist_update import update_watchlist


def main():
    args = get_args()
    search_list = get_item_list(args)
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

    if args.watchlist:
        try:
            watchlist = load_watchlist("watchlist.csv")
        except FileNotFoundError:
            print("No watchlist.csv found, creating new one.")
            watchlist = []
        if args.watchlist == "add":
            new_watchlist = add_to_watchlist(watchlist, args)
        if args.watchlist == "remove":
            new_watchlist = remove_from_watchlist(watchlist, args)
        if args.watchlist == "update":
            new_watchlist = update_watchlist(watchlist, args)
        save_results(new_watchlist, args, "watchlist.csv", "watchlist")


if __name__ == "__main__":
    main()
