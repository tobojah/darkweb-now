import requests
from bs4 import BeautifulSoup
import logging

    """Logging all to files"""
def setup_logging():
    """Setup logging  configuration , read logs."""
    logging.basicConfig(filename='script_log.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def check_tor_connection(proxies):
    """Check if the connection is through Tor and log the details."""
    logging.info("Tor Connection Check")
    try:
        system_ip = requests.get('https://ident.me', proxies=proxies).text
        tor_ip_list = requests.get('https://check.torproject.org/exit-addresses').text
            """Check tor ip list."""
        if system_ip in tor_ip_list:
            logging.info(f'Tor_IP: {system_ip}')
            logging.info("Tor Connection Success")
        else:
            logging.error('IP not in Tor exit node list')
            return False
    except Exception as e:
        logging.error(f"Error establishing Tor connection: {e}")
        return False
    return True

def read_url_file(filename):
    """Read URLs from a file."""
    try:
        with open(filename, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        logging.error("File not found")
        return None

def scrape_urls(urls, proxies):
    """Web Scraping through Tor for a list of URLs. Don't forget one url per line"""
    for url in urls:
        url = url.strip()
        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                page_title = soup.title.string if soup.title else 'No title'
                logging.info(f'Active: {url} - {page_title}')
            else:
                logging.info(f'Inactive (HTTP {response.status_code}): {url}')
        except requests.RequestException as e:
            logging.error(f'Error accessing {url}: {e}')

def main():
    setup_logging()

    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    if not check_tor_connection(proxies):
        return

    in_file = input("Submit the URL File: ")
    urls = read_url_file(in_file)
    if urls is not None:
        scrape_urls(urls, proxies)

if __name__ == "__main__":
    main()
