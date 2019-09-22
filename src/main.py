"""Scraping script"""

import datetime

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
        for idx in range(len(data['sent'])):
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
                                data['sqft'][idx])
                    )
            crawler.conn.commit()

if __name__ == '__main__':
    main()
