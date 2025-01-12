import argparse
import sys


def validate_args(args):
    if args.compare and args.save == "csv":
        print(
            "Error: Saving as CSV is not compatible with --total. Please choose a different save option."
        )
        sys.exit(2)
    if args.search and not args.items and not args.file and not args.search_watchlist:
        print(
            "Error: Search feature requires an input of search items using either --items, --file, or --search-watchlist."
        )
        sys.exit(2)
    if (
        (args.watchlist == "add" or args.watchlist == "remove")
        and not args.items
        and not args.file
    ):
        print(
            "Error: Adding or Removing items from watchlist requires an input of items using either --items or --file."
        )
        sys.exit(2)


def get_args():
    parser = argparse.ArgumentParser(
        description="Accepts item(s) and returns a list of products from different stores sorted by price."
    )

    item_group = parser.add_mutually_exclusive_group()

    item_group.add_argument(
        "-i",
        "--items",
        type=str,
        nargs="+",
        help="Accepts a list of string values. Ex: --items item1 item2 item3\n Currently limited to 10 items.",
    )
    item_group.add_argument(
        "-f",
        "--file",
        type=validate_input_file,
        help="Accepts a file path to load in a list of items. Expects a txt file.\n Currently limited to 10 items.",
    )
    item_group.add_argument(
        "--search-watchlist",
        action="store_true",
        help="Load list of items from watchlist to perform search or compare."
    )

    feature_group = parser.add_mutually_exclusive_group(required=True)

    feature_group.add_argument(
        "-s",
        "--search",
        action="store_true",
        help="Runs a basic search and return results mode for each individual item.",
    )
    feature_group.add_argument(
        "--compare",
        type=str,
        choices=["together", "seperate"],
        help="Run a total cost comparison either combining prices across both stores with 'together, or 'seperate' gives total cost per store seperately.",
    )
    feature_group.add_argument(
        "--watchlist",
        type=str,
        choices=["add", "update", "remove"],
        help="Create/Add to a watchlist using 'add' and either the --items or --file argument to pass in items. 'update' will update the watchlist with the optionn to store old data with the '--store-history' arg. Remove items from the watchlist with 'remove' and the --items or --file argument.",
    )
    parser.add_argument(
        "--order",
        type=str,
        choices=["list", "unit"],
        default="unit",
        help='Choose "list" to sort by the listed item price (5 EUR/1 bag(30g)), or unit price to sort by the price per unit (ex: 10 EUR/kg).\nDefault is unit price.',
    )
    parser.add_argument(
        "--results",
        type=int,
        default=3,
        help="Expects an int value for how many results to return. Results will also be limited by what the source returns.\nWarning, the more results you add the more likely you are to find unwanted items.\nDefault amount is 3.",
    )
    parser.add_argument(
        "--save",
        type=str,
        choices=["txt", "csv"],
        help="Saves results as either TXT, or in a CSV. CSV is not compatible with compare mode due to the resulting data.",
    )
    parser.add_argument(
        "--store-history",
        action="store_true",
        help="Flag to store historical data when updating watchlist with '--watch update'.",
    )

    args = parser.parse_args()
    validate_args(args)
    return args


def validate_input_file(filename):
    if filename.endswith("txt"):
        return filename
    else:
        raise argparse.ArgumentTypeError(f"{filename} is not a valid .txt file")
