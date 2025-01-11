from arg_parser import get_args
from process_results import generate_cost_report
from file_handling import get_search_list, save_results
from process_searches import handle_item_search
from cost_comparison import handle_cost_comparison


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
    if args.mode == "search":
        search_results = handle_item_search(search_list, args)
        save_results(search_results, args.save)
    if args.compare:
        search_results = handle_item_search(search_list, args)
        cost_data = handle_cost_comparison(search_results, args)
        report = generate_cost_report(cost_data, args)
        if args.save:
            save_results(report, args.save)
        else:
            print("\n" + "\n".join(report))


if __name__ == "__main__":
    main()
