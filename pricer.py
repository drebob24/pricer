from arg_parser import get_args
from file_handling import (
    get_item_list,
    save_results,
    load_watchlist,
)
from process_searches import handle_item_search
from cost_comparison import create_comparison_report
from watchlist_add import add_to_watchlist, remove_items
from watchlist_update import update_watchlist


def main():
    args = get_args()
    item_input_list = get_item_list(args)
    if args.search:
        search_results = handle_item_search(item_input_list, args)
        save_results(search_results, args)

    if args.compare:
        report = create_comparison_report(item_input_list, args)
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
            new_watchlist = add_to_watchlist(watchlist, item_input_list, args)
        if args.watchlist == "remove":
            new_watchlist = remove_items(watchlist, item_input_list)
        if args.watchlist == "update" or args.search_watchlist:
            new_watchlist = update_watchlist(watchlist, args)
        save_results(new_watchlist, args, "watchlist.csv", "watchlist")


if __name__ == "__main__":
    main()
