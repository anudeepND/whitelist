#!/usr/bin/env python3
#
# Project homepage: https://github.com/anudeepND/whitelist
# Licence: https://github.com/anudeepND/whitelist/blob/master/LICENSE
# Created by Anudeep
# ================================================================================
import os
import argparse
from sqlite3 import connect
from sqlite3 import Error as sqlError
import subprocess
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import re

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
        print ('')
        subprocess.call("docker exec -it pihole pihole restartdns reload", shell=True)
    else:
        print ('')
        subprocess.call(['pihole', 'restartdns', 'reload'])

def getPiholeVersion():
    pihole_version = subprocess.Popen(['pihole', 'version', '-p', '-c'], stdout=subprocess.PIPE)
    phVersion = pihole_version.stdout.read().decode().split('\n')
    p_h_Version = []
    for phv in phVersion:
        if phv != '':
            p_h_Version.append(re.sub("[^0-9]", "", phv.lstrip()))
    PHV = int(p_h_Version[0][:2])
    return (PHV)

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

# use the RGBA code for white (255, 255, 255, 1) as our Group ID we just take out the commas
# hopefully this number is big enough that no User added groups will overlap 
# please see ---> https://docs.pi-hole.net/database/gravity/groups/#group-management
anudeep_group_id = 2552552551 # Group ID used in gravity.db
anudeep_group = (anudeep_group_id, 1, "anudeepND/whitelist", "https://github.com/anudeepND/whitelist") # Group Information used in gravity.db

db_exists = False
db_connect = False

whitelist_remote = set()
whitelist_local = set()
whitelist_anudeep_local = set()
whitelist_old_anudeep = set()

os.system('clear')
print('')
print('This script will download and add domains from the repo to whitelist.')
print('All the domains in this list are safe to add and does not contain any tracking or adserving domains.')
print('')

# Check for pihole path exsists
if os.path.exists(pihole_location):
    print('[i] Pi-hole path exists')
else:
    # print(f'[X] {pihole_location} was not found')

    print("[X] {} was not found".format(pihole_location))

    print('')
    print('')
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
    print('')
    print('')
    exit(1)

# Determine whether we are using DB or not
if os.path.isfile(gravity_db_location) and os.path.getsize(gravity_db_location) > 0 and getPiholeVersion() >= 51:
    print('[i] Pi-Hole Gravity database found')
    remote_sql_str = fetch_whitelist_url(remote_sql_url)
    remote_sql_lines = remote_sql_str.split('\n')
    if len(remote_sql_lines) > 0:
        print("[i] {} domains and {} SQL queries discovered" .format(remote_whitelist_lines, len(remote_sql_lines)))
        db_exists = True
    else:
        print('[X] No remote SQL queries found')
        print('')
        print('')
        exit(1)
else:
    print('[i] Legacy Pi-hole detected (Version older than 5.0)')

# If domains were fetched, remove any comments and add to set
if whitelist_str:
    whitelist_remote.update(x for x in map(
        str.strip, whitelist_str.splitlines()) if x and x[:1] != '#')
else:
    print('[X] No remote domains were found.')
    print('')
    print('')
    exit(1)

# If Pi-hole v5 or newer we have sql database
if db_exists:
    print('[i] Connecting to Gravity.')
    # Try to connect to gravity DB
    try:
        gravityConnection = connect(gravity_db_location)
        gravity = gravityConnection.cursor()

        print('[i] Successfully Connected to Gravity.')
        print ('[i] Checking Gravity for domains added by script.')

        # Get domains in gravity database added by script
        gravityScript_before = gravity.execute(" SELECT * FROM domainlist WHERE type = 0 AND comment LIKE '%qjz9zk%' ")

        # fetch all matching entries which will create a tuple for us
        gravScriptBeforeTUP = gravityScript_before.fetchall()

        # Number of domains in database from script
        print ('[i] Found {} domains added by script in whitelist already.'.format(len(gravScriptBeforeTUP)))

        # check database for user added exact whitelisted domains
        print ('[i] Checking Gravity for domains added by user that are also in script.')

        # Check Gravity database for exact whitelisted domains added by user
        user_add = gravity.execute(" SELECT * FROM domainlist WHERE type = 0 AND comment NOT LIKE '%qjz9zk%' OR comment isnull ")
        userAddTUP = user_add.fetchall()

        # Check Gravity database for anudeepND/whitelist group
        print ('[i] Checking Gravity for anudeepND/whitelist group.')
        get_groups_table = gravity.execute("SELECT id FROM 'group'")
        fetch_groups = get_groups_table.fetchall()
        
        # create a list for all the group ID's in gravity
        groupList = []
        for group in fetch_groups:
            groupList.append(group[0])
        
        # Check for the one we need before we add it
        if anudeep_group_id not in groupList:
            print ('    - adding group for anudeepND/whitelist.')
            set_group_in_table = gravity.execute("INSERT OR IGNORE INTO 'group' (id, enabled, name, description) VALUES {} ".format(anudeep_group))
        else:
            print ('[i] Found anudeepND/whitelist group in Gravity.')
        
        db_connect = True
    except sqlError as error:
        print('[X] Failed to Connect to Gravity.', error)
        print('')
        print('')
        exit(1)
# else Pi-hole version is older than v5 so no sql database
else:
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
    print('[i] Reloading Pi-hole lists. This could take a few seconds')
    restart_pihole(args.docker)
    print('[i] Done. Happy ad-blocking :)')
    print('')
    print('Star me on GitHub: https://github.com/anudeepND/whitelist')
    print('Buy me a coffee: https://paypal.me/anudeepND')
    print('')
    exit(0)

# If we can successfully access the Gravity database
if db_connect:

    # Get domains from remote_sql_lines and make a list
    newWhiteList = [] # Make a list of domains
    for newWhiteDomain in remote_sql_lines:  # for each line found domains.sql
        #print (newWhiteDomain)
        removeBrace = newWhiteDomain.replace('(', '')  # remove (
        removeBraces10 = removeBrace.replace(')', '')  # remove )
        newWL = removeBraces10.split(', ')  # split at commas to create a list
        newWhiteList.append(newWL[1].replace('\'', ''))  # remove ' from domain and add to list

    # check if  whitelisted domains added by user are in script
    userAddList = [] # Make a list of domains whitelisted by user

    for userAddINgravity in userAddTUP:  # for every domain whitelisted by user we found in the database do:
        if userAddINgravity[2] in newWhiteList:  # if the domain we found added by user IS IN our new list count it
            userAddList.append(userAddINgravity[2])  # add the domain we found to the list we created

    # Make user aware of User Added domains that are also in our script
    if userAddList != []:  # If list not empty
        print ('[i] {} domain(s) added by the user that would be added by script.\n'.format(len(userAddList)))
        for userADD in userAddList:  # 
            print ('    {}. {}'.format(userAddList.index(userADD) + 1, userADD))  # Show us what we found
        print ('')
    else: # If we don't find any
        print ('[i] Found no domains added by the user that would be added by script.') # notify of negative result

    # Check Gravity database for domains added by script that are not in new script
    INgravityNOTnewList = [] # Make a list of domains that are no longer in this script
    gravScriptBeforeList = [] # Make a list of domains in gravity that were added by this script

    print ('[i] Checking Gravity for domains previously added by script that are NOT in new script.')

    for INgravityNOTnew in gravScriptBeforeTUP: # for every domain previously added by script
        gravScriptBeforeList.append(INgravityNOTnew[2]) # take domains from gravity and put them in a list for later
        if not INgravityNOTnew[2] in newWhiteList: # make sure it is not in new script
            INgravityNOTnewList.append(INgravityNOTnew)  # add not found to list for later

    # If In Gravity because of script but NOT in the new list remove it
    if INgravityNOTnewList != []: # If list not empty
        print ('[i] {} domain(s) added previously by script that are not in new script.\n'.format(len(INgravityNOTnewList)))
        for needTOdelete in INgravityNOTnewList: # For every domain in gravity we need to delete
            print ('    - deleting {}. {}'.format(INgravityNOTnewList.index(needTOdelete) + 1, needTOdelete[2])) # show us what needs to be deleted
            sql_delete_domain = " DELETE FROM domainlist WHERE type = 0 AND id = '{}' ".format(needTOdelete[0]) # Make our sql statement
            try: 
                gravity.executescript(sql_delete_domain) # Delete domain from gravity
            except sqlError as error:
                print ('Failed to delete {}'.format(needTOdelete[2]))
        print ('')
    else:
        # If not keep going
        print ('[i] Found no domain(s) added previously by script that are not in script.')

    # Check Gravity database for new domains to be added by script
    INnewNOTgravityList = [] # Make a list of domains we need to add

    print ('[i] Checking script for domains not in Gravity.')

    for INnewNOTgravity in newWhiteList:  # for every domain in the new script not in gravity
        if not INnewNOTgravity in gravScriptBeforeList and not INnewNOTgravity in userAddList:  # make sure it is not in gravity or added by user
            INnewNOTgravityList.append(INnewNOTgravity) # add domain to list we need to add

    # If there are domains in new list that are NOT in Gravity
    if INnewNOTgravityList != []: # If list not empty
        print ('[i] {} domain(s) NOT in Gravity that are in new script.\n'.format(len(INnewNOTgravityList)))
        for addNewWhiteDomain in newWhiteList: # For every domain in list
            if addNewWhiteDomain in INnewNOTgravityList: # If it's a domain we need to add
                print ('    - Adding {}. {}'.format(INnewNOTgravityList.index(addNewWhiteDomain) + 1, addNewWhiteDomain)) # show it to us
                sql_index = newWhiteList.index(addNewWhiteDomain) # Find it in our list
                sql_add_domain_to_whitelist = ' INSERT OR IGNORE INTO domainlist (type, domain, enabled, comment) VALUES {} '.format(remote_sql_lines[sql_index]) # make our sql statement
                try:
                    gravity.executescript(sql_add_domain_to_whitelist)
                except sqlError as error:
                    print ('Failed to add {}'.format(addNewWhiteDomain))
                    print (error)

        # Re-Check Gravity database for domains added by script after we update it
        gravityScript_after = gravity.execute(" SELECT * FROM domainlist WHERE type = 0 AND comment LIKE '%qjz9zk%' ")
        # fetch all matching entries which will create a tuple for us
        gravScriptAfterTUP = gravityScript_after.fetchall()

        gravScriptAfterList = [] # Make a list of domains so we can make sure all missing domains are in gravity
        gravScriptAfterListDI = []
        print ('')
        print ('[i] Checking Gravity for newly added domains.')
        print ('')
        for gravScriptAfterDomain in gravScriptAfterTUP:
            gravScriptAfterList.append(gravScriptAfterDomain[2]) # only get the domain
            gravScriptAfterListDI.append(gravScriptAfterDomain[0]) # get unique domainlist_id

        # check every domain the script has added 
        for domain_ID in gravScriptAfterListDI:
            get_domain_ID = gravity.execute(" SELECT * FROM domainlist_by_group WHERE domainlist_id = {} ".format(domain_ID))
            fetch_domainID = get_domain_ID.fetchall()
            only_domainlist_id = fetch_domainID[0][0]
            domain_group_id = fetch_domainID[0][1]
            if domain_group_id != anudeep_group_id: # and make sure it's in the correct group
                try:
                    gravity.execute("UPDATE domainlist_by_group SET group_id={} WHERE domainlist_id = {} ".format(anudeep_group_id, only_domainlist_id))
                except sqlError as error:
                    print ('Could not add domain to group')
                    print (error)

        weFOUNDitList = [] # Make list of missing domains we found
        for weFOUNDit in INnewNOTgravityList:
            if weFOUNDit in gravScriptAfterList:
                weFOUNDitList.append(weFOUNDit)
                print ('    - Found  {}. {} '.format(INnewNOTgravityList.index(weFOUNDit) + 1, weFOUNDit))
        # Assuming all domains are the same the number will be equal
        if len(weFOUNDitList) == len(INnewNOTgravityList):
            # All domains are accounted for.
            print ('\n[i] All {} missing domain(s) to be added by script have been discovered in Gravity.'.format(len(INnewNOTgravityList)))
        else:
            print ('\n[i] All {} new domain(s) have not been added to Gravity.'.format(len(INnewNOTgravityList)))
        
        print ('[i] All {} domains to be added by script have been discovered in Gravity'.format(len(remote_sql_lines)))
    else:
        # We should be done now
        # Do Nothing and exit. All domains are accounted for.
        print ('[i] All {} domains to be added by script have been discovered in Gravity'.format(len(remote_sql_lines)))
    
    # Find total whitelisted domains (regex)
    total_domains_R = gravity.execute(' SELECT * FROM domainlist WHERE type = 2 ')
    tdr = len(total_domains_R.fetchall())
    # Find total whitelisted domains (exact)
    total_domains_E = gravity.execute(' SELECT * FROM domainlist WHERE type = 0 ')
    tde = len(total_domains_E.fetchall())
    total_domains = tdr + tde
    print ('[i] There are a total of {} domains in your whitelist (regex({}) & exact({}))'.format(total_domains, tdr, tde))
    gravityConnection.commit()
    gravityConnection.close()
    print ('[i] The database connection is closed')
    if INnewNOTgravityList != [] or INgravityNOTnewList != []:
        print ('[i] Reloading Pi-hole lists. This could take a few seconds')
        restart_pihole(args.docker)

    print ('')
    print ('Done. Happy ad-blocking :)')
    print ('')
    print ('Star me on GitHub: https://github.com/anudeepND/whitelist')
    print ('Buy me a coffee: https://paypal.me/anudeepND')
    print ('')
    exit(0)
