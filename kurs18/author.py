class Author:
    def __init__(self
                ,firstname:str="BARTLOMIEJ"
                ,lastname:str="NICEWICZ"
                ,age:int=33):
        self.firstname=firstname
        self.lastname=lastname
        self.age=age
    def __repr__(self):
        return f"{self.__class__.__name__}({self.firstname},{self.lastname},{self.age})"