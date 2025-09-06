import json
from models.account_model import Account

class AccountRepository:
    """ Gere a persistência de dados das contas no ficheiro JSON. """
    def __init__(self, filepath='data.json'):
        self.filepath = filepath

    def _read_data(self):
        """ Função interna para ler todos os dados do JSON. """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": {}, "accounts": {}, "next_user_id": 1, "next_account_id": 1}

    def _write_data(self, data):
        """ Função interna para escrever dados no JSON. """
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def get_all_by_user_id(self, user_id):
        """ Encontra todas as contas que pertencem a um determinado utilizador. """
        data = self._read_data()
        accounts_dict = data.get('accounts', {})
        user_accounts = [
            Account.from_dict(acc_data) for acc_data in accounts_dict.values()
            if acc_data['user_id'] == user_id
        ]
        return user_accounts

    def find_by_id(self, account_id):
        """ Encontra uma única conta pelo seu ID. """
        data = self._read_data()
        account_data = data.get('accounts', {}).get(str(account_id))
        return Account.from_dict(account_data) if account_data else None

    def save(self, account):
        """ Guarda (cria ou atualiza) uma conta. """
        data = self._read_data()
        
        if not account.id:  
            account.id = data.get('next_account_id', 1)
            data['next_account_id'] = account.id + 1
        
        data.setdefault('accounts', {})[str(account.id)] = account.to_dict()
        self._write_data(data)
        return account

    def delete(self, account_id):
        """ Elimina uma conta pelo seu ID. """
        data = self._read_data()
        account_id_str = str(account_id)
        if 'accounts' in data and account_id_str in data['accounts']:
            del data['accounts'][account_id_str]
            self._write_data(data)
            return True
        return False

