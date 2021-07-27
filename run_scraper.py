from typing import List, Tuple, Any
import requests
from lxml import html
import argparse
from db_session import session
from models import CollectedData


URL_PARSE = "https://lite.ip2location.com/russian-federation-ip-address-ranges"
XPATH_BEGIN_IP_ADDRESS = ".//table[@id='ip-address']/tbody/tr/td[2]/text()"
XPATH_END_IP_ADDRESS = ".//table[@id='ip-address']/tbody/tr/td[4]/text()"
XPATH_TOTAL_COUNT = ".//table[@id='ip-address']/tbody/tr/td[6]/text()"
REQUESTS_HEADERS = {'Cache-Control': "no-cache",
                    'User-Agent': "Mozilla/5.0 (Macintosh; Intel "
                                  "Mac OS X 10_15_7) AppleWebKit/605.1.15 "
                                  "(KHTML, like Gecko) Version/14.1.2 "
                                  "Safari/605.1.15"}


def print_console(*lists: List[Tuple]) -> None:
    """
    Print table of lists
    :param lists: List[Tuple]
    :return: None
    """
    for line in zip(*lists):
        print("\t".join(line))


if __name__ == "__main__":
    request: Any = requests.get(URL_PARSE,
                                headers=REQUESTS_HEADERS,
                                allow_redirects=True)
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
        CollectedData.update_collected_data(session,
                                            begin_ip_address,
                                            end_ip_address,
                                            total_count)
