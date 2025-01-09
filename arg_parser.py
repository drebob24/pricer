import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Accepts item(s) and returns a list of products from different stores sorted by store.")
    
    parser.add_argument('-s', '--search', type=str, help='accepts an input to be searched for')

    return parser.parse_args()
