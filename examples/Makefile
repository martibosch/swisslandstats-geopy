.PHONY: download_land download_statpop

# global variables/rules
DATA_DIR = data
$(DATA_DIR):
	mkdir $@


# land (land use/land cover data)
LAND_URI = https://dam-api.bfs.admin.ch/hub/api/dam/assets/25885691/master
LAND_DATA_DIR := $(DATA_DIR)/land
LAND_CSV_FILEPATH := $(LAND_DATA_DIR)/land.csv

$(LAND_DATA_DIR): | $(DATA_DIR)
	mkdir $@
$(LAND_CSV_FILEPATH): | $(LAND_DATA_DIR)
	curl $(STATPOP_URI) -o $@
download_land: $(LAND_CSV_FILEPATH)

# STATPOP (population)
STATPOP_URI = https://dam-api.bfs.admin.ch/hub/api/dam/assets/27965868/master
STATPOP_DATA_DIR := $(DATA_DIR)/statpop
STATPOP_CSV_FILEPATH := $(STATPOP_DATA_DIR)/STATPOP2022.csv

$(STATPOP_DATA_DIR): | $(DATA_DIR)
	mkdir $@
$(STATPOP_DATA_DIR)/%.zip: $(STATPOP_DATA_DIR)
	curl $(STATPOP_URI) -o $@
$(STATPOP_DATA_DIR)/%.csv: $(STATPOP_DATA_DIR)/%.zip
	unzip -j $< 'ag-b-00.03-vz2022statpop/STATPOP2022.csv' -d $(STATPOP_DATA_DIR)
	touch $(STATPOP_CSV_FILEPATH)
download_statpop: $(STATPOP_CSV_FILEPATH)
