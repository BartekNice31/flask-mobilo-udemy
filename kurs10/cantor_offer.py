from currency import Currency
class CantorOffer:
    def __init__(self):
        self.currencies=[]
    def load_offer(self):
        self.currencies.append(Currency(code='USD',name='Usd',flag='flag_usa.png'))
        self.currencies.append(Currency(code='EUR',name='Eur',flag='flag_euro.png'))
        self.currencies.append(Currency(code='JPY',name='Yen',flag='flag_japan.png'))
        self.currencies.append(Currency(code='GPB',name='Gpb',flag='flag_england.png'))
        self.currencies.append(Currency(code='PLN',name='Pln',flag="flag_polish.png"))
    def get_by_code(self,code):
        for currency in self.currencies:
            if currency.code==code:
                return currency
        return Currency('unknown','unknown','flag_pirat.png')
    