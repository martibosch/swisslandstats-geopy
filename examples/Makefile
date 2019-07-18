SLS_URI = https://www.bfs.admin.ch/bfsstatic/dam/assets/6646411/master

DATA_DIR = data
SLS_CSV_FILEPATH := $(DATA_DIR)/AREA_NOAS04_17_181029.csv

# rules
$(DATA_DIR):
	mkdir $(DATA_DIR)
$(DATA_DIR)/%.zip: $(DATA_DIR)
	curl $(SLS_URI) -o $@
$(DATA_DIR)/%.csv: $(DATA_DIR)/%.zip
	unzip -j $< '*.csv' -d $(DATA_DIR)
	touch $(SLS_CSV_FILEPATH)

download_data: $(SLS_CSV_FILEPATH)
