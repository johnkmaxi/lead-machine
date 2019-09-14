
"""

Author: John Maxi
Date: 2019-09-14
"""

tables = ['LEADS']

columns = {
'LEADS':"""(
    ID SERIAL NOT NULL,
    APPEARED_DATE timestamp,
    CHANGE_TYPE varchar,
    MSL_NUM int,
    ADDRESS varchar,
    CURRENT_PRICE int,
    BEDS int,
    FULL_BATHS int,
    HALF_BATHS int,
    AGE_DESC varchar,
    YR_BLT int,
    SQ_FEET_LV int
    )"""
}

leads_insert = ("""
INSERT INTO LEADS(APPEARED_DATE, CHANGE_TYPE, MSL_NUM, ADDRESS, CURRENT_PRICE, BEDS, FULL_BATHS, HALF_BATHS, AGE_DESC, YR_BLT, SQ_FEET_LV)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
""")
