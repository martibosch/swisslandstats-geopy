"""swisslandstats settings."""

import logging as lg

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
# define hashes here to avoid long lines
_sls_known_hash = "059307949698805030c3cc1f9e99fe4db73406bc21b848faf823e90e0ba68626"
_statpop_known_hash = "80d9bccece07467e03872ceb642c6adfcc0472232d549fb1b37f988c1a919678"
_bds_known_hash = "ade605c6b843b2fce12b99d67fdb0594f2508498c6009c949dffa108ea74a533"
_statent_known_hash = "969b439be04b2699da6bcf1dd1f47b3f386352259e9f12f83c787b4c56d2c962"
DATASET_DICT = {
    "sls": {
        "latest": "2024",
        "2024": {
            "url": "https://dam-api.bfs.admin.ch/hub/api/dam/assets/32376216/master",
            "known_hash": _sls_known_hash,
            "zip": False,
            "read_csv_kwargs": {},
        },
    },
    "statpop": {
        "latest": "2023",
        "2023": {
            "url": "https://dam-api.bfs.admin.ch/hub/api/dam/assets/32686751/master",
            "known_hash": _statpop_known_hash,
            "zip": True,
            "members": "ag-b-00.03-vz2023statpop/STATPOP2023.csv",
            "which_member": 0,
            "read_csv_kwargs": {"x_column": "E_KOORD", "y_column": "N_KOORD"},
        },
    },
    "bds": {
        "latest": "2023",
        "2023": {
            "url": "https://dam-api.bfs.admin.ch/hub/api/dam/assets/32411359/master",
            "known_hash": _bds_known_hash,
            "zip": True,
            "members": "ag-b-00.03-vz2023gws/GWS2023.csv",
            "which_member": 0,
            "read_csv_kwargs": {
                "x_column": "E_KOORD",
                "y_column": "N_KOORD",
                "sep": ",",
            },
        },
    },
    "statent": {
        "latest": "2022",
        "2022": {
            "url": "https://dam-api.bfs.admin.ch/hub/api/dam/assets/32258837/master",
            "known_hash": _statent_known_hash,
            "zip": True,
            "members": "ag-b-00.03-22-STATENT2022/STATENT_2022.csv",
            "which_member": 0,
            "read_csv_kwargs": {
                "x_column": "E_KOORD",
                "y_column": "N_KOORD",
                "sep": ",",
            },
        },
    },
}

## logging
LOG_CONSOLE = False
LOG_FILE = False
LOG_FILENAME = "swisslandstats"
LOG_LEVEL = lg.INFO
LOG_NAME = "swisslandstats"
LOGS_FOLDER = "./logs"
