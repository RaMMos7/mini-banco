from repositories.user_repository import UserRepository
from models.user_model import User
from flask_bcrypt import Bcrypt

# Instância do Bcrypt para criptografia
bcrypt = Bcrypt()

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, name, email, password, is_admin=False):
        """Cria um novo usuário com senha criptografada."""
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        # O primeiro usuário cadastrado será um admin
        if len(self.repo.get_all()) == 0:
            is_admin = True
        
        new_user = User(id=None, name=name, email=email, password_hash=password_hash, is_admin=is_admin)
        return self.repo.save(new_user)

    def authenticate(self, email, password):
        """Autentica um usuário, verificando email e senha."""
        user = self.repo.find_by_email(email)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return None

    def find_by_id(self, user_id):
        """Busca um usuário pelo ID."""
        return self.repo.find_by_id(user_id)

    def find_by_email(self, email):
        """Busca um usuário pelo email."""
        return self.repo.find_by_email(email)

    def get_all_users(self):
        """Retorna todos os usuários."""
        return self.repo.get_all()

    def update_user(self, user_id, name, email):
        """Atualiza os dados de um usuário."""
        user = self.repo.find_by_id(user_id)
        if user:
            user.name = name
            user.email = email
            self.repo.save(user)
            return user
        return None

    def delete_user(self, user_id):
        """Deleta um usuário."""
        return self.repo.delete(user_id)
