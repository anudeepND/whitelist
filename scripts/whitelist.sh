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


if [ $(dpkg-query -W -f='${Status}' gawk 2>/dev/null |  grep -c "ok installed") -eq 0 ];
then
  echo -e " [...] \e[32m Installing gawk... \e[0m"
  sudo apt-get install gawk -qq > /dev/null
  wait
  echo -e " ${TICK} \e[32m Finished \e[0m"
fi


sudo curl -sS https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt >> /etc/pihole/whitelist.txt
echo -e " ${TICK} \e[32m Adding to whitelist... \e[0m"
sleep 0.5
echo -e " ${TICK} \e[32m Removing duplicates... \e[0m"
sudo gawk -i inplace '!a[$0]++' /etc/pihole/whitelist.txt
wait
echo -e " ${TICK} \e[32m Restarting DNS service \e[0m"
pihole restartdns > /dev/null
wait
echo -e " ${TICK} \e[32m Done! \e[0m"


echo -e " \e[1m  Star me on GitHub, https://github.com/anudeepND/whitelist \e[0m"
echo -e " \e[1m  Happy AdBlocking :)\e[0m"
echo -e "\n\n"
