
import argparse
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Objects import *
from Anomalies import *
from Signatures import *


def main():
    parser = argparse.ArgumentParser(description="Creates shared account MISP-Event")

    parser.add_argument("--account-uid", type=str, required=True, help="Account UID")
    parser.add_argument("--account-full-name", type=str, required=False, help="Account Full Name")
    parser.add_argument("--account-application", type=str, required=True, help="Account Application")

    parser.add_argument("--identity-uid", nargs="+", type=str, required=True, help="Identity UID")
    parser.add_argument("--identity-full-name", nargs="*", type=str, help="Identity Full Name")
    parser.add_argument("--identity-job-id", nargs="*", type=str, help="Identity Job ID")
    parser.add_argument("--identity-department", nargs="*", type=str, help="Identity Department")
    parser.add_argument("--identity-hiring-date", nargs="*", type=str, help="Identity Hiring Date")
    parser.add_argument("--identity-termination-date", nargs="*", type=str, help="Identity Termination Date")
    args = parser.parse_args()

    # default values for multiple input objects
    args.identity_full_name = args.identity_full_name or ([""] * len(args.identity_uid) if args.identity_uid else [])
    args.identity_job_id = args.identity_job_id or ([""] * len(args.identity_uid) if args.identity_uid else [])
    args.identity_department = args.identity_department or ([""] * len(args.identity_uid) if args.identity_uid else [])
    args.identity_hiring_date = args.identity_hiring_date or ([""] * len(args.identity_uid) if args.identity_uid else [])
    args.identity_termination_date = args.identity_termination_date or ([""] * len(args.identity_uid) if args.identity_uid else [])

    anomaly = SharedAccount().getObject()
    account = Account(args.account_uid, args.account_full_name, args.account_application).getObject()

    # Create an Anomaly Detection course of action
    courseDetection = CourseOfAction("Anomaly Detection", "Monitoring",
                                     "Implement automated processes to detect anomalous user behavior").getObject()

    # create event and add objects
    event = Event()
    event.addObjects([anomaly, account, courseDetection])

    # references
    anomaly.add_reference(account.uuid, relationship_type='caused-by')
    courseDetection.add_reference(anomaly.uuid, relationship_type='course-of-action')



    # create objects and add references for multiple input objects
    for identity_uid, identity_full_name, identity_job_id, identity_department, identity_hiring_date, identity_termination_date in zip(
            args.identity_uid , args.identity_full_name, args.identity_job_id,
            args.identity_department, args.identity_hiring_date, args.identity_termination_date):


        identity = Identity(identity_uid, identity_full_name, identity_job_id, identity_department,
                            identity_hiring_date, identity_termination_date).getObject()
        event.addObjects([identity])
        identity.add_reference(account.uuid, relationship_type='uses')


    print(event.toString())
    event.writeToFile('SharedAccount')




if __name__ == "__main__":
    main()
