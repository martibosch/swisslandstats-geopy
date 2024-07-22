"""swisslandstats settings."""

import logging as lg

import requests_cache

# geometry
DEFAULT_CRS = "epsg:2056"
DEFAULT_RES = (100, 100)

DEFAULT_INDEX_COLUMN = "RELI"
DEFAULT_X_COLUMN = "E_COORD"
DEFAULT_Y_COLUMN = "N_COORD"
DEFAULT_SEP = ";"

# utils
## datasets
# DEFAULT_DATASET = "sls"
# LATEST_DATASET_URL_DICT = {
#     # 05.07.2023
#     "sls": "https://dam-api.bfs.admin.ch/hub/api/dam/assets/25885691/master",
#     # 2022
#     "statpop": "https://dam-api.bfs.admin.ch/hub/api/dam/assets/27965868/master",
#     # 2022
#     "bds": "https://dam-api.bfs.admin.ch/hub/api/dam/assets/27905171/master",
#     # 2021
#     "statent": "https://dam-api.bfs.admin.ch/hub/api/dam/assets/27245297/master",
# }
LATEST_SLS_URL = "https://dam-api.bfs.admin.ch/hub/api/dam/assets/25885691/master"
## cache
USE_CACHE = True
CACHE_NAME = "swisslandstats-cache"
CACHE_BACKEND = "sqlite"
CACHE_EXPIRE = requests_cache.NEVER_EXPIRE

## logging
LOG_CONSOLE = False
LOG_FILE = False
LOG_FILENAME = "swisslandstats"
LOG_LEVEL = lg.INFO
LOG_NAME = "swisslandstats"
LOGS_FOLDER = "./logs"
