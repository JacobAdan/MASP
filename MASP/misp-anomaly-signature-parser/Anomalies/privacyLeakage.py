
import argparse
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Objects import *
from Anomalies import *
from Signatures import *

def main():
    parser = argparse.ArgumentParser(description="Creates privacy leakage MISP-Event")

    parser.add_argument("--identity-uid", type=str, required=True, help="Identity UID")
    parser.add_argument("--identity-full-name", type=str, help="Identity Full Name")
    parser.add_argument("--identity-job-id", type=str, help="Identity Job ID")
    parser.add_argument("--identity-department", type=str, help="Identity Department")
    parser.add_argument("--identity-hiring-date", type=str, help="Identity Hiring Date")
    parser.add_argument("--identity-termination-date", type=str, help="Identity Termination Date")


    args = parser.parse_args()

    # create objects
    anomaly = PrivacyLeakage().getObject()
    identity = Identity(args.identity_uid, args.identity_full_name, args.identity_job_id, args.identity_department, args.identity_hiring_date, args.identity_termination_date)
    identity = identity.getObject()

    # course of actions
    courseAccessAudit = CourseOfAction("Audit", "Monitoring",
                                        "Audit access.").getObject()
    courseEncription = CourseOfAction("Encryption", "Governance",
                                             "Encrypt personal information.").getObject()


    # create event and add objects
    event = Event()
    event.addObjects([anomaly, identity, courseAccessAudit, courseEncription])

    # references
    identity.add_reference(anomaly.uuid, relationship_type='leaked')
    courseAccessAudit.add_reference(anomaly.uuid, relationship_type='course-of-action')
    courseEncription.add_reference(anomaly.uuid, relationship_type='course-of-action')



    print(event.toString())
    event.writeToFile('PprivacyLeakage')

if __name__ == "__main__":
    main()
