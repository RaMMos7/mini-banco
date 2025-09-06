from datetime import datetime

class Transaction:
    """ Representa uma única transação bancária. """
    def __init__(self, type, amount, timestamp=None):
        self.type = type 
        self.amount = amount
        self.timestamp = timestamp or datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')

    def to_dict(self):
        """ Converte o objeto Transação para um dicionário para ser guardado em JSON. """
        return self.__dict__

    @staticmethod
    def from_dict(data):
        """ Cria um objeto Transação a partir de um dicionário (vindo do JSON). """
        return Transaction(**data)

class Account:
    """ Representa uma conta bancária. """
    def __init__(self, id, user_id, holder_name, account_number, balance=0.0, transactions=None):
        self.id = id
        self.user_id = user_id  
        self.holder_name = holder_name
        self.account_number = account_number
        self.balance = balance
        self.transactions = [Transaction.from_dict(t) for t in transactions] if transactions else []

    def to_dict(self):
        """ Converte o objeto Conta para um dicionário para ser guardado em JSON. """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "holder_name": self.holder_name,
            "account_number": self.account_number,
            "balance": self.balance,
            "transactions": [t.to_dict() for t in self.transactions]
        }

    @staticmethod
    def from_dict(data):
        """ Cria um objeto Conta a partir de um dicionário. """
        return Account(**data)

