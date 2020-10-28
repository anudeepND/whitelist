#!/usr/bin/env python3
#
# Project homepage: https://github.com/anudeepND/whitelist
# Licence: https://github.com/anudeepND/whitelist/blob/master/LICENSE
# Created by Anudeep
# ================================================================================
import os
import argparse
import sqlite3
import subprocess
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def fetch_whitelist_url(url):

    if not url:
        return
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}
    try:
        response = urlopen(Request(url, headers=headers))
    except HTTPError as e:
        print('[X] HTTP Error:', e.code, 'whilst fetching', url)
        print('\n')
        print('\n')
        exit(1)
    except URLError as e:
        print('[X] URL Error:', e.reason, 'whilst fetching', url)
        print('\n')
        print('\n')
        exit(1)
    # Read and decode
    response = response.read().decode('UTF-8').replace('\r\n', '\n')
    # If there is data
    if response:
        # Strip leading and trailing whitespace
        response = '\n'.join(x.strip() for x in response.splitlines())
    # Return the hosts
    return response

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def restart_pihole(docker):
    if docker is True:
        subprocess.call("docker exec -it pihole pihole restartdns reload",
                        shell=True, stdout=subprocess.DEVNULL)
    else:
        subprocess.call(['pihole', '-g'], stdout=subprocess.DEVNULL)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", type=dir_path, help="optional: Pi-hole etc directory")
parser.add_argument("-D", "--docker",  action='store_true', help="optional: set if you're using Pi-hole in docker environment")
args = parser.parse_args()

if args.dir:
    pihole_location = args.dir
else:
    pihole_location = r'/etc/pihole'

whitelist_remote_url = 'https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt'
remote_sql_url = 'https://raw.githubusercontent.com/anudeepND/whitelist/master/scripts/domains.sql'
gravity_whitelist_location = os.path.join(pihole_location, 'whitelist.txt')
gravity_db_location = os.path.join(pihole_location, 'gravity.db')
anudeep_whitelist_location = os.path.join(pihole_location, 'anudeep-whitelist.txt')

db_exists = False
db_connect = False

whitelist_remote = set()
whitelist_local = set()
whitelist_anudeep_local = set()
whitelist_old_anudeep = set()

os.system('clear')
print('\n')
print('This script will download and add domains from the repo to whitelist.')
print('All the domains in this list are safe to add and does not contain any tracking or adserving domains.')
print('\n')

# Check for pihole path exsists
if os.path.exists(pihole_location):
    print('[i] Pi-hole path exists')
else:
    # print(f'[X] {pihole_location} was not found')

    print("[X] {} was not found".format(pihole_location))

    print('\n')
    print('\n')
    exit(1)

# Check for write access to /etc/pihole
if os.access(pihole_location, os.X_OK | os.W_OK):
    print("[i] Write access to {} verified" .format(pihole_location))
    whitelist_str = fetch_whitelist_url(whitelist_remote_url)
    remote_whitelist_lines = whitelist_str.count('\n')
    remote_whitelist_lines += 1
else:
    print("[X] Write access is not available for {}. Please run as root or other privileged user" .format(
        pihole_location))
    print('\n')
    print('\n')
    exit(1)

# Determine whether we are using DB or not
if os.path.isfile(gravity_db_location) and os.path.getsize(gravity_db_location) > 0:
    db_exists = True
    print('[i] Pi-Hole Gravity database found')
    remote_sql_str = fetch_whitelist_url(remote_sql_url)
    remote_sql_lines = remote_sql_str.split('\n')
    if len(remote_sql_str) > 0:
        print("[i] {} domains and {} SQL queries discovered" .format(remote_whitelist_lines, len(remote_sql_lines)))
        # make `remote_sql_str` a tuple so we can easily compare
        newWhiteTUP = remote_sql_lines
        # Number of domains that would be added by script
    else:
        print('[X] No remote SQL queries found')
        print('\n')
        print('\n')
        exit(1)
else:
    print('[i] Legacy Pi-hole detected (Version older than 5.0)')

# If domains were fetched, remove any comments and add to set
if whitelist_str:
    whitelist_remote.update(x for x in map(
        str.strip, whitelist_str.splitlines()) if x and x[:1] != '#')
else:
    print('[X] No remote domains were found.')
    print('\n')
    print('\n')
    exit(1)

if db_exists: # IF Pi-hole v5 or newer we have sql database
    print('[i] Connecting to Gravity.')
    try: # Try to create a DB connection
        sqliteConnection = sqlite3.connect(gravity_db_location)
        cursor = sqliteConnection.cursor()
        print('[i] Successfully Connected to Gravity.')
        print ('[i] Checking Gravity for domains added by script.')
        # Check Gravity database for domains added by script
        gravityScript_before = cursor.execute(" SELECT * FROM domainlist WHERE type = 0 AND comment LIKE '%qjz9zk%' ")
        # fetch all matching entries which will create a tuple for us
        gravScriptBeforeTUP = gravityScript_before.fetchall()
        # Number of domains in database from script
        print ('[i] Found {} domains added by script in whitelist already.'.format(len(gravScriptBeforeTUP)))
        db_connect = True
    except sqlite3.Error as error:
        print('[X] Failed to Connect to Gravity.', error)
        print('\n')
        print('\n')
        exit(1)
else: # else Pi-hole version is older than v5 so no sql database
    if os.path.isfile(gravity_whitelist_location) and os.path.getsize(gravity_whitelist_location) > 0:
        print('[i] Collecting existing entries from whitelist.txt')
        with open(gravity_whitelist_location, 'r') as fRead:
            whitelist_local.update(x for x in map(
                str.strip, fRead) if x and x[:1] != '#')

    if whitelist_local:
        print("[i] {} existing whitelists identified".format(len(whitelist_local)))
        if os.path.isfile(anudeep_whitelist_location) and os.path.getsize(anudeep_whitelist_location) > 0:
            print('[i] Existing anudeep-whitelist install identified')
            with open(anudeep_whitelist_location, 'r') as fOpen:
                whitelist_old_anudeep.update(x for x in map(
                    str.strip, fOpen) if x and x[:1] != '#')

                if whitelist_old_anudeep:
                    print('[i] Removing previously installed whitelist')
                    whitelist_local.difference_update(whitelist_old_anudeep)

    print("[i] Syncing with {}" .format(whitelist_remote_url))
    whitelist_local.update(whitelist_remote)

    print("[i] Outputting {} domains to {}" .format(len(whitelist_local), gravity_whitelist_location))
    with open(gravity_whitelist_location, 'w') as fWrite:
        for line in sorted(whitelist_local):
            fWrite.write("{}\n".format(line))

    with open(anudeep_whitelist_location, 'w') as fWrite:
        for line in sorted(whitelist_remote):
            fWrite.write("{}\n".format(line))

    print('[i] Done - Domains are now added to your Pi-Hole whitelist\n')
    print('[i] Restarting Pi-hole. This could take a few seconds')
    restart_pihole(args.docker)
    print('[i] Done. Happy ad-blocking :)')
    print('\n')
    print('Star me on GitHub: https://github.com/anudeepND/whitelist')
    print('Buy me a coffee: https://paypal.me/anudeepND')
    print('\n')
    exit(0)

if db_connect: # If we can successfully access the Gravity database
    #
    # Get domains from newWhiteTUP and make a list
    nW = []
    newWL = [None]
    newWhiteList = []
    for newWhiteDomain in newWhiteTUP:  # for each line found domains.sql
        nW.append(newWhiteDomain)  # Add line to a controlled list
        index = nW.index(newWhiteDomain)
        removeBrace = nW[index].replace('(', '')  # remove (
        removeBraces10 = removeBrace.replace(')', '')  # remove )
        newWL = removeBraces10.split(', ')  # split at commas to create a list
        newWhiteList.append(newWL[1].replace('\'', ''))  # remove ' from domain and add to list
    #
    # check database for user added exact whitelisted domains
    print ('[i] Checking Gravity for domains added by user that are also in script.')
    # Check Gravity database for exact whitelisted domains added by user
    user_add = cursor.execute(" SELECT * FROM domainlist WHERE type = 0 AND comment NOT LIKE '%qjz9zk%' ")
    userAddTUP = user_add.fetchall()
    #
    # check if  whitelisted domains added by user are in script
    userAddList = []
    #
    for userAddINgravity in userAddTUP:  # for every whitelisted domain we found in the database do:
        if userAddINgravity[2] in newWhiteList:  # if the domain we found added by user IS IN our new list count it
            userAddList.append(userAddINgravity[2])  # add the domain we found to the list we created
    #
    # Make us aware of User Added domains that are also in our script
    if userAddList != []:  # if we found user added domains from our list in gravity do:
        print ('[i] {} domain(s) added by the user that would be added by script.\n'.format(len(userAddList)))
        for userADD in userAddList:  # 
            a = userAddList.index(userADD) + 1 # counter for number output to screen
            print ('    {}. {}'.format(a, userADD))  # Show us what we found
        print ('')
    else: # If we don't find any
        print ('[i] Found no domains added by the user that would be added by script.') # notify of negative result
    #
    # Check Gravity database for domains added by script that are not in new script
    INgravityNOTnewList = []
    gravScriptBeforeList = []
    #
    print ('[i] Checking Gravity for domains previously added by script that are NOT in new script.')
    #
    for INgravityNOTnew in gravScriptBeforeTUP:  # for every domain previously added by script
        gravScriptBeforeList.append(INgravityNOTnew[2]) # take domains from gravity and put them in a list for later
        if not INgravityNOTnew[2] in newWhiteList:  # make sure it is not in new script
            INgravityNOTnewList.append(INgravityNOTnew)  # add not found to list for later
    #
    # If In Gravity because of script but NOT in the new list Prompt for removal
    if INgravityNOTnewList != []:
        print ('[i] {} domain(s) added previously by script that are not in new script.\n'.format(len(INgravityNOTnewList)))
        for needTOdelete in INgravityNOTnewList:
            print ('    deleting {}'.format(needTOdelete[2]))
            sql_delete = " DELETE FROM domainlist WHERE type = 0 AND id = '{}' ".format(needTOdelete[0])
            cursor.executescript(sql_delete)
        print ('')
    else:
        # If not keep going
        print ('[i] Found no domain(s) added previously by script that are not in script.')
    #
    # Check Gravity database for new domains to be added by script
    INnewNOTgravityList = []
    #
    print ('[i] Checking script for domains not in Gravity.')
    #
    for INnewNOTgravity in newWhiteList:  # for every domain in the new script
        if not INnewNOTgravity in gravScriptBeforeList and not INnewNOTgravity in userAddList:  # make sure it is not in gravity or added by user
            INnewNOTgravityList.append(INnewNOTgravity) # add domain to list we created
    #
    # If there are domains in new list that are NOT in Gravity
    if INnewNOTgravityList != []:  # Add domains that are missing from new script and not user additions
        print ('[i] {} domain(s) NOT in Gravity that are in new script.\n'.format(len(INnewNOTgravityList)))
        for addNewWhiteDomain in newWhiteList:
            if addNewWhiteDomain in INnewNOTgravityList:
                print ('    - Adding {}'.format(addNewWhiteDomain))
                sql_index = newWhiteList.index(addNewWhiteDomain)
                sql_add = ' INSERT OR IGNORE INTO domainlist (type, domain, enabled, comment) VALUES {} '.format(nW[sql_index])
                cursor.executescript(sql_add)
        #
        # Re-Check Gravity database for domains added by script after we update it
        gravityScript_after = cursor.execute(" SELECT * FROM domainlist WHERE type = 0 AND comment LIKE '%qjz9zk%' ")
        # fetch all matching entries which will create a tuple for us
        gravScriptAfterTUP = gravityScript_after.fetchall()
        # Number of domains in database from script
        #
        gravScriptAfterList = []
        print ('')
        print ('[i] Checking Gravity for newly added domains.')
        print ('')
        for gravScriptAfterDomain in gravScriptAfterTUP:
            gravScriptAfterList.append(gravScriptAfterDomain[2])

        weFOUNDitList = []
        for weFOUNDit in INnewNOTgravityList:
            if weFOUNDit in gravScriptAfterList:
                weFOUNDitList.append(weFOUNDit)
                print ('    - Found  {} '.format(weFOUNDit))

        if len(weFOUNDitList) == len(INnewNOTgravityList):
            # All domains are accounted for.
            print ('\n[i] All {} missing domain(s) to be added by script have been discovered in Gravity.'.format(len(INnewNOTgravityList)))
        else:
            print ('\n[i] All {} new domain(s) have not been added to Gravity.'.format(len(INnewNOTgravityList)))
        #
        print ('[i] All {} domains to be added by script have been discovered in Gravity'.format(len(newWhiteTUP)))
    else:
        # We should be done now
        # Do Nothing and exit. All domains are accounted for.
        print ('[i] All {} domains to be added by script have been discovered in Gravity'.format(len(newWhiteTUP)))
    #
    # Find total whitelisted domains (regex)
    total_domains_R = cursor.execute(' SELECT * FROM domainlist WHERE type = 2 ')
    tdr = len(total_domains_R.fetchall())
    # Find total whitelisted domains (exact)
    total_domains_E = cursor.execute(' SELECT * FROM domainlist WHERE type = 0 ')
    tde = len(total_domains_E.fetchall())
    total_domains = tdr + tde
    print ('[i] There are a total of {} domains in your whitelist (regex({}) & exact({}))'.format(total_domains, tdr, tde))
    sqliteConnection.close()
    print ('[i] The database connection is closed')
    if INnewNOTgravityList != []:
        print ('[i] Restarting Pi-hole. This could take a few seconds')
        restart_pihole(args.docker)

    print ('\n')
    print ('Done. Happy ad-blocking :)')
    print ('\n')
    print ('Star me on GitHub: https://github.com/anudeepND/whitelist')
    print ('Buy me a coffee: https://paypal.me/anudeepND')
    print ('\n')
    exit(0)
