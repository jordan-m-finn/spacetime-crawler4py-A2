from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
from scraper import print_summary, load_crawler_data, save_crawler_data

import multiprocessing
multiprocessing.set_start_method("fork")


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    
    # Load any existing crawler data before starting
    if not restart:
        load_crawler_data()
    
    crawler = Crawler(config, restart)
    crawler.start()
    
    # Save crawler data after crawling is done
    save_crawler_data()
    
    # Generate the summary
    print_summary() 


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)
