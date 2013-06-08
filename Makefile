
CONFIG_DIR=/etc/home/
BIN_DIR=/usr/local/bin/
SYSTEMD_DIR=/etc/systemd/system/

install:
	#mkdir -p $(CONFIG_DIR)
	cp cfg/app.cfg $(CONFIG_DIR)
	cp restServer.py $(BIN_DIR)/home-restServer.py
	cp home-rest.service $(SYSTEMD_DIR)

config-bed:
	cp json/bed_sensors.json $(CONFIG_DIR)/sensors.json
	cp json/bed_switches.json $(CONFIG_DIR)/switches.json

install-bed: install config-bed

config-desk:
	cp json/desk_sensors.json $(CONFIG_DIR)/sensors.json
	cp json/desk_switches.json $(CONFIG_DIR)/switches.json

install-desk: install config-desk
