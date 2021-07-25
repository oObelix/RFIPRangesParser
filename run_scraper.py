from typing import List, Set, Dict, Tuple, Optional, Any
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


if __name__ == "__main__":
    request: Any = requests.get(URL_PARSE)
    html_parse: str = request.text

    parse_tree: Any = html.fromstring(html_parse)

    begin_ip_address: List = parse_tree.xpath(XPATH_BEGIN_IP_ADDRESS)
    end_ip_address: List = parse_tree.xpath(XPATH_END_IP_ADDRESS)
    total_count: List = parse_tree.xpath(XPATH_TOTAL_COUNT)

    args: Any = argparse.ArgumentParser()
    args.add_argument('--dry_run')
    namespace: Any = args.parse_args()

    if namespace.dry_run == 'True':
        print_console(begin_ip_address, end_ip_address, total_count)
    else:
        update_collected_data(zip(begin_ip_address, end_ip_address, total_count))
