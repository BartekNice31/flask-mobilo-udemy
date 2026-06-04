from priority_type import PriorityType

class NotificationPriorities:
    def __init__(self):
        self.list_of_priorities=[]
    def load_priorities(self):
        self.list_of_priorities.append(PriorityType(code='HIGH PRIORITY'
                                 ,description='Critical notification content<'
                                 ,selected='HIGH PRIORITY'))
        self.list_of_priorities.append(PriorityType(code='MEDIUM'
                                ,description='Important notification content'
                                ,selected='MEDIUM'))
        self.list_of_priorities.append(PriorityType(code='NOT URGENT'
                                ,description='Notification content, not urgent'
                                ,selected='NOT URGENT'))
        self.list_of_priorities.append(PriorityType(code='LOW'
                                ,description='Low notification, most low urgent'
                                ,selected='LOW'))
    def get_priority_by_code(self,code):
        for priority in self.list_of_priorities:
            if priority.code==code:
                return priority
        return PriorityType(code='unknown'
                        ,description='unknown'
                        ,selected='unknown')