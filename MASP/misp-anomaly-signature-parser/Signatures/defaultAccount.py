
import argparse
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Objects import *
from Anomalies import *
from Signatures import *


def main():
    parser = argparse.ArgumentParser(description="Creates default account MISP-Event")

    parser.add_argument("--account-uid", type=str, required=True, help="Account UID")
    parser.add_argument("--account-full-name", type=str, required=False, help="Account Full Name")
    parser.add_argument("--account-application", type=str, required=True, help="Account Application")

    args = parser.parse_args()

    # create objects
    signature = DefaultAccount().getObject()
    account = Account(args.account_uid, args.account_full_name, args.account_application).getObject()

    # course of actions
    courseManage = CourseOfAction("Manage", "Monitoring",
                                     "Manage default accounts.").getObject()
    courseAutomatedProcesses = CourseOfAction("Automated Processes", "Automation",
                                             "Implement automated processes to detect default Accounts").getObject()


    # create event and add objects
    event = Event()
    event.addObjects([signature, account, courseAutomatedProcesses, courseManage])

    # references
    signature.add_reference(account.uuid, relationship_type='caused-by')
    courseManage.add_reference(signature.uuid, relationship_type='course-of-action')
    courseAutomatedProcesses.add_reference(signature.uuid, relationship_type='course-of-action')

    print(event.toString())
    event.writeToFile('DefaultAccount')


if __name__ == "__main__":
    main()
