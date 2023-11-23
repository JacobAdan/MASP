
import argparse
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Objects import *
from Anomalies import *
from Signatures import *

def main():
    parser = argparse.ArgumentParser(description="Creates poor data quality MISP-Event")

    parser.add_argument("--account-uid", type=str,  help="Account UID")
    parser.add_argument("--account-full-name", type=str, help="Account Full Name")
    parser.add_argument("--account-application", type=str,  help="Account Application")

    parser.add_argument("--identity-uid", type=str,  help="Identity UID")
    parser.add_argument("--identity-full-name", type=str, help="Identity Full Name")
    parser.add_argument("--identity-job-id", type=str, help="Identity Job ID")
    parser.add_argument("--identity-department", type=str, help="Identity Department")
    parser.add_argument("--identity-hiring-date", type=str, help="Identity Hiring Date")
    parser.add_argument("--identity-termination-date", type=str, help="Identity Termination Date")

    parser.add_argument("--policy-id", type=str,  help="Policy ID")
    parser.add_argument("--policy-name", type=str, help="Policy Name")
    parser.add_argument("--policy-description", type=str, help="Policy Description")

    parser.add_argument("--role-id", type=str, help="Role ID")
    parser.add_argument("--role-name", type=str, help="Role Name")
    parser.add_argument("--role-description", type=str, help="Role Description")

    parser.add_argument("--permission-id", type=str, help="Permission ID")
    parser.add_argument("--permission-name", type=str, help="Permission Name")
    parser.add_argument("--permission-description", type=str, help="Permission Description")

    args = parser.parse_args()

    # create objects
    anomaly = PoorDataQuality().getObject()
    account = Account(args.account_uid, args.account_full_name, args.account_application).getObject()
    identity = Identity(args.identity_uid, args.identity_full_name, args.identity_job_id, args.identity_department, args.identity_hiring_date, args.identity_termination_date)
    identity = identity.getObject()
    policy = Policy(args.policy_id, args.policy_name, args.policy_description).getObject()
    role = Role(args.role_id, args.role_name, args.role_description).getObject()
    permission = Permission(args.permission_id, args.permission_name, args.permission_description).getObject()

    # course of actions
    courseAccessQuality = CourseOfAction("Quality Management", "Monitoring",
                                        "Implement and monitor data quality policies to ensure good data quality").getObject()


    # create event and add objects
    event = Event()
    event.addObjects([anomaly, account, identity, policy, courseAccessQuality])

    # references
    anomaly.add_reference(account.uuid, relationship_type='caused-by')
    anomaly.add_reference(identity.uuid, relationship_type='caused-by')
    anomaly.add_reference(policy.uuid, relationship_type='caused-by')
    anomaly.add_reference(role.uuid, relationship_type='caused-by')
    anomaly.add_reference(permission.uuid, relationship_type='caused-by')
    courseAccessQuality.add_reference(anomaly.uuid, relationship_type='course-of-action')


    print(event.toString())
    event.writeToFile('PoorDataQuality')

if __name__ == "__main__":
    main()
