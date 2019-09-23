
"""

Author: John Maxi
Date: 2019-09-14
"""

testtables = ['TESTLEADS']

testcolumns = {
'TESTLEADS':"""(
    ID SERIAL NOT NULL,
    SCRAPE_DATE timestamp,
    APPEARED_DATE timestamp,
    CHANGE_TYPE varchar,
    MLS_NUM int,
    ADDRESS varchar,
    CURRENT_PRICE int,
    BEDS int,
    FULL_BATHS int,
    HALF_BATHS int,
    AGE_DESC varchar,
    YR_BLT int,
    SQ_FEET_LV int,
    PRIMARY KEY (APPEARED_DATE, ADDRESS)
    )"""
}

tables = ['LEADS']

columns = {
'LEADS':"""(
    ID SERIAL NOT NULL,
    SCRAPE_DATE timestamp,
    APPEARED_DATE timestamp,
    CHANGE_TYPE varchar,
    MLS_NUM int,
    ADDRESS varchar,
    CURRENT_PRICE int,
    BEDS int,
    FULL_BATHS int,
    HALF_BATHS int,
    AGE_DESC varchar,
    YR_BLT int,
    SQ_FEET_LV int,
    PRIMARY KEY (APPEARED_DATE, ADDRESS)
    )"""
}

leads_insert = ("""
INSERT INTO LEADS(SCRAPE_DATE, APPEARED_DATE, CHANGE_TYPE, MLS_NUM, ADDRESS, CURRENT_PRICE, BEDS, FULL_BATHS, HALF_BATHS, AGE_DESC, YR_BLT, SQ_FEET_LV)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
""")
