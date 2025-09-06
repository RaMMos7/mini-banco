import json
from models.user_model import User

class UserRepository:
    def __init__(self, filepath='data.json'):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Garante que o arquivo JSON exista."""
        try:
            with open(self.filepath, 'r') as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.filepath, 'w') as f:
                json.dump({"users": {}, "next_id": 1}, f, indent=4)

    def _read_data(self):
        """Lê os dados do arquivo JSON."""
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def _write_data(self, data):
        """Escreve os dados no arquivo JSON."""
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def get_all(self):
        """Retorna todos os usuários como objetos User."""
        data = self._read_data()
        users_dict = data.get('users', {})
        return [User.from_dict(user_data) for user_data in users_dict.values()]

    def find_by_id(self, user_id):
        """Encontra um usuário pelo seu ID."""
        data = self._read_data()
        user_data = data.get('users', {}).get(str(user_id))
        return User.from_dict(user_data) if user_data else None

    def find_by_email(self, email):
        """Encontra um usuário pelo seu email."""
        users = self.get_all()
        for user in users:
            if user.email == email:
                return user
        return None

    def save(self, user):
        """Salva (cria ou atualiza) um usuário."""
        data = self._read_data()
        
        if not user.id: 
            user.id = data['next_id']
            data['next_id'] += 1
        
        data['users'][str(user.id)] = user.to_dict()
        self._write_data(data)
        return user

    def delete(self, user_id):
        """Deleta um usuário pelo seu ID."""
        data = self._read_data()
        user_id_str = str(user_id)
        if user_id_str in data['users']:
            del data['users'][user_id_str]
            self._write_data(data)
            return True
        return False
