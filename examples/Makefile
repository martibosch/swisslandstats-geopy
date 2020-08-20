.PHONY: download_land download_statpop

# global variables/rules
DATA_DIR = data
$(DATA_DIR):
	mkdir $@


# land (land use/land cover data)
LAND_URI = https://www.bfs.admin.ch/bfsstatic/dam/assets/6646411/master
LAND_DATA_DIR := $(DATA_DIR)/land
LAND_CSV_FILEPATH := $(LAND_DATA_DIR)/AREA_NOAS04_17_181029.csv

$(LAND_DATA_DIR): | $(DATA_DIR)
	mkdir $@
$(LAND_DATA_DIR)/%.zip: $(LAND_DATA_DIR)
	curl $(LAND_URI) -o $@
$(LAND_DATA_DIR)/%.csv: $(LAND_DATA_DIR)/%.zip
	unzip -j $< '*.csv' -d $(LAND_DATA_DIR)
	touch $(LAND_CSV_FILEPATH)
download_land: $(LAND_CSV_FILEPATH)

# STATPOP (population)
STATPOP_URI = https://www.bfs.admin.ch/bfsstatic/dam/assets/9947069/master
STATPOP_DATA_DIR := $(DATA_DIR)/statpop
STATPOP_CSV_FILEPATH := $(STATPOP_DATA_DIR)/STATPOP2018.csv

$(STATPOP_DATA_DIR): | $(DATA_DIR)
	mkdir $@
$(STATPOP_DATA_DIR)/%.zip: $(STATPOP_DATA_DIR)
	curl $(STATPOP_URI) -o $@
$(STATPOP_DATA_DIR)/%.csv: $(STATPOP_DATA_DIR)/%.zip
	unzip -j $< 'STATPOP2018.csv' -d $(STATPOP_DATA_DIR)
	touch $(STATPOP_CSV_FILEPATH)
download_statpop: $(STATPOP_CSV_FILEPATH)
