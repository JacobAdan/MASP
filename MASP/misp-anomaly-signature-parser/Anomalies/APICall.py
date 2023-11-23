from pymisp import ExpandedPyMISP, MISPEvent
import sys, os
import subprocess
import json
import argparse
import urllib3
import csv

misp_url = ''
misp_key = 'hpXAn5S9eBxFBSa10ItwsKvtGndEcBOhUQbsdlE2'
path = os.path.join('..','SharedAccounts.csv')


def postEvent(cmd):


    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    output = subprocess.check_output(cmd, universal_newlines=True)

    misp_verifycert = False

    misp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert, 'json')

    event = MISPEvent()
    event.load(json.loads(output))

    response = misp.add_event(event, pythonify=True)

    if response.get('errors'):
        print(response.info)
    else:
        print('Created Event with ID: ' + str(response.id))

def readFile():

    with open(path, 'r') as file:
        csvreader = csv.reader(file, delimiter=';')
        for row in csvreader:

            cmd = ["python", "sharedAccount.py", "--account-uid", row[1], "--account-full-name", row[2], "--account-application", row[3], "--identity-uid", row[4], row[5], row[6],"--identity-full-name", row[7],  row[8], row[9]]
            postEvent(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sends MISP-Event to MISP-Instance")
    #parser.add_argument("--csv-path", type=str, required=True, help="Path to csv file")
    parser.add_argument("--misp-ip-adress", type=str, required=True, help="IP-Adress of MISP-Instance")
    args = parser.parse_args()

    misp_url = args.misp_ip_adress
    readFile()
