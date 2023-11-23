
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Objects import *
from Anomalies import *
from Signatures import *

def main():
    parser = argparse.ArgumentParser(description="Creates policy conflict MISP-Event")

    parser.add_argument("--policy-id", nargs="*", type=str, required=True, help="Policy ID")
    parser.add_argument("--policy-name", nargs="*", type=str, required=True, help="Policy Name")
    parser.add_argument("--policy-description", nargs="*", type=str, required=True, help="Policy Description")

    parser.add_argument("--role-id", nargs="*", type=str, help="Role ID")
    parser.add_argument("--role-name", nargs="*", type=str, help="Role Name")
    parser.add_argument("--role-description", nargs="*", type=str, help="Role Description")

    parser.add_argument("--permission-id", nargs="*", type=str, help="Permission ID")
    parser.add_argument("--permission-name", nargs="*", type=str, help="Permission Name")
    parser.add_argument("--permission-description", nargs="*", type=str, help="Permission Description")

    parser.add_argument("--identity-uid", type=str, required=True, help="Identity UID")
    parser.add_argument("--identity-full-name", type=str, help="Identity Full Name")
    parser.add_argument("--identity-job-id", type=str, help="Identity Job ID")
    parser.add_argument("--identity-department", type=str, help="Identity Department")
    parser.add_argument("--identity-hiring-date", type=str, help="Identity Hiring Date")
    parser.add_argument("--identity-termination-date", type=str, help="Identity Termination Date")

    args = parser.parse_args()

    # default values for multiple input objects
    args.role_name = args.role_name or ([""] * len(args.role_id) if args.role_id else [])
    args.role_description = args.role_description or ([""] * len(args.role_id) if args.role_id else [])
    args.permission_name = args.permission_name or ([""] * len(args.permission_id) if args.permission_id else [])
    args.permission_description = args.permission_description or ([""] * len(args.permission_id) if args.permission_id else [])
    args.policy_name = args.policy_name or ([""] * len(args.policy_id) if args.policy_id else [])
    args.policy_description = args.policy_description or (
        [""] * len(args.policy_id) if args.policy_id else [])

    # create objects
    signature = DeadElement().getObject()

    permission = Permission(args.permission_id, args.permission_name, args.permission_description).getObject()
    identity = Identity(args.identity_uid, args.identity_full_name, args.identity_job_id, args.identity_department,
                        args.identity_hiring_date, args.identity_termination_date).getObject()
    # course of actions
    courseAutomatedProcesses = CourseOfAction("Automated Processes", "Automation",
                                              "Implement automated processes to detect policy conflicts").getObject()
    # create Event and add objects
    event = Event()
    event.addObjects([signature, courseAutomatedProcesses, permission, identity])

    # references
    identity.add_reference(signature.uuid, relationship_type='refers-to')
    courseAutomatedProcesses.add_reference(signature.uuid, relationship_type='course-of-action')


    # create objects and add references for multiple input objects
    for policy_id, policy_name, policy_description in zip(args.policy_id, args.policy_name, args.policy_description):
        policy = Policy(policy_id, policy_name, policy_description).getObject()
        event.addObjects([policy])
        signature.add_reference(policy.uuid, relationship_type='caused-by')
    for role_id, role_name, role_description in zip(args.role_id, args.role_name, args.role_description):
        role = Role(role_id, role_name, role_description).getObject()
        event.addObjects([role])
        signature.add_reference(role.uuid, relationship_type='caused-by')
    for permission_id, permission_name, permission_description in zip(args.permission_id, args.permission_name, args.permission_description):
        permission = Permission(permission_id, permission_name, permission_description).getObject()
        event.addObjects([permission])
        signature.add_reference(permission.uuid, relationship_type='caused-by')



    print(event.toString())
    event.writeToFile('PolicyConflict')

if __name__ == "__main__":
    main()
