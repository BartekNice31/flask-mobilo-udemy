class Currency:
    def __init__(self,code,name,flag):
        self.code=code
        self.name=name
        self.flag=flag
    def __repr__(self):
        return f"<Currency({self.code})>"