#!/usr/bin/env python

# ua_borderpoints
# # MIT License
# Copyright (c) 2023 Michael John <michael.john@gmx.at>

import time
import argparse
import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    pass
from prettytable import from_html, from_csv, from_json, \
    PLAIN_COLUMNS, ORGMODE, SINGLE_BORDER, DOUBLE_BORDER  # noqa: F401
from tabulate import tabulate
import pandas as pd

PROGNAME = "ua_borderpoints"
VERSION = "0.1.0"
AUTHOR = "Copyright (C) 2023, by Michael John"
DESC = "Fetch and show data from the State Customs Service of Ukraine at kordon.customs.gov.ua"  # noqa: E501

def build_url(lang='uk', country='pl', direction='o'):
    if lang is None or lang == "":
        lang = "en"
    if country is None or country == "":
        country = 'pl'
    if direction is None or direction == "":
        direction = "o"
    if direction in ["in", "i", "entry", "entering"]:
        direction = "i"
    if direction in ["out", "o", "exit", "exiting"]:
        direction = "o"
    url = f"https://kordon.customs.gov.ua/{lang}/home/countries/{country}/{direction}"
    return url

def get_data_rq(url, quiet=False):
    if not quiet:
        print(f"Fetching {url}")
    response = requests.get(url)
    return response.text

def get_data_pd(url, quiet=False):
    if not quiet:
        print(f"Fetching {url}")
    tb_df = pd.read_html(url, skiprows=1, header=0, flavor=["lxml"])[0]
    # tb1 = tb[["Cross border point", "Passenger vehicle", "Cargo vehicle"]]
    tb_df = tb_df.iloc[:, 0:3]  # this will work even for foreign languages
    pd.set_option('display.max_colwidth', 120)
    pd.set_option('display.colheader_justify', 'left')
    tb_df = tb_df.fillna('N/A', inplace=False)  # avoid SettingWithCopyWarning
    return tb_df

def _parse_data(data, table_id):
    """Read the data 
    """
    soup = BeautifulSoup(data, 'lxml')
    htmltable = soup.find('table', { 'class' : 'responsive' })
    table = from_html(str(htmltable))
    # table.del_row(0)
    return table

def main():
    start = time.time()

    parser = argparse.ArgumentParser(prog=PROGNAME, description=DESC)
    parser.add_argument('-l', '--language', dest='language', 
        help='what language to use in output', type=str, 
        required=False, choices=['uk', 'en', 'ru', 'hu', 'pl', 'ro', 'sk'])
    parser.add_argument('-c', '--country', dest='country', 
        help='search for country, i.e. `RO` or `ro` for `Romania`', type=str, 
        required=True, choices=['md', 'ro', 'hu', 'sk', 'pl', 'by', 'ru', 'kr'])
    parser.add_argument('-d', '--direction', dest='direction', 
        help='specify a direction, i.e. `entry` or `exit`', type=str)
    parser.add_argument('-q', '--quiet', 
        help='suppress output', action='store_true')
    parser.add_argument('-f', '--format', 
        help='output format [tab (default)|pandas|json|csv]', type=str)
    parser.add_argument('-v', '--version', action='version', 
        version='%(prog)s ' + VERSION + ' ' + AUTHOR)

    args = parser.parse_args()
    language = vars(args)["language"]
    country = vars(args)["country"]
    direction = vars(args)["direction"]
    quiet = vars(args)["quiet"]
    format = vars(args)["format"] or "tab"
    if not quiet:
        print(str(args).replace("Namespace", "Options"))
    
    # data = get_data_rq(build_url(language, country, direction), quiet)
    data = get_data_pd(build_url(language, country, direction), quiet)
    
    if format == "tab":
        print(tabulate(data, showindex=False, headers=data.columns))
    if format == "csv":
        print(data.to_csv(quotechar="'", doublequote=True, escapechar="\\"))
    if format == "pandas":
        print(data)
    if format == "json":
        print(data.to_json(orient="records", indent=4, force_ascii=False))
    if format == "pt":
        parsed = from_json(data.to_json(orient="records"))
        # parsed.set_style(SINGLE_BORDER)
        print(parsed)

    end = time.time()
    if not quiet:
        print('[{:2.3} seconds elapsed]'.format((end - start)))
        rowcount = data.shape[0]
        if rowcount > 0:
            print(f"Number of results: {rowcount}")
        else:
            print("No results for search criteria.")


if __name__ == "__main__":
    main()
