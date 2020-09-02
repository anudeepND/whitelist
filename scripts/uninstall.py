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
        subprocess.call(['pihole', 'restartdns', 'reload'],
                        stdout=subprocess.DEVNULL)


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", type=dir_path,
                    help="optional: Pi-hole etc directory")
parser.add_argument(
    "-D", "--docker",  action='store_true', help="optional: set if you're using Pi-hole in Docker environment")
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
If you are using Pi-hole 5.0 or later, then this script will remove the domains which are only added by my script. 
Any other domains added by you will stay as it is. 
''')
print('\n')

# Check for pihole path exsists
if os.path.exists(pihole_location):
    print('[i] Pi-hole path exists')
else:
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
        print("[i] {} domains discovered" .format(remote_whitelist_lines))
    else:
        print('[X] No remote SQL queries found')
        print('\n')
        print('\n')
        exit(1)
else:
    print('[i] Legacy Pi-hole detected (Version older than 5.0)')

if whitelist_str:
    whitelist_remote.update(x for x in map(
        str.strip, whitelist_str.splitlines()) if x and x[:1] != '#')
else:
    print('[X] No remote domains were found.')
    print('\n')
    print('\n')
    exit(1)

if db_exists:
    # Create a DB connection
    print('[i] Connecting to Gravity database')

    try:
        sqliteConnection = sqlite3.connect(gravity_db_location)
        cursor = sqliteConnection.cursor()
        print('[i] Successfully Connected to Gravity database')
        total_domains = cursor.execute(" SELECT * FROM domainlist WHERE type = 0 AND comment LIKE '%qjz9zk%' ")
        
        totalDomains = len(total_domains.fetchall())
        print("[i] There are a total of {} domains in your whitelist which are added by my script" .format(totalDomains))
        print('[i] Removing domains in the Gravity database')
        cursor.execute (" DELETE FROM domainlist WHERE type = 0 AND comment LIKE '%qjz9zk%' ")

        sqliteConnection.commit()

        # we only removed domains we added so use total_domains
        print("[i] {} domains are removed" .format(totalDomains))
        remaining_domains = cursor.execute(" SELECT * FROM domainlist WHERE type = 0 OR type = 2 ")
        print("[i] There are a total of {} domains remaining in your whitelist" .format(len(remaining_domains.fetchall())))

        cursor.close()

    except sqlite3.Error as error:
        print('[X] Failed to remove domains from Gravity database', error)
        print('\n')
        print('\n')
        exit(1)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()

            print('[i] The database connection is closed')

            print('[i] Restarting Pi-hole. This could take a few seconds')
            restart_pihole(args.docker)
            print('\n')
            print('Done. Happy ad-blocking :)')
            print('\n')
            print('Star me on GitHub: https://github.com/anudeepND/whitelist')
            print('Buy me a coffee: https://paypal.me/anudeepND')
            print('\n')

else:
    if os.path.isfile(gravity_whitelist_location) and os.path.getsize(gravity_whitelist_location) > 0:
        with open(gravity_whitelist_location, 'r') as fRead:
            whitelist_local.update(x for x in map(
                str.strip, fRead) if x and x[:1] != '#')

    if whitelist_local:
        print("[i] {} existing whitelisted domains identified" .format(
            len(whitelist_local)))

        if os.path.isfile(anudeep_whitelist_location) and os.path.getsize(anudeep_whitelist_location) > 0:
            print('[i] Existing anudeep-whitelist install identified')
            with open(anudeep_whitelist_location, 'r') as fOpen:
                whitelist_old_anudeep.update(x for x in map(
                    str.strip, fOpen) if x and x[:1] != '#')

                if whitelist_old_anudeep:
                    whitelist_local.difference_update(whitelist_old_anudeep)

            os.remove(anudeep_whitelist_location)

        else:
            print('[i] Removing domains that match the remote repo')
            whitelist_local.difference_update(whitelist_remote)

    print("[i] Adding exsisting {} domains to {}" .format(
        len(whitelist_local), gravity_whitelist_location))
    with open(gravity_whitelist_location, 'w') as fWrite:
        for line in sorted(whitelist_local):
            fWrite.write("{}\n".format(line))

    print('[i] Restarting Pi-hole. This could take a few seconds')
    restart_pihole(args.docker)
    print('[i] Done - Domains are now removed your Pi-Hole whitelist')
    print('\n')
    print('Happy ad-blocking :)')
    print('\n')
    print('Star me on GitHub: https://github.com/anudeepND/whitelist')
    print('Buy me a coffee: https://paypal.me/anudeepND')
    print('\n')
