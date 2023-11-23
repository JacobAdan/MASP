
import argparse
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Objects import *
from Anomalies import *
from Signatures import *


def main():
    parser = argparse.ArgumentParser(description="Creates universal access MISP-Event")

    parser.add_argument("--system-id", type=str, required=True, help="System ID")
    parser.add_argument("--system-name", type=str,  help="System Name")
    parser.add_argument("--system-description", type=str, help="System Description")

    args = parser.parse_args()

    event = create(args.system_id, args.system_name, args.system_description)


def create(system_id, system_name, system_description):
    # create objects
    anomaly = UniversalAccess().getObject()
    system = System(system_id, system_name, system_description).getObject()
    courseOfAction = CourseOfAction("Implementation of standard", "Governance",
                                    "Implement iam or connect system").getObject()

    # create event and add objects
    event = Event()
    event.addObjects([anomaly, system, courseOfAction])

    # references
    anomaly.add_reference(system.uuid, relationship_type='caused-by')
    courseOfAction.add_reference(anomaly.uuid, relationship_type='course-of-action')
    print(event.toString())
    event.writeToFile('UniversalAccess')
    return event.toString()


if __name__ == "__main__":
    main()
