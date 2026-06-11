from priority_type import PriorityType

class NotificationPriorities:
    def __init__(self):
        self.list_of_priorities = []
    
    def load_priorities(self):
        self.list_of_priorities.append(PriorityType('high','HIGH PRIORITY', False))
        self.list_of_priorities.append(PriorityType('medium','MEDIUM', False))
        self.list_of_priorities.append(PriorityType('normal', 'NOT URGENT', True))
        self.list_of_priorities.append(PriorityType('low', 'REMARK', False))

    def get_priority_by_code(self, code):
        for p in self.list_of_priorities:
            if p.code == code:
                return p
        return PriorityType('normal', 'NOT URGENT', True)
