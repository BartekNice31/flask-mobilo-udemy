class Bank:
    def __init__(self,name):
        self.name=name
    def __repr__(self):
        return f"<Bank({self.name})>"