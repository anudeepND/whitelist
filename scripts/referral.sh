#!/bin/bash
# This script will download and add domains from the rep to whitelist.txt file.
# Project homepage: https://github.com/anudeepND/whitelist
# Licence: https://github.com/anudeepND/whitelist/blob/master/LICENSE
# Created by Anudeep
#================================================================================
TICK="[ \e[1m\e[32m ✔ \e[0m]"
echo -e " \e[1m This script will download and add domains from the repo to whitelist.txt \e[0m"
sleep 1
if [ $(dpkg-query -W -f='${Status}' gawk 2>/dev/null |  grep -c "ok installed") -eq 0 ];
then
  apt-get -y install gawk;
fi
sleep 1
sudo curl -sS https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/referral-sites.txt >> /etc/pihole/whitelist.txt
sleep 0.5
echo -e " ${TICK} \e[32m Added to whitelist! \e[0m"
sleep 0.5
echo -e " ${TICK} \e[32m Removing duplicates... \e[0m"
sudo gawk -i inplace '!a[$0]++' /etc/pihole/whitelist.txt
echo -e " ${TICK} \e[32m Done! \e[0m"
