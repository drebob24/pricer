import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description="Accepts item(s) and returns a list of products from different stores sorted by price."
    )
    
    item_group = parser.add_mutually_exclusive_group(required=True)
    
    item_group.add_argument(
        "--items",
        nargs="+",
        help="Accepts a list of items. Ex: --items item1 item2 item3\n Currently limited to 10 items.",
    )
    item_group.add_argument(
        "-f",
        "--file",
        type=validate_input_file,
        help="Accepts a file path to load in a list of items. Expects a txt file.\n Currently limited to 10 items",
    )   
    parser.add_argument(
        "-s",
        "--search",
        action="store_true",
        help="Run search mode for provided items.",
    )
    parser.add_argument(
        "--order",
        choices=["list", "unit"],
        default="unit",
        help='Choose "list" to sort by the listed item price (5 EUR/1 bag(30g)), or unit price to sort by the per per unit (ex: 10 EUR/kg).\nDefault is unit price',
    )
    parser.add_argument(
        "--results",
        type=int,
        default=3,
        help="Expects an int value for how many results to return. Warning, the more results you add the more likely you are to find unwanted items.\nDefault amount is 3."
    )
    parser.add_argument(
        "--save",
        type=str,
        help = "Saves results to designated file path in a txt file."
    )
      
    return parser.parse_args()


def validate_input_file(filename):
    if filename.endswith("txt"):
        return filename
    else:
        raise argparse.ArgumentTypeError(f"{filename} is not a valid .txt file")