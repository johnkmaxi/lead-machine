"""Real estate lead data sources

"""

import configparser

config = configparser.ConfigParser()
config.read(conn_info)

MLS_SEARCHES = config['SOURCES']['MLS_SEARCHES']
SF_FQ = config['SOURCES']['SF_FQ']
MF_7TH_9TH_MARIGNY_BYWATER = config['SOURCES']['MF_7TH_9TH_MARIGNY_BYWATER']
SF_7TH_9TH_MARIGNY_BYWATER = config['SOURCES']['SF_7TH_9TH_MARIGNY_BYWATER']
# MF_70114_70131 = "https://nom.mlsmatrix.com/Matrix/Public/Portal.aspx?L=1&k=426296XQ23D&p=AE-293661-290"
# SF_70114_70131 = "https://nom.mlsmatrix.com/Matrix/Public/Portal.aspx?L=1&k=426296XQ23D&p=AE-293660-417"
# MF_70119_70122_70124 = "https://nom.mlsmatrix.com/Matrix/Public/Portal.aspx?L=1&k=426296XQ23D&p=AE-293659-109"
SF_70119_70122_70124 = config['SOURCES']['SF_70119_70122_70124']
MF_70118_70125_70113_70130_70115 = config['SOURCES']['MF_70118_70125_70113_70130_70115']
SF_70118_70125_70113_70130_70115 = config['SOURCES']['SF_70118_70125_70113_70130_70115']
