
import argparse
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Objects import *
from Anomalies import *
from Signatures import *


def main():
    parser = argparse.ArgumentParser(description="Creates process Error MISP-Event")

    parser.add_argument("--process-id", type=str, required=True, help="System ID")
    parser.add_argument("--process-name", type=str,  help="System Name")
    parser.add_argument("--process-description", type=str, help="System Description")

    args = parser.parse_args()

    # create objects
    anomaly = ProcessError().getObject()
    process = Process(args.process_id, args.process_name, args.process_description).getObject()
    courseImplement= CourseOfAction("Implementation of process", "Governance", "Implement processes.").getObject()
    courseAutomated = CourseOfAction("Implement automated processes", "Process",
                                     "Automated processes are more reliable.").getObject()

    # create event and add objects
    event = Event()
    event.addObjects([anomaly, process, courseImplement, courseAutomated])

    # references
    anomaly.add_reference(process.uuid, relationship_type='caused-by')
    courseImplement.add_reference(anomaly.uuid, relationship_type='course-of-action')
    courseAutomated.add_reference(anomaly.uuid, relationship_type='course-of-action')

    print(event.toString())
    event.writeToFile('ProcessError')

if __name__ == "__main__":
    main()
