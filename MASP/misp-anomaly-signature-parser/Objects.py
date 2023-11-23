import os
from pymisp import MISPEvent, MISPAttribute, MISPObject
import datetime
import time
import Anomalies
definitionsPath = os.path.join("..","venv","Lib","site-packages","pymisp","data","misp-objects","objects")
class Event:
    def __init__(self):
        self.e = MISPEvent()
        self.e.publish()
        self.e.info = "Event describes iam anomalies and signatures"
        self.e.date = datetime.date.today()
        self.e.timestamp = int(time.time())
        #self.e.publish_timestamp = "1691417706"
        self.e.org_id = "1"
        self.e.orgc_id = "1"
        self.e.distribution = 1


    def addObjects(self, objects):
        for object in objects:
            self.e.add_object(object)

    def getEvent(self):
        return self.e

    def toString(self):
        return '{"Event":' + self.e.to_json(indent=" ") + '}'

    def writeToFile(self, name):
        filename = name + '_' + str(self.e.date) + '_' + str(self.e.timestamp) + ".json"
        completeName = os.path.join('..','Results', filename)
        f = open(completeName, "w")
        f.write('{"Event":' + self.e.to_json(indent=" ") + '}')
        f.close()

class Identity:
    def __init__(self, uid,  fullName, jobId, dept, hiring, termination):
        self.obj = MISPObject(name='iam_identity', strict=True,
                              misp_objects_path_custom=definitionsPath)
        self.obj.add_attribute('uid', value=uid)
        self.obj.add_attribute('full-name', value=fullName)
        self.obj.add_attribute('job-id', value=jobId)
        self.obj.add_attribute('department', value=dept)
        self.obj.add_attribute('hiring-date', value=hiring)
        self.obj.add_attribute('termination-date', value=termination)

    def getObject(self):
        return self.obj

class Account:
    def __init__(self, uid, full_name, application):
        self.obj = MISPObject(name='iam_account', strict=True,
                              misp_objects_path_custom=definitionsPath)
        self.obj.add_attribute('uid', value=uid)
        self.obj.add_attribute('full-name', value=full_name)
        self.obj.add_attribute('application', value=application)

    def getObject(self):
        return self.obj

class Permission:
    def __init__(self, permission_id, permission_name, description):
        self.obj = MISPObject(name='iam_permission', strict=True,
                              misp_objects_path_custom=definitionsPath)
        self.obj.add_attribute('permission-id', value=permission_id)
        self.obj.add_attribute('permission-name', value=permission_name)
        self.obj.add_attribute('description', value=description)

    def getObject(self):
        return self.obj

class Role:
    def __init__(self, role_id, role_name, description):
        self.obj = MISPObject(name='iam_role', strict=True,
                              misp_objects_path_custom=definitionsPath)
        self.obj.add_attribute('role-id', value=role_id)
        self.obj.add_attribute('role-name', value=role_name)
        self.obj.add_attribute('description', value=description)


    def getObject(self):
        return self.obj



class Policy:
    def __init__(self, policy_id, policy_name, description):
        self.obj = MISPObject(name='iam_policy', strict=True,
                              misp_objects_path_custom=definitionsPath)
        self.obj.add_attribute('policy-id', value=policy_id)
        self.obj.add_attribute('policy-name', value=policy_name)
        self.obj.add_attribute('description', value=description)

    def getObject(self):
        return self.obj

class Process:
    def __init__(self, process_id, process_name, description):
        self.obj = MISPObject(name='iam_process', strict=True,
                              misp_objects_path_custom=definitionsPath)
        self.obj.add_attribute('process-id', value=process_id)
        self.obj.add_attribute('process-name', value=process_name)
        self.obj.add_attribute('description', value=description)

    def getObject(self):
        return self.obj


class System:
    def __init__(self, system_id, system_name, description):
        self.obj = MISPObject(name='iam_system', strict=True,
                              misp_objects_path_custom=definitionsPath)
        self.obj.add_attribute('system-id', value=system_id)
        self.obj.add_attribute('system-name', value=system_name)
        self.obj.add_attribute('description', value=description)

    def getObject(self):
        return self.obj



class CourseOfAction:
        def __init__(self, name, type, description):
            self.obj = MISPObject(name='course-of-action', strict=True,
                                  misp_objects_path_custom=definitionsPath)
            self.obj.add_attribute('name', value=name)
            self.obj.add_attribute('type', value=type)
            self.obj.add_attribute('description', value=description)

        def getObject(self):
            return self.obj
