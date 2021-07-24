import requests
from lxml import html
import argparse
from db_init import update_collected_data

url_parse: str = "https://lite.ip2location.com/russian-federation-ip-address-ranges"
xpath_begin_ip_address: str = ".//table[@id='ip-address']/tbody/tr/td[2]/text()"
xpath_end_ip_address: str = ".//table[@id='ip-address']/tbody/tr/td[4]/text()"
xpath_total_count: str = ".//table[@id='ip-address']/tbody/tr/td[6]/text()"


def print_console(
        _begin_ip_address: list,
        _end_ip_address: list,
        _total_count: list
):
    print(f"id\t| begin_ip_address\t| end_ip_address\t| total_count\t")
    for i, line in enumerate(zip(_begin_ip_address,
                                 _end_ip_address,
                                 _total_count)):
        print(f"{i}\t| {line[0]}\t| {line[1]}\t| {line[2]}\t")


def add_to_db(
        _begin_ip_address: list,
        _end_ip_address: list,
        _total_count: list
):
    print('Added to Db')
    update_collected_data(zip(_begin_ip_address, _end_ip_address, _total_count))


request = requests.get(url_parse)
html_parse: str = request.text

parse_tree = html.fromstring(html_parse)

begin_ip_address: list = parse_tree.xpath(xpath_begin_ip_address)
end_ip_address: list = parse_tree.xpath(xpath_end_ip_address)
total_count: list = parse_tree.xpath(xpath_total_count)

args = argparse.ArgumentParser()
args.add_argument('--dry_run')
namespace = args.parse_args()
if namespace.dry_run == 'True':
    print_console(begin_ip_address, end_ip_address, total_count)
else:
    add_to_db(begin_ip_address, end_ip_address, total_count)
