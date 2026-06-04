class Bank:
    def __init__(self,name,city,country):
        self.name=name
        self.city=city
        self.country=country

class Banks:
    def __init__(self):
        self.banks=[]
    def load_banks(self):
        self.banks.append(Bank(name="BRITISH_BANK",city="London",country="England"))
        self.banks.append(Bank(name="PKO",city="WARSAW",country="Warsaw"))
        self.banks.append(Bank(name="USA_BANK",city="New York",country="USA"))
        self.banks.append(Bank(name="JAPAN_BANK",city="Tokyo",country="Japan"))
    def get_name(self,name):
        for bank in self.banks:
            if bank.name==name:
                return bank
        return Bank(name="unknown",city="unknown",country="unknown")