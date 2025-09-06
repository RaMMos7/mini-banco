class User:
    def __init__(self, id, name, email, password_hash, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin

    def to_dict(self):
        """Converte o objeto User para um dicionário para salvar em JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "is_admin": self.is_admin
        }

    @staticmethod
    def from_dict(data):
        """Cria um objeto User a partir de um dicionário."""
        return User(
            id=data.get('id'),
            name=data.get('name'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            is_admin=data.get('is_admin', False)
        )
