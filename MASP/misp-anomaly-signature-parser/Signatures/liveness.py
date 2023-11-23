
import argparse
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Objects import *
from Anomalies import *
from Signatures import *


def main():
    parser = argparse.ArgumentParser(description="Creates liveness MISP-Event")

    parser.add_argument("--policy-id", type=str, required=True, help="Policy ID")
    parser.add_argument("--policy-name", type=str,  help="Policy Name")
    parser.add_argument("--policy-description", type=str,  help="Policy Description")

    parser.add_argument("--role-id", type=str, help="Role ID")
    parser.add_argument("--role-name", type=str, help="Role Name")
    parser.add_argument("--role-description", type=str, help="Role Description")

    parser.add_argument("--permission-id", type=str, help="Permission ID")
    parser.add_argument("--permission-name", type=str, help="Permission Name")
    parser.add_argument("--permission-description", type=str, help="Permission Description")

    args = parser.parse_args()

    # create objects
    signature = Liveness().getObject()
    policy = Policy(args.policy_id, args.policy_name, args.policy_description).getObject()
    courseRole = CourseOfAction("Optimize element definitions", "Automation",
                                              "Redefine roles and permissions to support the liveness.").getObject()
    courseAutomatedProcesses = CourseOfAction("Automated Processes", "Automation",
                                              "Implement automated processes to detect elements with only one user.").getObject()
    role = Role(args.role_id, args.role_name, args.role_description).getObject()
    permission = Permission(args.permission_id, args.permission_name, args.permission_description).getObject()

    # create Event and add objects
    event = Event()
    event.addObjects([signature, policy, courseRole, role, permission, courseAutomatedProcesses])

    # references
    signature.add_reference(policy.uuid, relationship_type='caused-by')
    courseRole.add_reference(signature.uuid, relationship_type='course-of-action')
    courseAutomatedProcesses.add_reference(signature.uuid, relationship_type='course-of-action')
    signature.add_reference(role.uuid, relationship_type='caused-by')
    signature.add_reference(permission.uuid, relationship_type='caused-by')

    print(event.toString())
    event.writeToFile('Liveness')


if __name__ == "__main__":
    main()
