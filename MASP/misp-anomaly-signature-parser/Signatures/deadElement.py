
import argparse
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Objects import *
from Anomalies import *
from Signatures import *

def main():
    parser = argparse.ArgumentParser(description="Creates dead element MISP-Event")

    parser.add_argument("--policy-id", type=str, required=True, help="Policy ID")
    parser.add_argument("--policy-name", type=str, help="Policy Name")
    parser.add_argument("--policy-description", type=str,  help="Policy Description")

    parser.add_argument("--role-id", nargs="*", type=str, help="Role ID")
    parser.add_argument("--role-name", nargs="*", type=str, help="Role Name")
    parser.add_argument("--role-description", nargs="*", type=str, help="Role Description")

    parser.add_argument("--permission-id", nargs="*", type=str, help="Permission ID")
    parser.add_argument("--permission-name", nargs="*", type=str, help="Permission Name")
    parser.add_argument("--permission-description", nargs="*", type=str, help="Permission Description")

    args = parser.parse_args()

    # create objects
    signature = DeadElement().getObject()
    policy = Policy(args.policy_id, args.policy_name, args.policy_description).getObject()
    role = Role(args.role_id, args.role_name, args.role_description).getObject()
    permission = Permission(args.permission_id, args.permission_name, args.permission_description).getObject()

    # course of actions
    courseAutomatedProcesses = CourseOfAction("Automated Processes", "Automation",
                                              "Implement automated processes to detect and delete dead elements").getObject()
    # create Event and add objects
    event = Event()
    event.addObjects([signature, policy, courseAutomatedProcesses, role, permission])

    # references
    signature.add_reference(policy.uuid, relationship_type='caused-by')
    courseAutomatedProcesses.add_reference(signature.uuid, relationship_type='course-of-action')
    signature.add_reference(role.uuid, relationship_type='caused-by')
    signature.add_reference(permission.uuid, relationship_type='caused-by')


    print(event.toString())
    event.writeToFile('DeadElements')

if __name__ == "__main__":
    main()
