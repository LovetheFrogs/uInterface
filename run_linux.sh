#!/bin/bash

# If config.conf file has not yet been created then the program has not been executed yet  
# Once the file exists, that means the dependencies are dowloaded because the program was used before
CONF_FILE=gui/resources/config.conf

# Colors for echo printing
BPurple='\033[1;35m'
BGreen='\033[1;32m'
LGray='\e[0;37m'

if [[ ! -f "$CONF_FILE" ]]
then
	echo -e "${BPurple}Installing dependencies"
	echo -e "${LGray} "
	sudo apt-get install python3-tk
	sudo apt-get python3-pil python3-pil.imagetk
	sudo python3 setup.py install
fi

echo -e "${BGreen}Launching uInterface"
echo -e "${LGray} "
cd gui
python3 main.py

echo -e "${BGreen}Closing uInterface"
