#!/bin/bash
# This script will download and add domains from the rep to whitelist.txt file.
# Project homepage: https://github.com/anudeepND/whitelist
# Licence: https://github.com/anudeepND/whitelist/blob/master/LICENSE
# Created by Anudeep
#================================================================================
TICK="[\e[32m ✔ \e[0m]"


echo -e " \e[1m This script will download and add domains from the repo to whitelist.txt \e[0m"
sleep 1
echo -e "\n"

if [ "$(id -u)" != "0" ] ; then
	echo "This script requires root permissions. Please run this as root!"
	exit 2
fi

if [ "$(dpkg-query -W -f='${Status}' gawk 2>/dev/null |  grep -c "ok installed")" -eq 0 ];
then
  echo -e " [...] \e[32m Installing gawk... \e[0m"
  apt-get install gawk -qq > /dev/null
  wait
  echo -e " ${TICK} \e[32m Finished \e[0m"
fi


curl -sS https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/optional-list.txt | sudo tee -a /etc/pihole/whitelist.txt >/dev/null
echo -e " ${TICK} \e[32m Adding to whitelist... \e[0m"
sleep 0.5
echo -e " ${TICK} \e[32m Removing duplicates... \e[0m"
gawk -i inplace '!a[$0]++' /etc/pihole/whitelist.txt
wait
echo -e " [...] \e[32m Pi-hole gravity rebuilding lists. This may take a while... \e[0m"
pihole -g > /dev/null
wait
echo -e " ${TICK} \e[32m Pi-hole's gravity updated \e[0m"
echo -e " ${TICK} \e[32m Done! \e[0m"


echo -e " \e[1m  Star me on GitHub, https://github.com/anudeepND/whitelist \e[0m"
echo -e " \e[1m  Happy AdBlocking :)\e[0m"
echo -e "\n\n"
