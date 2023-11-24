from pymisp import MISPObject




class Signature:
    def __init__(self, anomaly_type, description, threat):
        self.obj = MISPObject(name='iam_signature', strict=True)
        self.obj.add_attribute('type', value=anomaly_type)
        self.obj.add_attribute('description', value=description)
        self.obj.add_attribute('threat', value=threat)



    def getObject(self):
        return self.obj


class DefaultAccount(Signature):
    def __init__(self):
        super().__init__('Default Account',
                         'Default accounts are pre-configured accounts that have standard login information.',
                         'Default accounts can be used by attackers to penetrate the system.')



class DeadElement(Signature):
    def __init__(self):
        super().__init__('Dead element',
                         'Dead element refers to accounts, roles, or permissions that are no longer in use, but are still active.',
                         'Dead element can be used as a gateway by attackers to escalate privileges and penetrate the system.')


class Liveness(Signature):
    def __init__(self):
        super().__init__('Liveness',
                         'Liveness refers to access control elements that are used by exactlcy one user',
                         'Liveness issues can be exploited by attackers for unauthorized access.')


class MissingAccessReviews(Signature):
    def __init__(self):
        super().__init__('Missing Access Reviews',
                         'Missing access reviews refer to a missing process, that validates current access control elements and policies.',
                         'Missing access reviews can result in excessive permissions, data breaches, policy errors, etc.')


class PolicyConflict(Signature):
    def __init__(self):
        super().__init__('Policy Conflict',
                         'Policy conflict occurs when two or more policies contradict each other.',
                         'Policy conflict can lead to misuse of permissions')