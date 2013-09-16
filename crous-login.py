#!/usr/bin/env python

"""
crous-login: Fill the forms needed to login to the crous osiris network.
Rodrigo Campos <rodrigo@sdfg.com.ar>
"""

import requests
import time
import subprocess

USER="XXX"
PASS="YYY"


def login(user, password):

    #subprocess.check_call("killall dhclient ; dhclient -v eth0", shell=True)
    time.sleep(1)

    r = requests.get("http://google.com")
    if not "/webauth/loginprocess" in r.text:
        print "Not the expected form. Already conected ?"
        return

    print "Got the form..."

    # Do the POST to: <the same site we connected>/webauth/loginprocess
    payload = { "user": user, "pass": password }
    r = requests.post("http://google.com/webauth/loginprocess", data=payload)

    # Print just in case it says some wierd error
    print r.text

    # Wait till the access is granted
    while 'granted' not in r.text.lower():
        # Two seconds is the time used in the META header to refresh, so we wait
        # the same (and if they change it, fuck it :D)
        time.sleep(2)
        r = requests.get("http://google.com/webauth/statusprocess")

    print "granted! Waiting to activate..."
    time.sleep(10)
    #subprocess.check_call("killall dhclient ; dhclient -v eth0", shell=True)

def connect(use, password):

    while True:
        try:
            login(USER, PASS)
        except:
            print "Error while trying to login, trying again"
            time.sleep(2)
            continue

        break

def are_connected():

    try:
        subprocess.check_call("ping -c 2 8.8.8.8 > /dev/null", shell=True)
        return True
    except:
        return False

if __name__ == "__main__":

    while True:
        if not are_connected():
            print "Not connected! Trying to connect..."
            connect(USER, PASS)

        try:
            time.sleep(60)
        except KeyboardInterrupt:
            print "Checking connection again..."

