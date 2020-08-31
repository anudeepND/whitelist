# Project homepage: https://github.com/anudeepND/whitelist
# Licence: https://github.com/anudeepND/whitelist/blob/master/LICENSE
# Created by Anudeep
# ================================================================================
import os
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


whitelist_remote_url = 'https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt'
remote_sql_url = 'https://raw.githubusercontent.com/anudeepND/whitelist/master/scripts/domains.sql'
pihole_location = r'/etc/pihole'
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
    # Create a DB connection
    print('[i] Connecting to Gravity database')

    try:
        sqliteConnection = sqlite3.connect(gravity_db_location)
        cursor = sqliteConnection.cursor()
        print('[i] Successfully Connected to Gravity database')
        print('[i] Adding / updating domains in the Gravity database')
        cursor.executescript(remote_sql_str)

        sqliteConnection.commit()

        # total_changes is returning 2x the actual value. ¯\_(ツ)_/¯
        # if I made a mistake, please create a PR
        numberOfDomains = sqliteConnection.total_changes
        if numberOfDomains > 1:
            numberOfDomains = numberOfDomains // 2
        #print(f'[i] {numberOfDomains} domains are added to whitelist out of {len(whitelist_remote)}')
        print("[i] {} domains are added to whitelist out of {}" .format(
            numberOfDomains, len(whitelist_remote)))
        total_domains = cursor.execute(
            " SELECT * FROM domainlist WHERE type = 0 OR type = 2 ")
        #print(f'[i] There are a total of {len(total_domains.fetchall())} domains in your whitelist')
        print("[i] There are a total of {} domains in your whitelist" .format(
            len(total_domains.fetchall())))
        cursor.close()

    except sqlite3.Error as error:
        print('[X] Failed to insert domains into Gravity database', error)
        print('\n')
        print('\n')
        exit(1)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print('[i] The database connection is closed')
            print('[i] Restarting Pi-hole. This could take a few seconds')
            subprocess.call(['pihole', 'restartdns', 'reload'],
                            stdout=subprocess.DEVNULL)
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
    subprocess.call(['pihole', 'restartdns', 'reload'],
                    stdout=subprocess.DEVNULL)
    print('[i] Done. Happy ad-blocking :)')
    print('\n')
    print('Star me on GitHub: https://github.com/anudeepND/whitelist')
    print('Buy me a coffee: https://paypal.me/anudeepND')
    print('\n')
