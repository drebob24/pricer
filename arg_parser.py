import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Accepts item(s) and returns a list of products from different stores sorted by store.")
    
    parser.add_argument('-s', '--search', type=str, help='accepts an input to be searched for.')
    parser.add_argument('-o', '--order', choices=["list", "unit"], default="unit", help='choose "list" to sort by the listed item price (5 EUR/1 bag(30g)), or unit price to sort by the per per unit (ex: 10 EUR/kg).\nDefault is unit price')

    return parser.parse_args()
