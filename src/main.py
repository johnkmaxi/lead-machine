"""Scraping script"""

import datetime
import random

from scraper import MlsCrawler
from sources import MF_7TH_9TH_MARIGNY_BYWATER
from sources import SF_7TH_9TH_MARIGNY_BYWATER
from sources import SF_70119_70122_70124
from sources import MF_70118_70125_70113_70130_70115
from sources import SF_70118_70125_70113_70130_70115
from sources import SF_FQ
from sql_queries import leads_insert

SOURCES = [
    MF_7TH_9TH_MARIGNY_BYWATER,
    SF_7TH_9TH_MARIGNY_BYWATER,
    SF_70119_70122_70124,
    MF_70118_70125_70113_70130_70115,
    SF_70118_70125_70113_70130_70115,
    SF_FQ
]

def main():

    for source in SOURCES:
        crawler = MlsCrawler(source)
        soup = crawler.single_line_view()
        data = crawler.scrape_table_columns(soup)
        mls_nums = data['mlsnum']
        random.shuffle(mls_nums)
        # data_idxs = [x for x in range(len(data['sent']))]
        # random.shuffle(data_idxs)
        for num in mls_nums:
            listing_info = crawler.get_listing_info(num,
                                     properties=[
                                        'Property Type',
                                        'Dwelling Type',
                                        'Zip',
                                        'LP/SqFt',
                                        'Neighborhood',
                                        'DOM',
                                        'City',
                                        'Zip',
                                        'Bounding Streets',
                                        'Lot Size',
                                        'Lot Description',
                                        'Acres#',
                                        'Age'
                                    ])
            cur = crawler.to_db(
                        leads_insert,
                        params=(crawler.date,
                                data['sent'][idx],
                                data['changetype'][idx],
                                data['mlsnum'][idx],
                                data['address'][idx],
                                data['price'][idx],
                                data['beds'][idx],
                                data['fullbath'][idx],
                                data['halfbath'][idx],
                                data['agedesc'][idx],
                                data['built'][idx],
                                data['sqft'][idx],
                                listing_info['Property Type'],
                                listing_info['Dwelling Type'],
                                listing_info['City'],
                                int(listing_info['Zip']),
                                crawler.format_money(listing_info['LP/SqFt']),
                                listing_info['Neighborhood'],
                                crawler.format_money(listing_info['DOM']),
                                listing_info['Bounding Streets'],
                                listing_info['Lot Size'],
                                listing_info['Lot Description'],
                                listing_info['Acres#'],
                                listing_info['Age'])
                    )
            crawler.conn.commit()
        crawler.conn.close()
        # close http connection

if __name__ == '__main__':
    main()
