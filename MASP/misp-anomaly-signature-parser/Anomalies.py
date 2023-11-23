from pymisp import MISPObject
import os
definitionsPath = os.path.join("..","venv","Lib","site-packages","pymisp","data","misp-objects","objects")


class Anomaly:
    def __init__(self, anomaly_type, description, threat):
        self.obj = MISPObject(name='iam_anomaly', strict=True,
                              misp_objects_path_custom=definitionsPath)
        self.obj.add_attribute('type', value=anomaly_type)
        self.obj.add_attribute('description', value=description)
        self.obj.add_attribute('threat', value=threat)

    def getObject(self):
        return self.obj



class SharedAccount(Anomaly):
    def __init__(self):
        super().__init__('Shared Account',
                         'Shared accounts are account that are used by more than one person',
                         'Shared accounts can lead to unnoticed integrity and confidentiality issues.')


class OrphanAccount(Anomaly):
    def __init__(self):
        super().__init__('Orphan Account',
                         'Orphan accounts refer to still active accounts despite no identity is available',
                         'Orphan accounts can lead to unauthorized access.')


class ExcessivePermissions(Anomaly):
    def __init__(self):
        super().__init__('Excessive Permissions',
                         'Excessive permissions refer to users having more permissions than necessary for their tasks.',
                         'Excessive permissions can lead to unauthorized data access and privilege escalation.')


class UniversalAccess(Anomaly):
    def __init__(self):
        super().__init__('Universal Access',
                         'Universal access occurs when all users have access to all resources.',
                         'Universal access can lead to data breaches and unauthorized access.')


class ProcessError(Anomaly):
    def __init__(self):
        super().__init__('Process Error',
                         'Policy errors refer missing or errorneous processes.',
                         'Policy errors can lead to unauthorized access.')



class PolicyError(Anomaly):
    def __init__(self):
        super().__init__('Policy Error',
                         'Policy error refers to misconfigurations in policies.',
                         'Alternative bypass can lead to unauthorized access.')


class PrivacyLeakage(Anomaly):
    def __init__(self):
        super().__init__('Privacy Leakage',
                         'Privacy leakage occurs when sensitive data is exposed to unauthorized users.',
                         'Privacy leakage can lead to regulatory violations and loss of trust from customers.')



class PoorDataQuality(Anomaly):
    def __init__(self):
        super().__init__('Poor Data Quality',
                         'Poor data quality refers to inaccuracies in access control data.',
                         'Poor data quality can lead to unauthorized access and outdated access control.')





