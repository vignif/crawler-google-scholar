import argparse

import os
import sys
import pandas as pd

from get_picts import fetch as fetchpictures
from get_stats_serial import fetch as fetchserial

# Create the parser
my_parser = argparse.ArgumentParser(description='Crawl and download statistics and public pictures of researchers from google scholar')

# Add the arguments
my_parser.add_argument('file',
                       metavar='file',
                       type=str,
                       help='File path containing pairs (name, surname) of researchers')

my_parser.add_argument('-t',
                       '--type',
                       metavar='type',
                       default='serial',
                       help='type of crawler to use')

# Execute parse_args()
args = my_parser.parse_args()

input_file = args.file
crawl_type = args.type

if not os.path.isfile(input_file):
    print('The filepath specified does not exist')
    sys.exit()

if input_file.endswith('.txt'):
    df = pd.read_csv(input_file, sep=",", header=None, names=["name", "surname"])
elif input_file.endswith('.xlsx'):
    df = pd.read_excel(input_file, sheet_name=0, engine="openpyxl")
else:
    print('The filepath not in the supported file format (.txt or .xlsx)')
    sys.exit()


if __name__ == "__main__":
    if crawl_type == "picts":
        fetchpictures(df)
    elif crawl_type == "serial":
        fetchserial(df)
    # elif crawl_type == "parallel":
    #     parallel(df)
    # elif crawl_type == "coroutine":
    #     coroutine(df)
    else:
        print("Error on type of crawler requested")   


