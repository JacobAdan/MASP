
import argparse
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Objects import *
from Anomalies import *
from Signatures import *




def main():

    parser = argparse.ArgumentParser(description="Creates orphan account MISP-Event")

    parser.add_argument("--account-uid", type=str, required=True, help="Account UID")
    parser.add_argument("--account-full-name", type=str, required=False, help="Account Full Name")
    parser.add_argument("--account-application", type=str, required=True, help="Account Application")

    parser.add_argument("--identity-uid", type=str, required=True, help="Identity UID")
    parser.add_argument("--identity-full-name", type=str, help="Identity Full Name")
    parser.add_argument("--identity-job-id", type=str, help="Identity Job ID")
    parser.add_argument("--identity-department", type=str, help="Identity Department")
    parser.add_argument("--identity-hiring-date", type=str, help="Identity Hiring Date")
    parser.add_argument("--identity-termination-date", type=str, help="Identity Termination Date")

    args = parser.parse_args()

    # create objects
    anomaly = OrphanAccount().getObject()
    account = Account(args.account_uid, args.account_full_name, args.account_application).getObject()
    identity = Identity(args.identity_uid, args.identity_full_name, args.identity_job_id, args.identity_department, args.identity_hiring_date, args.identity_termination_date).getObject()

    courseAccess = CourseOfAction("Access Reviews", "Monitoring", "Access reviews support discovering orphan accounts and removing them.").getObject()
    courseAutomated = CourseOfAction("Implement automated processes", "Process", "Automated processes enable the removal of orphan accounts.").getObject()

    # create event and add objects
    event = Event()
    event.addObjects([anomaly, account, identity, courseAccess, courseAutomated])

    # references
    anomaly.add_reference(account.uuid, relationship_type='caused-by')
    identity.add_reference(account.uuid, relationship_type='linked')
    courseAccess.add_reference(anomaly.uuid, relationship_type='course-of-action')
    courseAutomated.add_reference(anomaly.uuid, relationship_type='course-of-action')

    print(event.toString())
    event.writeToFile('OrphanAccount')

if __name__ == "__main__":
    main()
