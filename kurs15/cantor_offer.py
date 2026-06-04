from currency import Currency

class CantorOffer:
    def __init__(self):
        self.currencies=[]
        self.denies_codes=[]
    def load_offer(self):
        self.currencies.append(Currency(code='USD',name='Dollar',flag='flag_usa.png'))
        self.currencies.append(Currency(code='EUR',name='Euro',flag='flag_euro.png'))
        self.currencies.append(Currency(code='JPY',name='Yen',flag='flag_japan.png'))
        self.currencies.append(Currency(code='GBP',name='Pound',flag='flag_england.png'))
        self.denies_codes.append('USD')
    def get_by_code(self,code):
        for currency in self.currencies:
            if currency.code==code:
                return currency
        return Currency(code='unknown',name='unknown',flag='flag_pirat.png')