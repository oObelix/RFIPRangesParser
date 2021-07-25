from typing import List, Set, Dict, Tuple, Optional
import requests
from lxml import html
import argparse
from db_init import update_collected_data

URL_PARSE = "https://lite.ip2location.com/russian-federation-ip-address-ranges"
XPATH_BEGIN_IP_ADDRESS = ".//table[@id='ip-address']/tbody/tr/td[2]/text()"
XPATH_END_IP_ADDRESS = ".//table[@id='ip-address']/tbody/tr/td[4]/text()"
XPATH_TOTAL_COUNT = ".//table[@id='ip-address']/tbody/tr/td[6]/text()"


def print_console(*lists: List[Tuple]) -> None:
    """
    Print table of lists
    :param lists: List[Tuple]
    :return: None
    """
    for line in zip(*lists):
        print("\t".join(line))


def add_to_db(
        _begin_ip_address: list,
        _end_ip_address: list,
        _total_count: list
):
    print('Added to Db')
    update_collected_data(zip(_begin_ip_address, _end_ip_address, _total_count))


request = requests.get(URL_PARSE)
html_parse: str = request.text

parse_tree = html.fromstring(html_parse)

begin_ip_address: list = parse_tree.xpath(XPATH_BEGIN_IP_ADDRESS)
end_ip_address: list = parse_tree.xpath(XPATH_END_IP_ADDRESS)
total_count: list = parse_tree.xpath(XPATH_TOTAL_COUNT)

args = argparse.ArgumentParser()
args.add_argument('--dry_run')
namespace = args.parse_args()
if namespace.dry_run == 'True':
    print_console(begin_ip_address, end_ip_address, total_count)
else:
    add_to_db(begin_ip_address, end_ip_address, total_count)
