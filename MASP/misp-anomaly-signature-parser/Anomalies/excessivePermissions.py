
import argparse
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Objects import *
from Anomalies import *
from Signatures import *

def main():
    parser = argparse.ArgumentParser(description="Creates excessive permissions MISP-Event")

    parser.add_argument("--account-uid", type=str, required=True, help="Account UID")
    parser.add_argument("--account-full-name", type=str, required=False, help="Account Full Name")
    parser.add_argument("--account-application", type=str, required=True, help="Account Application")

    parser.add_argument("--identity-uid", type=str, help="Identity UID")
    parser.add_argument("--identity-full-name", type=str, help="Identity Full Name")
    parser.add_argument("--identity-job-id", type=str, help="Identity Job ID")
    parser.add_argument("--identity-department", type=str, help="Identity Department")
    parser.add_argument("--identity-hiring-date", type=str, help="Identity Hiring Date")
    parser.add_argument("--identity-termination-date", type=str, help="Identity Termination Date")

    parser.add_argument("--policy-id", type=str, help="Policy ID")
    parser.add_argument("--policy-name", type=str, help="Policy Name")
    parser.add_argument("--policy-description", type=str, help="Policy Description")

    parser.add_argument("--role-id", nargs="*", type=str, help="Role ID")
    parser.add_argument("--role-name", nargs="*", type=str, help="Role Name")
    parser.add_argument("--role-description", nargs="*", type=str, help="Role Description")

    parser.add_argument("--permission-id", nargs="*", type=str, help="Permission ID")
    parser.add_argument("--permission-name", nargs="*", type=str, help="Permission Name")
    parser.add_argument("--permission-description", nargs="*", type=str, help="Permission Description")

    args = parser.parse_args()


    # default values for multiple input objects
    args.role_name = args.role_name or ([""] * len(args.role_id) if args.args.role_id else [])
    args.role_description = args.role_description or ([""] * len(args.role_id) if args.role_id else [])
    args.permission_name = args.permission_name or ([""] * len(args.permission_id) if args.permission_id else [])
    args.permission_description = args.permission_description or ([""] * len(args.permission_id) if args.permission_id else [])


    # create objects
    anomaly = ExcessivePermissions().getObject()
    account = Account(args.account_uid, args.account_full_name, args.account_application).getObject()
    identity = Identity(args.identity_uid, args.identity_full_name, args.identity_job_id, args.identity_department, args.identity_hiring_date, args.identity_termination_date)
    identity = identity.getObject()
    policy = Policy(args.policy_id, args.policy_name, args.policy_description).getObject()

    # course of actions
    courseAccessReviews = CourseOfAction("Access Reviews", "Monitoring",
                                        "Conduct regular access reviews to ensure permissions are appropriate").getObject()
    courseAutomatedProcesses = CourseOfAction("Automated Processes", "Automation",
                                             "Implement automated processes to manage and monitor permissions").getObject()
    coursePolicyReview = CourseOfAction("Policy Review", "Governance",
                                        "Regularly review and update policies to align with security best practices").getObject()

    # create event and add objects
    event = Event()
    event.addObjects([anomaly, account, identity, policy, courseAccessReviews, courseAutomatedProcesses, coursePolicyReview])

    # references
    account.add_reference(anomaly.uuid, relationship_type='linked')
    identity.add_reference(anomaly.uuid, relationship_type='linked')
    anomaly.add_reference(policy.uuid, relationship_type='caused-by')
    courseAccessReviews.add_reference(anomaly.uuid, relationship_type='course-of-action')
    courseAutomatedProcesses.add_reference(anomaly.uuid, relationship_type='course-of-action')
    coursePolicyReview.add_reference(anomaly.uuid, relationship_type='course-of-action')

    # create objects and add references for multiple input objects
    for role_id, role_name, role_description in zip(args.role_id, args.role_name, args.role_description):
        role = Role(role_id, role_name, role_description).getObject()
        event.addObjects([role])
        role.add_reference(policy.uuid, relationship_type='linked')

    for permission_id, permission_name, permission_description in zip(args.permission_id, args.permission_name, args.permission_description):
        permission = Permission(permission_id, permission_name, permission_description).getObject()
        event.addObjects([permission])
        permission.add_reference(policy.uuid, relationship_type='linked')

    print(event.toString())
    event.writeToFile('ExcessivePermissions')
if __name__ == "__main__":
    main()
