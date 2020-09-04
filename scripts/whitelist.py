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
import time

today = int(time.time())

def fetch_whitelist_url(url):

    if not url:
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}

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
parser.add_argument("-d", "--dir", type=dir_path,
                    help="optional: Pi-hole etc directory")
parser.add_argument(
    "-D", "--docker",  action='store_true', help="optional: set if you're using Pi-hole in docker environment")
args = parser.parse_args()

if args.dir:
    pihole_location = args.dir
else:
    pihole_location = r'/etc/pihole'

whitelist_remote_url = 'https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt'
remote_sql_url = 'https://raw.githubusercontent.com/anudeepND/whitelist/master/scripts/domains.sql'
gravity_whitelist_location = os.path.join(pihole_location, 'whitelist.txt')
gravity_db_location = os.path.join(pihole_location, 'gravity.db')
anudeep_whitelist_location = os.path.join(
    pihole_location, 'anudeep-whitelist.txt')

db_exists = False
sqliteConnection = None
cursor = None

whitelist_remote = set()
whitelist_local = set()
whitelist_anudeep_local = set()
whitelist_old_anudeep = set()

os.system('clear')
print('\n')
print('''
This script will download and add domains from the repo to whitelist.
All the domains in this list are safe to add and does not contain any tracking or adserving domains.
''')
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
    remote_sql_lines = remote_sql_str.count('\n')
    remote_sql_lines += 1

    if len(remote_sql_str) > 0:
        print("[i] {} domains and {} SQL queries discovered" .format(
            remote_whitelist_lines, remote_sql_lines))
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

if db_exists:
    print('[i] Connecting to Gravity database')
    try: # Try to create a DB connection
        sqliteConnection = sqlite3.connect(gravity_db_location)
        cursor = sqliteConnection.cursor()
        print('[i] Successfully Connected to Gravity database')

        # Check Gravity database for domains added by script
        number_d = cursor.execute(" SELECT * FROM domainlist WHERE type = 0 AND comment LIKE '%qjz9zk%' ")

        numberD = number_d.fetchall()

        # Number of domains in database from script
        numberD_ = len(numberD)
        print('[i] Checking Gravity database for domains added by script')
        print ("[i] {} Domains from script in whitelist already" .format(numberD_))

        # make `whitelist_str` a tuple so we can easily compare
        whitelist_tup = tuple(whitelist_str.split("\n"))
        # Number of domains that would be added by script
        whiteTUPlen = len(whitelist_tup)

        # Check Gravity database for domains added by script that are not in new script
        INgravityNOTnewList = [None] * numberD_
        z = 0
        print('[i] Checking Gravity database for domains added previously by script that are not in new script')
        for INgravityNOTnew in numberD:
           if not INgravityNOTnew[2] in whitelist_tup:
               INgravityNOTnewList[z] = INgravityNOTnew
               # uncomment the next 2 line to delete domains not in script anymore
               # sql_delete = " DELETE FROM domainlist WHERE type = 0 AND id = '{}' "  .format(INgravityNOTnewList[z][0])
               # cursor.executescript(sql_delete)
               z = z + 1

        z = z - 1
        a = 0
        INgravityNOTnewListCount = z
        ignl = False
        if z >= 0:
           ignl = True
           while z >= 0:
                a = a + 1
                print ('   {}. {}' .format(a, INgravityNOTnewList[z][2]))
                # ignl = True
                z = z - 1
        # I will figure out how to remove them soon

        # some logic to check if there are any domain(s) added previous by script that are not in new script.
        if ignl == False:
          numberDlen = numberD_
        else:
            print ('[i] There are {} domain(s) added previously by script that are not in new script.' .format(INgravityNOTnewListCount+1))
            numberDlen = numberD_ - (INgravityNOTnewListCount+1)

        # Check Gravity database for exact whitelisted domains added by user
        number_d_n = cursor.execute(" SELECT * FROM domainlist WHERE type = 0 AND comment NOT LIKE '%qjz9zk%' ")
        numberDN = number_d_n.fetchall()

        userADD = 0
        # check if  whitelisted domains added by user are in script
        print('[i] Checking Gravity database for domains added by user that are also in script')
        for domain in numberDN:
           if domain[2] in whitelist_tup:
             print('   {}. {}' .format(userADD+1, domain[2]))
             userADD = userADD + 1

        # Number of domains in database from user that would also be added by script
        print ("[i] {} user added domain(s) are also in script and they will NOT be changed." .format(userADD))

        # Add [Number of domains in database from script] + [Number of domains in database from user that would also be added by script] = inDatabase
        inDatabase = userADD + numberDlen

        # compare total in database [inDatabase] = total to be added [whiteTUPlen]
        if inDatabase == whiteTUPlen:
            # Do Nothing and exit. All domains are accounted for.
            print ("[i] No Domains Need to be Added!!!")
            print("[i] All {} domains to be added by script have been discovered in database" .format(remote_whitelist_lines))
            
            # Find total whitelisted domains (regex)
            total_domains_R = cursor.execute(" SELECT * FROM domainlist WHERE type = 2 ")
            tdr = len(total_domains_R.fetchall())

            # Find total whitelisted domains (exact)
            total_domains_E = cursor.execute(" SELECT * FROM domainlist WHERE type = 0 ")
            tde = len(total_domains_E.fetchall())
            total_domains = tdr + tde
            print("[i] There are a total of {} domains in your whitelist (regex({}) & exact({}))" .format(total_domains, tdr, tde))
            cursor.close()
            sqliteConnection.close()
            print('[i] The database connection is closed!!')

        else:
            # Add our domains to Gravity database (unless they are already present)
            print('[i] Adding / updating domains in the Gravity database')
            cursor.executescript(remote_sql_str)
            print('[i] Commiting changes to Gravity database')
            # Commit changes to Gravity Database
            sqliteConnection.commit()
            time.sleep(1)

            # Check for domains added by script
            number_domains = cursor.execute(" SELECT * FROM domainlist WHERE type = 0 AND comment LIKE '%qjz9zk%' ")

            x = 0
            print ("[i] The following domains were added ")
            # Check for recently added (since script started)
            for tm in number_domains:
               if tm[4] >= today:
                 print ("   {}. {}" .format(x + 1, tm[2]))
                 x = x + 1

            numberDomains = x
            print ("\n")
            print ("[i] If no domains are listed make sure they have comments.")
            # I can not figure out how to find info for domains w/o comments in the Web GUI...

            # Find total whitelisted domains (regex)
            total_domains_R = cursor.execute(" SELECT * FROM domainlist WHERE type = 2 ")
            tdr = len(total_domains_R.fetchall())

            # Find total whitelisted domains (exact)
            total_domains_E = cursor.execute(" SELECT * FROM domainlist WHERE type = 0 ")
            tde = len(total_domains_E.fetchall())
            total_domains = tdr + tde
            print("[i] There are a total of {} domains in your whitelist (regex({}) & exact({}))" .format(total_domains, tdr, tde))
            cursor.close()

            sqliteConnection.close()
            print('[i] The database connection is closed')
            print('[i] Restarting Pi-hole. This could take a few seconds')
            restart_pihole(args.docker)

    except sqlite3.Error as error:
        print('[X] Failed to insert domains into Gravity database', error)
        print('\n')
        print('\n')
        exit(1)

    finally:
        print('\n')
        print('Done. Happy ad-blocking :)')
        print('\n')
        print('Star me on GitHub: https://github.com/anudeepND/whitelist')
        print('Buy me a coffee: https://paypal.me/anudeepND')
        print('\n')

else:

    if os.path.isfile(gravity_whitelist_location) and os.path.getsize(gravity_whitelist_location) > 0:
        print('[i] Collecting existing entries from whitelist.txt')
        with open(gravity_whitelist_location, 'r') as fRead:
            whitelist_local.update(x for x in map(
                str.strip, fRead) if x and x[:1] != '#')

    if whitelist_local:
        print("[i] {} existing whitelists identified".format(
            len(whitelist_local)))
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

    print("[i] Outputting {} domains to {}" .format(
        len(whitelist_local), gravity_whitelist_location))
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
