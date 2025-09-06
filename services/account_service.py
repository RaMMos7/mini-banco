from repositories.account_repository import AccountRepository
from models.account_model import Account, Transaction

class AccountService:
    """ Contém a lógica de negócio para as operações das contas. """
    def __init__(self):
        self.repo = AccountRepository()

    def create_account(self, user_id, holder_name, account_number, initial_balance=0.0):
        """ Cria uma nova conta bancária para um utilizador. """
        new_account = Account(id=None, user_id=user_id, holder_name=holder_name, account_number=account_number)
        if initial_balance > 0:
            new_account.balance = initial_balance
            new_account.transactions.append(Transaction("Depósito Inicial", initial_balance))
        return self.repo.save(new_account)

    def get_accounts_for_user(self, user_id):
        """ Obtém todas as contas de um utilizador. """
        return self.repo.get_all_by_user_id(user_id)

    def find_account_by_id(self, account_id, user_id):
        """ Encontra uma conta e verifica se pertence ao utilizador correto. """
        account = self.repo.find_by_id(account_id)
        
        if account and account.user_id == user_id:
            return account
        return None

    def perform_transaction(self, account_id, user_id, transaction_type, amount):
        """ Executa uma transação (depósito ou saque) numa conta. """
        account = self.find_account_by_id(account_id, user_id)
        if not account:
            return None, "Conta não encontrada ou não tem permissão para aceder."
        
        try:
            amount = float(amount)
            if amount <= 0:
                return None, "O valor da transação deve ser positivo."
        except (ValueError, TypeError):
            return None, "Valor inválido."

        if transaction_type == 'deposito':
            account.balance += amount
            account.transactions.append(Transaction("Depósito", amount))
        elif transaction_type == 'saque':
            if account.balance < amount:
                return None, "Saldo insuficiente para realizar o saque."
            account.balance -= amount
            account.transactions.append(Transaction("Saque", amount))
        else:
            return None, "Tipo de transação inválido."
        
        self.repo.save(account)
        return account, f"{transaction_type.capitalize()} de R$ {amount:.2f} realizado com sucesso!"

    def delete_account(self, account_id, user_id):
        """ Elimina uma conta, verificando a posse do utilizador. """
        account = self.find_account_by_id(account_id, user_id)
        if not account:
            return False 
        return self.repo.delete(account_id)

