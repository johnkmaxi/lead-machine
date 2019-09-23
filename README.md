# Lead Machine

Lead machine is a program for finding information about properties listed on the
MLS. The parts of the lead machine are a Crawler, an Analyzer, and a DB.
Together, these parts accept a variety of data sources from which they obtain
the necessary information, store it, analyze it, and output a list of properties
and the contact information for each property. This list acts as a daily to-do
list for driving wholesaling KPIs.

## Crawler
The purpose of the crawler is to extract information from web-based data sources.
Identified sources include:
- Realtor-created MLS search portal
- Zillow
- Realtor.com
- Redfin
- Trulia
- Craigslist

## DB

## Analyzer

## Usage
1. Clone conda lema env
2. Put lead-machine in Users directory
3. Run src/tests.py
4. Run src/create_tables.py
5. Add move geckodriver to file location of your choice. Add it to PATH
6. Run src/main.py
7. Schedule src/main.py to run on a schedule using Task Scheduler (Windows)
